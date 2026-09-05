"""W5-ALG-R1-F1：两数配对旧题独立复测。

在项目根目录运行：
    ./.venv/Scripts/python.exe code/algorithms/w5_r1_two_sum.py

输入：整数列表 nums 和整数 target；允许空列表、负数、零和重复值。
有解时保证恰好一对有效下标。返回 [i, j]，其中 i < j，
nums[i] + nums[j] == target；无解返回 []；不得修改 nums。

当前任务：独立实现已说明的字典方案，并在本文件的函数外编写至少六条
真实调用 two_sum 的 assert，覆盖非相邻答案、不同位置相同值、
负数或零参与有效配对、单元素、空列表、普通无解。测试数字自行选择。
通过标准：函数和边界测试真实运行通过；后续另在同题中解释复杂度。
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # 保存已经扫描过的数字及其下标
    for i, num in enumerate(nums):
        need = target - num
        if need in seen:
            return [seen[need], i]
        seen[num] = i
    return []


if __name__ == "__main__":

    # 不同位置相同值
    assert two_sum([3, 3], 6) == [0, 1]

    # 负数参与有效配对
    assert two_sum([-1, 2, 3, -5], -6) == [0, 3]

    # 零参与有效配对
    assert two_sum([0, 5, 2], 5) == [0, 1]

    # 单元素
    assert two_sum([5], 10) == []

    # 空列表
    assert two_sum([], 0) == []

    # 普通无解
    assert two_sum([1, 2, 3], 7) == []
