#
# @lc app=leetcode id=17 lang=python3
#
# [17] Letter Combinations of a Phone Number
#

# @lc code=start
from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        lookup = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }
        if not digits:
            return []
        def backtracking(path, result, index):
            if len(path) == len(digits):
                result.append(''.join(path))
                return
            letter = lookup[digits[index]]
            for char in letter:
                path.append(char)
                backtracking(path, result, index + 1)
                path.pop()
        result = []
        backtracking([], result, 0)
        return result
# @lc code=end
Solution().letterCombinations("23")
