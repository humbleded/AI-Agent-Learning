"""W4 算法回收第 1 题：两数之和。

运行方式：
    .venv/Scripts/python.exe code/algorithms/w4_01_two_sum.py

任务：实现 ``two_sum(nums, target)``，返回两个不同元素的下标 ``[i, j]``。
通过标准：结果满足 ``i < j`` 且两数之和等于 target；能独立说明复杂度，
并用题目给出的三个案例完成断言测试。
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """返回唯一有效数对的两个下标，较小下标在前。"""
    # 先查补数，再保存当前数字，避免重复使用同一个下标。
    lookup = {}
    for i, num in enumerate(nums):
        if target - num in lookup:
            return [lookup[target - num], i]
        lookup[num] = i
    return []


if __name__ == "__main__":
    # 规定案例：普通输入、非相邻答案和重复数字。
    assert two_sum([2, 7, 11, 15], 9) == [0, 1], "Test case 1 failed"
    assert two_sum([3, 2, 4], 6) == [1, 2], "Test case 2 failed"
    assert two_sum([3, 3], 6) == [0, 1], "Test case 3 failed"
    print("All test cases passed.")
