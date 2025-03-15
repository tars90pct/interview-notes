#
# @lc app=leetcode id=77 lang=python3
#
# [77] Combinations
#

# @lc code=start
from collections import deque
from typing import List


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        result = []
        def backtracking(path, result, start):
            path_len = len(path)
            if path_len == k:
                result.append(path[:])
                return
            for i in range(start, n - (k - path_len) + 2):
                path.append(i)
                backtracking(path, result, i + 1)
                path.pop()
        backtracking([], result, 1)
        return result
                
# @lc code=end
Solution().combine(4, 2)
