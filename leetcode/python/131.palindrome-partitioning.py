#
# @lc app=leetcode id=131 lang=python3
#
# [131] Palindrome Partitioning
#

# @lc code=start
from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        def is_palindrome(start, end):
            i = start
            j = end
            while i < j:
                if s[i] != s[j]:
                    return False
                i+=1
                j-=1
            return True
        def backtracking(path, result, start):
            if start == len(s):
                result.append(path[:])
                return
            
            for i in range(start, len(s)):
                if is_palindrome(start, i):
                    path.append(s[start:i+1])
                    backtracking(path, result, i + 1)
                    path.pop()
        result = []
        backtracking([], result, 0)
        return result
# @lc code=end

