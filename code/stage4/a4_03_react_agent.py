"""
A4-03 ReAct Agent。

运行：
    python code/stage4/a4_03_react_agent.py

任务：
    1. 展示 Thought/Action/Observation。
    2. 至少调用一个工具。
    3. 设置 max_steps，防止无限循环。
"""


def search_tool(query):
    return f"模拟搜索结果：{query} 相关资料 3 条"


def react_loop(question, max_steps=3):
    trace = []
    for step in range(1, max_steps + 1):
        thought = f"第 {step} 步：判断是否需要工具"
        action = {"tool": "search", "query": question}
        observation = search_tool(question)
        trace.append((thought, action, observation))
        break
    answer = f"根据 observation 回答：{observation}"
    return trace, answer


def main():
    question = input("问题：").strip()
    trace, answer = react_loop(question)
    for thought, action, observation in trace:
        print("Thought:", thought)
        print("Action:", action)
        print("Observation:", observation)
    print("Final:", answer)


if __name__ == "__main__":
    main()
