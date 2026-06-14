#- 输入今天学习时长，判断：不足、合格、优秀。
#- 用循环打印未来 7 天学习计划。

def main():
    time = int(input("请输入今天的学习时长（小时）："))
    if time < 2:
        print("学习时长不足，请加油！")
    elif time < 4:
        print("学习时长合格，继续保持！")
    else:
        print("学习时长优秀，太棒了！")

    print("\n未来7天的学习计划：")
    for day in range(1, 8):
        print(f"第{day}天：继续努力学习！")

main()