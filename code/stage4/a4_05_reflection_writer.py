"""A4-05：实现一个带质量门槛的 Reflection Writer。

最终运行方式（项目根目录）：
    .venv/Scripts/python.exe code/stage4/a4_05_reflection_writer.py

最终任务与通过标准：
    - 使用真实 DeepSeek 依次生成初稿、评审反馈和改进稿。
    - 保留可观察的 Reflection 轨迹与稳定停止边界。
    - 用同一套硬约束比较初稿和改进稿，退化版本不能覆盖当前最佳稿。
    - 输出初稿、反思、改进稿和对比结果。

实现阶段状态：
    C1～C6 实现检查点已完成；已取得真实 DeepSeek 的正常提前停止轨迹，
    以及故障注入下的初稿、反思、改进稿和同标准对比轨迹；待正式练习与复核。
"""


import os
from collections.abc import Callable

from dotenv import load_dotenv
from openai import OpenAI


EVENT_DATE = "2026年8月8日"
EVENT_LOCATION = "3号会议室"
MAX_DRAFT_LENGTH = 80
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-pro"

WRITING_TASK = (
    "请为公司内部的 AI Agent 学习分享会写一则中文公告。"
    f"必须写明日期“{EVENT_DATE}”和地点“{EVENT_LOCATION}”，"
    f"去除首尾空白后总长度不超过 {MAX_DRAFT_LENGTH} 个字符；"
    "语气简洁，并明确邀请同事参加。"
)


def evaluate_draft(draft: str) -> dict[str, bool | int]:
    """返回公告的日期、地点、长度及总硬约束检查结果。"""
    # C1：
    # 1. 去除 draft 首尾空白，并计算规范化后的长度。
    # 2. 分别检查 EVENT_DATE、EVENT_LOCATION 和 MAX_DRAFT_LENGTH。
    # 3. 返回 length、date_present、location_present、within_length、
    #    all_hard_constraints_pass 五个字段。
    normalized_draft = draft.strip()
    length = len(normalized_draft)
    date_present = EVENT_DATE in normalized_draft
    location_present = EVENT_LOCATION in normalized_draft
    within_length = length <= MAX_DRAFT_LENGTH
    all_hard_constraints_pass = date_present and location_present and within_length

    return {
        "length": length,
        "date_present": date_present,
        "location_present": location_present,
        "within_length": within_length,
        "all_hard_constraints_pass": all_hard_constraints_pass,
    }


def build_initial_prompt(task: str) -> str:
    """构造只生成公告初稿的 Execution prompt。"""
    #C2：包含原始任务，并约束模型只输出公告正文。
    return (
        f"任务：{task}\n"
        "请只输出公告正文，不要包含任何额外说明。"
    )


def build_reflection_prompt(
    task: str,
    draft: str,
    hard_checks: dict[str, bool | int],
) -> str:
    """构造结合原始任务、待评审稿和硬检查结果的 Reflection prompt。"""
    # C2：明确日期、地点、长度、清晰度和行动指引等评审标准；
    # 有问题时逐项输出“问题、证据、修改建议”，全部通过时只输出“无需改进”。
    return (
        f"任务：{task}\n"
        f"待评审稿：{draft}\n"
        f"硬检查结果：{hard_checks}\n"
        "评审标准包括日期、地点、文本长度不超过80字、表达清晰和行动指引。\n"
        "请根据以上信息进行反思，逐项输出“问题、证据、修改建议”，"
        "如果全部通过，请只输出“无需改进”。"
    )


def build_refinement_prompt(task: str, draft: str, feedback: str) -> str:
    """构造结合原始任务、上一版草稿和反馈的 Refinement prompt。"""
    # C2：要求保留全部硬约束，并只输出改进后的公告正文。
    return (
        f"任务：{task}\n"
        f"上一版草稿：{draft}\n"
        f"反馈：{feedback}\n"
        "请根据以上信息进行改进，保留全部硬约束，"
        "只输出改进后的公告正文，不要包含任何额外说明。"
    )


