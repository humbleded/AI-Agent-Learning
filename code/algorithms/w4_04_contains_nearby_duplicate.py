"""W4 数组/哈希第 4 道新题：存在相近的重复元素。

运行方式：
    .venv/Scripts/python.exe code/algorithms/w4_04_contains_nearby_duplicate.py

任务：实现 ``contains_nearby_duplicate(nums, k)``。当存在两个不同下标
``i``、``j``，同时满足 ``nums[i] == nums[j]`` 且 ``abs(i - j) <= k``
时返回 ``True``，否则返回 ``False``。

通过标准：不修改输入列表；平均时间复杂度为 O(n)，额外空间至多 O(n)；
通过下方全部规定断言，并能解释循环量、哈希操作与容器空间上限。
"""


def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    """判断 nums 中是否存在下标距离不超过 k 的相同数值。"""
    res={}
    for i, num in enumerate(nums):
        if num in res and i - res[num] <= k:
            return True
        res[num] = i
    return False


if __name__ == "__main__":
    assert contains_nearby_duplicate([1, 2, 3, 1], 3) is True
    assert contains_nearby_duplicate([1, 0, 1, 1], 1) is True
    assert contains_nearby_duplicate([1, 2, 3, 1, 2, 3], 2) is False
    assert contains_nearby_duplicate([], 3) is False
    assert contains_nearby_duplicate([1], 1) is False
    assert contains_nearby_duplicate([1, 1], 0) is False
    assert contains_nearby_duplicate([-1, 2, -1], 2) is True
    assert contains_nearby_duplicate([1, 2, 1, 1], 1) is True
    print("All test cases passed.")
