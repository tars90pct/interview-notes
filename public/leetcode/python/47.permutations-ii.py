#
# @lc app=leetcode id=47 lang=python3
#
# [47] Permutations II
#

# @lc code=start
from typing import List

class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        def backtracking(path, result, index_used: set):
            if len(path) == len(nums):
                result.append(path[:])
                return
            
            value_used = set()
            for i in range(0, len(nums)):
                if i in index_used:
                    continue
                if nums[i] in value_used:
                    continue
                value_used.add(nums[i])
                path.append(nums[i])
                index_used.add(i)
                backtracking(path, result, index_used)
                index_used.remove(i)
                path.pop()
        result = []
        backtracking([], result, set())
        return result
# @lc code=end

Solution().permuteUnique([1,2,3])