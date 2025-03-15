#
# @lc app=leetcode id=90 lang=python3
#
# [90] Subsets II
#

# @lc code=start
from typing import List

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        def backtracking(path, result, start):
            result.append(path[:])
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

