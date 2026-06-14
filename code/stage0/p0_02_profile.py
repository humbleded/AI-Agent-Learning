#保存姓名、年龄、学习目标、每日学习分钟数，输出一段学习档案

name = input("请输入你的姓名：")
age = int(input("请输入你的年龄："))
goal = input("请输入你的学习目标：")
minutes = float(input("请输入你每天学习的分钟数："))
flag=3>2
print("学习档案：")
print("姓名：" + name)
print(f"年龄：{age}")  
print("学习目标：" + goal)
print(f"每日学习分钟数：{minutes}")
print(f"3>2：{flag}")