#
# @lc app=leetcode id=216 lang=python3
#
# [216] Combination Sum III
#

# @lc code=start
from typing import List

class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        def backtracking(path, result, current, start):
            path_len = len(path)
            if path_len == k and current == n:
                result.append(path[:])
                return
            if path_len >= k:
                return
            for i in range(start, 10):
                path.append(i)
                current += i
                if current <= n:
                    backtracking(path, result, current, i + 1)
                current -= i
                path.pop()
        result = []
        backtracking([], result, 0, 1)
        return result
        
# @lc code=end

Solution().combinationSum3(3,9)