def before_run(func):
    def wrapper(*args, **kwargs):
        print("函数马上开始")
        result = func(*args, **kwargs)
        return result
    return wrapper

def after_run(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("函数已经结束")
        return result
    return wrapper

@before_run
@after_run
def say(name):
    print(f"Hello, {name}")

say("Alice")


LABELS=['工作','账单 ','促销 ','其他 ']

def classify(text):
    if any(word in text for word in ["工作", "项目", "会议"]):
        return "工作"
    elif any(word in text for word in ["账单", "发票", "付款"]):
        return "账单 "
    elif any(word in text for word in ["促销", "优惠", "打折"]):
        return "促销 "
    else:
        return "其他 "

def route(text):
    category = classify(text)
    # if category == "问题":
    #     return answer(text)
    # elif category == "投诉":
    #     return escalate(text)
    # elif category == "建议":
    #     return log_idea(text)
    # elif category == "闲聊":
    #     return chat(text)
    # else:
    #     return fallback(text)
    #用dict实现
    route_dict = {
        "问题": answer,
        "投诉": escalate,
        "建议": log_idea,
        "闲聊": chat,
        "其他": fallback
    }
    return route_dict.get(category, fallback)(text)
    
def answer(text): ...      # 自动答疑
def escalate(text): ...    # 转人工
def log_idea(text): ...    # 记录建议
def chat(text): ...        # 闲聊回复
def fallback(text): ...    # 兜底处理


import json

def get_weather(location):
    return f"{location}：多云，22°C"

TOOLS = {"get_weather": get_weather}

messages = [
    {"role": "system", "content": "你是天气助手，可用工具：get_weather(location)"},
    {"role": "user", "content": "巴黎今天多热？"},
]

model_output = '{"action": "get_weather", "action_input": {"location": "巴黎"}}'

# TODO ①：把 model_output 解析成 dict，取出工具名 tool_name 和参数 args
action_dict = json.loads(model_output)
tool_name = action_dict["action"]
args = action_dict["action_input"]

# TODO ②：从 TOOLS 注册表按 tool_name 找到函数并真正执行，结果存进 result
result = TOOLS[tool_name](**args)

# TODO ③：把 result 作为 Observation 拼回 messages——role 用 "tool"，content 放 result
messages.append({"role": "tool", "content": result})