def run_reflection_once(
    task: str,
    llm_call: Callable[[str], str],
) -> dict[str, object]:
    """执行至多一轮 Reflection，并返回可观察的调用轨迹。"""
    # C3：
    # 1. 依次完成初稿生成、初稿硬检查和 Reflection，并按实际发生顺序记录
    #    trajectory；每条记录形如 {"type": "execution/reflection", "content": ...}。
    # 2. 将模型返回统一 strip()；只有反馈精确等于“无需改进”时才提前停止，
    #    此分支不得调用 Refinement。
    # 3. 其他反馈进入一次 Refinement，并把新稿追加为 execution 记录；本检查点
    #    只生成候选稿，暂不决定它能否覆盖初稿。
    # 4. 返回 initial_draft、initial_checks、feedback、refined_draft、trajectory、
    #    model_call_count、stop_reason 七个字段。提前停止时 refined_draft 为 None，
    #    stop_reason 为 "no_improvement"；完成一次改进时为 "one_iteration_complete"。
    trajectory = []
    # 初稿生成
    initial_prompt = build_initial_prompt(task)
    initial_draft = llm_call(initial_prompt).strip()
    # 初稿硬检查
    trajectory.append({"type": "execution", "content": initial_draft})
    initial_checks = evaluate_draft(initial_draft)
    # 反馈生成
    feedback_prompt = build_reflection_prompt(task, initial_draft, initial_checks)
    feedback = llm_call(feedback_prompt).strip()
    trajectory.append({"type": "reflection", "content": feedback})

    if feedback == "无需改进":
        return {
            "initial_draft": initial_draft,
            "initial_checks": initial_checks,
            "feedback": feedback,
            "refined_draft": None,
            "trajectory": trajectory,
            "model_call_count": 2,
            "stop_reason": "no_improvement",
        }
    # 候选稿生成
    refinement_prompt = build_refinement_prompt(task, initial_draft, feedback)
    refined_draft = llm_call(refinement_prompt).strip()
    trajectory.append({"type": "execution", "content": refined_draft})

    return {
        "initial_draft": initial_draft,
        "initial_checks": initial_checks,
        "feedback": feedback,
        "refined_draft": refined_draft,
        "trajectory": trajectory,
        "model_call_count": 3,
        "stop_reason": "one_iteration_complete",
    }


def select_best_draft(
    initial_draft: str,
    refined_draft: str | None,
) -> dict[str, object]:
    """用同一套硬约束选择最终公告，拒绝不合格候选稿。"""
    # C4：
    # 1. 初稿始终调用 evaluate_draft()；有候选稿时也调用同一个评估器，不能
    #    用模型反馈代替确定性检查。
    # 2. refined_draft 为 None 时保留初稿，refined_checks 为 None，原因记为
    #    "no_refinement"。
    # 3. 候选稿只有在 all_hard_constraints_pass 为 True 时才能被接受；接受时
    #    原因记为 "accepted_hard_constraints_pass"，否则必须回退初稿，原因记为
    #    "rejected_hard_constraints_failed"。
    # 4. 返回 initial_checks、refined_checks、final_draft、accepted_refinement、
    #    decision_reason 五个字段；本检查点不调用模型，也不打印最终报告。
    initial_checks = evaluate_draft(initial_draft)
    if refined_draft is None:
        return {
            "initial_checks": initial_checks,
            "refined_checks": None,
            "final_draft": initial_draft,
            "accepted_refinement": False,
            "decision_reason": "no_refinement",
        }
    refined_checks = evaluate_draft(refined_draft)
    if refined_checks["all_hard_constraints_pass"]:
        return {
            "initial_checks": initial_checks,
            "refined_checks": refined_checks,
            "final_draft": refined_draft,
            "accepted_refinement": True,
            "decision_reason": "accepted_hard_constraints_pass",
        }
    else:
        return {
            "initial_checks": initial_checks,
            "refined_checks": refined_checks,
            "final_draft": initial_draft,
            "accepted_refinement": False,
            "decision_reason": "rejected_hard_constraints_failed",
        }


