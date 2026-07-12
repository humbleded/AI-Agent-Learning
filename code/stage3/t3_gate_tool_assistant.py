"""
T3-Gate Tool Calling 闯关：真实三工具助手。

运行（项目根目录）：
    .venv/Scripts/python.exe code/stage3/t3_gate_tool_assistant.py

本关目标：
    1. 把计算器、沙箱文件、外部 API 写成模型可见的 tools schema。
    2. 让 DeepSeek 真实返回 assistant.tool_calls，不用关键词 if/elif 代替模型选择。
    3. 客户端校验工具名和 JSON 参数，再从 TOOLS 注册表执行真实函数。
    4. 把结果以 role="tool" + tool_call_id 回填，第二次调用模型生成最终回答。
    5. 覆盖无需工具、坏参数、工具失败、危险路径/恶意 URL 和最大工具轮数。

模式约定：
    本关先显式使用 non-thinking mode：extra_body={"thinking": {"type": "disabled"}}。
    deepseek-v4-pro 默认 thinking；thinking + tool calls 还要求持续回传 reasoning_content，
    这是 A4 多步 Agent 再扩展的内容，不和第一次 Tool Calling 闭环混在一起。

通过标准：
    - 计算、读文件、外部 API 各真跑至少 1 次。
    - 无工具问题可直接回答；沙箱外路径、localhost/私网/metadata 等恶意 URL 必须拒绝。
    - eval_cases.json 含 10 正常 + 3 失败 + 1 危险输入；正式复核者直接执行并把关键结果写入 daily。

评估产物边界：T3 只长期保留 eval_cases.json，不保存专用 runner、baseline 或原始运行报告。
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI
import math

from t3_02_calculator_tool import calculator_tool
from t3_03_file_reader_tool import read_sandbox_file
from t3_04_public_api_tool import public_api_tool

load_dotenv()


MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
MAX_TOOL_ROUNDS = 3

TOOLS = {
    "calculator_tool": calculator_tool,
    "read_sandbox_file": read_sandbox_file,
    "public_api_tool": public_api_tool,
}


def build_tool_schemas():
    """返回 OpenAI/DeepSeek `tools` 参数需要的三个 function schema。"""
    # TODO 2：参数类型、required、additionalProperties 要与真实函数签名一致。
    tools_list = []
    calculator_tool_Schema = {
        "type": "function",
        "function": {
            "name": "calculator_tool",
            "description": "输入一个运算规则和两个数字或者字符串数字，进行两个数的加，减，乘，除精确运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "sub", "mul", "div"],
                        "description": "必选参数,用来进行两个数精确计算的规则",
                    },
                    "a": {
                        "anyOf": [
                            {"type": "number"},
                            {"type": "string"},
                        ],
                        "description": "数字或者数字字符串类型的参数",
                    },
                    "b": {
                        "anyOf": [
                            {"type": "number"},
                            {"type": "string"},
                        ],
                        "description": "数字或者数字字符串类型的参数",
                    },
                },
                "required": ["operation", "a", "b"],
                "additionalProperties": False,
            },
        },
    }

    read_sandbox_file_Schema = {
        "type": "function",
        "function": {
            "name": "read_sandbox_file",
            "description": "只能读取项目沙箱内的文本文件，并返回截断后的内容。",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {
                        "type": "string",
                        "description": "必选参数,这是 resources/sandbox/ 内的相对路径",
                    },
                    "max_chars": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5000,
                        "default": 1000,
                        "description": "可选参数,限制最多返回多少个字符",
                    },
                },
                "required": ["relative_path"],
                "additionalProperties": False,
            },
        },
    }
    public_api_tool_Schema = {
        "type": "function",
        "function": {
            "name": "public_api_tool",
            "description": "仅在用户明确要求检查公开 API 状态时调用，返回API当前的状态。",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "default": "https://api.github.com",
                        "description": "访问客户端允许列表内的 HTTPS 公开 API",
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    }
    tools_list.append(calculator_tool_Schema)
    tools_list.append(read_sandbox_file_Schema)
    tools_list.append(public_api_tool_Schema)
    return tools_list


def create_client():
    """读取 DEEPSEEK_API_KEY，返回连接 DeepSeek 的 OpenAI 客户端。"""
    # TODO：缺 key 时给稳定错误；不要把 key 写进代码。
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError(
            "未设置 DEEPSEEK_API_KEY：请在项目根目录 .env 里加一行 DEEPSEEK_API_KEY=你的key"
        )
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    return client


def execute_tool_call(tool_call):
    """校验一个模型 tool_call，执行真实工具并返回可 JSON 序列化的结果。

    提示顺序：取 name/arguments -> 校验工具白名单 -> json.loads -> 校验 dict
    -> 对 public_api_tool 校验 scheme/host/port；禁用自动重定向或逐跳校验 Location
    -> TOOLS[name](**arguments) -> 捕获参数/执行错误并返回稳定 ok/error。
    """
    # TODO 1：绝不能 eval(arguments)，也不能执行 TOOLS 以外的名字。
    # TODO 2：public_api_tool 不得接收任意 URL；拒绝 loopback、私网、link-local、
    #         云 metadata 地址与重定向逃逸；不能只校验初始 URL 后自动跟随跳转。
    #         为正常 URL、初始恶意 URL、危险重定向分别写可重复测试。
    tool_call_function_name = tool_call.function.name
    tool_call_arguments = tool_call.function.arguments
    if tool_call_function_name not in TOOLS:
        return {"ok": False, "error": f"工具 {tool_call_function_name} 不在白名单中"}
    try:
        if not isinstance(tool_call_arguments, str):
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} 参数不是合法 JSON 字符串",
            }
        arguments_dict = json.loads(tool_call_arguments)
    except (json.JSONDecodeError, TypeError) as e:
        return {
            "ok": False,
            "error": f"工具 {tool_call_function_name} 参数不是合法 JSON: {str(e)}",
        }
    # 判断参数是否为字典
    if not isinstance(arguments_dict, dict):
        return {
            "ok": False,
            "error": f"工具 {tool_call_function_name} 参数不是合法 JSON 对象",
        }
    # 从 build_tool_schemas() 构造：
    # 工具名 → parameters schema
    tool_schemas = build_tool_schemas()
    schema_dict = {
        tool["function"]["name"]: tool["function"]["parameters"]
        for tool in tool_schemas
    }
    schema = schema_dict[tool_call_function_name]
    required_fields = schema.get("required", [])
    # 找出缺失的必填字段；存在时返回稳定错误。
    missing_fields = [field for field in required_fields if field not in arguments_dict]
    if missing_fields:
        return {
            "ok": False,
            "error": f"工具 {tool_call_function_name} 缺少必填字段: {sorted(missing_fields)}",
        }
    allowed_fields = schema.get("properties", {}).keys()
    # 找出 schema 未声明的多余字段；存在时返回稳定错误。
    extra_fields = [field for field in arguments_dict if field not in allowed_fields]
    # 错误中的字段列表用 sorted(...)，保证测试结果顺序稳定。
    if extra_fields:
        return {
            "ok": False,
            "error": f"工具 {tool_call_function_name} 存在多余字段: {sorted(extra_fields)}",
        }

    if tool_call_function_name == "calculator_tool":
        operation = arguments_dict.get("operation")

        # 判断operation类型是否为字符串且非空
        if not operation or not isinstance(operation, str):
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} operation 字段必须是非空字符串",
            }

        # operation 必须是 add/sub/mul/div
        if operation not in ["add", "sub", "mul", "div"]:
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} operation 字段必须是 add/sub/mul/div",
            }

        # 判断 a 和 b 是否为数字或数字字符串,转str 还要尝试转换成 float；转换失败就拒绝
        a = arguments_dict.get("a")
        b = arguments_dict.get("b")

        for arg_name, arg_value in [("a", a), ("b", b)]:
            if isinstance(arg_value, bool):
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} {arg_name} 字段不能是布尔值",
                }
            if not isinstance(arg_value, (int, float, str)):
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} {arg_name} 字段必须是数字或数字字符串",
                }
            try:
                numeric_value = float(arg_value)
            except (ValueError, OverflowError):
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} {arg_name} 字段必须是数字或数字字符串",
                }
            if not math.isfinite(numeric_value):
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} {arg_name} 字段不能是无穷大或 NaN",
                }

    elif tool_call_function_name == "read_sandbox_file":
        # relative_path 必须是 resources/sandbox/ 内的相对路径
        relative_path = arguments_dict.get("relative_path")
        if not relative_path or not isinstance(relative_path, str):
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} relative_path 字段必须是非空字符串",
            }
        # 禁止访问沙箱外的路径
        if (
            ".." in relative_path
            or relative_path.startswith("/")
            or relative_path.startswith("\\")
        ):
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} relative_path 字段不能访问沙箱外路径",
            }
        # max_chars 若提供，必须是非 bool 的 int，且满足 1 <= max_chars <= 5000
        max_chars = arguments_dict.get("max_chars")
        if max_chars is not None and isinstance(max_chars, bool):
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} max_chars 字段必须是整数",
            }
        if max_chars is not None:
            if not isinstance(max_chars, int):
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} max_chars 字段必须是整数",
                }
            if not (1 <= max_chars <= 5000):
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} max_chars 字段必须在 1 到 5000 之间",
                }

    elif tool_call_function_name == "public_api_tool":
        # url 必须是 HTTPS 且在允许列表内
        url = arguments_dict.get("url", "https://api.github.com")

        # 先检查是 str，再执行 .startswith() 和 urlparse()
        if not isinstance(url, str):
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} url 字段必须是字符串",
            }

        if not url.startswith("https://"):
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} url 字段必须是 HTTPS",
            }
        # 允许列表：github、openai、deepseek
        allowed_hosts = ["api.github.com", "api.openai.com", "api.deepseek.com"]
        from urllib.parse import urlparse

        # 端口号若提供，必须是合法整数；urlparse.port 若不合法会抛 ValueError
        try:
            parsed_url = urlparse(url)
            # 如果是 : 结尾的 url，parsed_url.netloc 会以 : 结尾，这种情况也算端口号不合法
            if parsed_url.netloc.endswith(":"):
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} url 字段端口号不合法",
                }

            if parsed_url.hostname not in allowed_hosts:
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} url 字段不在允许列表内",
                }
            parsed_url_port = parsed_url.port
            # 前面显式的空端口被拦截，隐式的空端口和 443 都是合法的；其他端口号都不合法
            if parsed_url_port not in [None, 443]:
                return {
                    "ok": False,
                    "error": f"工具 {tool_call_function_name} url 字段端口号不合法",
                }
        except ValueError:
            return {
                "ok": False,
                "error": f"工具 {tool_call_function_name} url 字段端口号不合法",
            }

    try:
        result = TOOLS[tool_call_function_name](**arguments_dict)
        return result
    except Exception as e:
        return {
            "ok": False,
            "error": f"工具 {tool_call_function_name} 执行失败: {str(e)}",
        }


def run_agent(user_text, max_tool_rounds=MAX_TOOL_ROUNDS):
    """完成模型决策、客户端执行、Observation 回填和最终回答。

    要同时处理两条分支：
      - message.tool_calls 为空：直接返回 message.content。
      - 有 tool_calls：保存 assistant 消息，逐个执行并追加 role="tool" 消息，
        再请求模型；超过 max_tool_rounds 时稳定停止。
    """
    # TODO 1：创建 client、messages、tools。
    # TODO 2：调用 chat.completions.create(..., tools=tools,
    #         extra_body={"thinking": {"type": "disabled"}})。
    #         tool_choice 默认就是 auto，本关可先不显式传。
    # TODO 3：区分直接回答与 tool_calls；回填必须带对应 tool_call_id。
    # TODO 4：工具结果用 json.dumps(..., ensure_ascii=False) 转成字符串。
    # TODO 5：处理 API/消息异常和最大轮数，不能把模型自编文本当 Observation。
    try:
        client = create_client()
    except Exception as e:
        return f"创建客户端失败: {str(e)}"
    tools = build_tool_schemas()
    messages = [
        {
            "role": "system",
            "content": "你是三工具助手，可用工具：calculator_tool、read_sandbox_file、public_api_tool",
        },
        {"role": "user", "content": user_text},
    ]
    tool_rounds = 0
    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                extra_body={"thinking": {"type": "disabled"}},
            )
        except Exception as e:
            return f"调用模型失败: {str(e)}"
        if not response.choices or not response.choices[0].message:
            return "模型未返回有效消息"
        message = response.choices[0].message

        if not message.tool_calls:
            # None或者空字符串
            if not message.content:
                return "模型未返回有效内容"
            else:
                return message.content
        # 调用工具轮数超过 max_tool_rounds 时，稳定停止并返回提示。
        if tool_rounds >= max_tool_rounds:
            return f"已达到最大工具调用轮数 {max_tool_rounds}，停止执行。"
        # 有 tool_calls，逐个执行并回填 role="tool" 消息
        messages.append(message)
        for tool_call in message.tool_calls:
            tool_result = execute_tool_call(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(tool_result, ensure_ascii=False),
                    "tool_call_id": tool_call.id,
                }
            )
        tool_rounds += 1


def main():
    """读取用户问题，运行三工具助手，并打印最终回答。"""
    # TODO：空输入给提示；允许输入 exit/quit 退出；不要在这里复制 Agent 主循环。
    input_text = input("请输入问题（输入 exit 或 quit 退出）：").strip()
    if not input_text:
        print("输入不能为空，请重新输入。")
        return
    if input_text.lower() in ["exit", "quit"]:
        print("退出程序。")
        return
    answer = run_agent(input_text)
    print("最终回答：", answer)


if __name__ == "__main__":
    main()
