"""W4 算法回收第 3 题：有效的字母异位词。

运行方式：
    .venv/Scripts/python.exe code/algorithms/w4_03_valid_anagram.py

任务：实现 ``is_anagram(s, t)``。两个字符串只包含小写英文字母；当且仅当
二者包含的字符及每个字符的出现次数完全相同时返回 ``True``。

通过标准：独立说明思路，完成函数，加入覆盖关键边界的可重复断言测试，
并正确说明时间复杂度与额外空间复杂度。
"""


def is_anagram(s: str, t: str) -> bool:
    """判断 s 和 t 是否互为字母异位词。"""
    if len(s) != len(t):
        return False
    count = {}
    count1 = {}
    for char in s:
        count[char] = count.get(char, 0) + 1
    for char in t:
        count1[char] = count1.get(char, 0) + 1
    return count == count1

    # 排序后比较
def is_anagram_sort(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)



if __name__ == "__main__":
    # TODO: 添加至少 6 个断言并在全部通过后打印成功消息。
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False
    assert is_anagram("", "") is True
    assert is_anagram("a", "a") is True
    assert is_anagram("ab", "ba") is True
    assert is_anagram("abc", "cba") is True
    assert is_anagram("aacc", "ccac") is False
    assert is_anagram("abcaa", "def") is False
    print("All tests passed.")
