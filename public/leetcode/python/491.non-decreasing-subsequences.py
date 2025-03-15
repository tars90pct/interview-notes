#
# @lc app=leetcode id=491 lang=python3
#
# [491] Non-decreasing Subsequences
#

# @lc code=start
from typing import List

class Solution:
    def findSubsequences(self, nums: List[int]) -> List[List[int]]:
        def backtracking(path, result, start):
            if len(path) >= 2:
                if path[-1] >= path[-2]:
                    result.append(path[:])
                else:
                    return
            used = set()
            for i in range(start, len(nums)):
                if nums[i] in used:
                    continue
                used.add(nums[i])
                path.append(nums[i])
                backtracking(path, result, i + 1)
                path.pop()
        result = []
        backtracking([], result, 0)
        return result
        
# @lc code=end
Solution().findSubsequences([4,4,3,2,1])