def run_reflection_writer(
    task: str,
    llm_call: Callable[[str], str],
) -> dict[str, object]:
    """运行一次完整 Reflection Writer，并返回生成与选择证据。"""
    # C5：
    # 1. 只调用一次 run_reflection_once(task, llm_call)，取得初稿、反馈、候选稿、
    #    轨迹、调用次数和停止原因。
    # 2. 把该结果中的 initial_draft、refined_draft 交给 select_best_draft()；
    #    即使候选稿被拒绝，也要保留原候选稿和完整轨迹供审计。
    # 3. 返回 initial_draft、initial_checks、feedback、refined_draft、
    #    refined_checks、final_draft、accepted_refinement、decision_reason、
    #    trajectory、model_call_count、stop_reason 十一个字段。
    # 4. 本检查点不新增模型调用、不连接真实 API，也不打印最终报告。
    reflection_once_result = run_reflection_once(task, llm_call)
    initial_draft = reflection_once_result["initial_draft"]
    refined_draft = reflection_once_result["refined_draft"]
    selection_result = select_best_draft(initial_draft, refined_draft)
    return {
        "initial_draft": initial_draft,  #初稿
        "initial_checks": reflection_once_result["initial_checks"],  #初稿硬检查结果
        "feedback": reflection_once_result["feedback"],  #模型反馈
        "refined_draft": refined_draft,  #候选稿
        "refined_checks": selection_result["refined_checks"],  #候选稿硬检查结果
        "final_draft": selection_result["final_draft"],  #最终稿
        "accepted_refinement": selection_result["accepted_refinement"],  #是否接受候选稿
        "decision_reason": selection_result["decision_reason"],  #决策原因
        "trajectory": reflection_once_result["trajectory"],  #调用轨迹
        "model_call_count": reflection_once_result["model_call_count"],  #模型调用次数
        "stop_reason": reflection_once_result["stop_reason"],  #停止原因
    }


def create_deepseek_llm_call() -> Callable[[str], str]:
    """创建接收单个 prompt、返回正文字符串的真实 DeepSeek 调用函数。"""
    # C6：
    # 1. 先 load_dotenv()，再用 os.environ.get("DEEPSEEK_API_KEY") 读取 key；
    #    key 缺失时抛出不泄露敏感信息的 RuntimeError，绝不能把 key 写进代码。
    # 2. 使用 OpenAI(api_key=..., base_url=DEEPSEEK_BASE_URL) 创建客户端。
    # 3. 返回一个 llm_call(prompt) 闭包；它调用 chat.completions.create()，模型为
    #    DEEPSEEK_MODEL，messages 只含当前 user prompt，stream=False，并显式关闭
    #    thinking，避免推理内容干扰“只输出正文/反馈”的契约。
    # 4. llm_call 返回 choices[0].message.content；内容为 None 时返回空字符串。
    load_dotenv()
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DeepSeek API key is missing.")
    client = OpenAI(api_key=api_key, base_url=os.environ.get("DEEPSEEK_BASE_URL", DEEPSEEK_BASE_URL))

    def llm_call(prompt: str) -> str:
        response = client.chat.completions.create(
            model=os.environ.get("DEEPSEEK_MODEL", DEEPSEEK_MODEL),
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
        )
        content = response.choices[0].message.content
        return content if content is not None else ""

    return llm_call


def main() -> None:
    """真实运行 Reflection Writer，并打印任务要求的完整证据。"""
    # C6：创建真实 llm_call，调用 run_reflection_writer(WRITING_TASK, llm_call)。
    # 依次打印清晰标题与对应内容：初稿、Reflection 反馈、改进候选稿、
    # 同标准对比（两版 checks + accepted_refinement + decision_reason）、最终稿，
    # 最后打印 model_call_count 与 stop_reason；不要打印 API key。
    llm_call = create_deepseek_llm_call()
    result = run_reflection_writer(WRITING_TASK, llm_call)
    print("初稿:\n", result["initial_draft"])
    print("Reflection 反馈:\n", result["feedback"])
    print("改进候选稿:\n", result["refined_draft"])
    print("初稿硬检查结果:\n", result["initial_checks"])
    print("候选稿硬检查结果:\n", result["refined_checks"])
    print("是否接受候选稿:\n", result["accepted_refinement"])
    print("决策原因:\n", result["decision_reason"])
    print("最终稿:\n", result["final_draft"])
    print("调用轨迹:\n", result["trajectory"])
    print("模型调用次数:\n", result["model_call_count"])
    print("停止原因:\n", result["stop_reason"])


if __name__ == "__main__":
    main()
