"""W4 数组/哈希新题：存在重复元素。

运行方式：python code/algorithms/w4_02_contains_duplicate.py

任务：如果整数列表中任意数值出现至少两次，返回 True；
否则返回 False。允许空列表。

通过标准：独立实现函数，通过规定与边界测试，并能说明时间和额外空间复杂度。
"""


def contains_duplicate(nums: list[int]) -> bool:
    """判断 nums 中是否存在重复数值。"""
    res={}
    for i, num in enumerate(nums):
        if num in res:
            return True
        res[num] = i
    return False


if __name__ == "__main__":
    assert contains_duplicate([1, 2, 3, 1]) == True, "Test case 1 failed"
    assert contains_duplicate([1, 2, 3, 4]) == False, "Test case 2 failed"
    assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True, "Test case 3 failed"
    assert contains_duplicate([]) == False, "Test case 4 failed"
    assert contains_duplicate([1]) == False, "Test case 5 failed"
    assert contains_duplicate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == False, "Test case 6 failed"
    assert contains_duplicate([-2, -2, 3, 4, 5]) == True, "Test case 7 failed"
    assert contains_duplicate([-2, -1, 0, 1, 2]) == False, "Test case 8 failed"
    print("All test cases passed.")
