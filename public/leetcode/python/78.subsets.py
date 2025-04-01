#
# @lc app=leetcode id=78 lang=python3
#
# [78] Subsets
#

# @lc code=start
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def backtracking(path, result, start):
            result.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtracking(path, result, i + 1)
                path.remove(nums[i])
        result = []
        backtracking([], result ,0)
        return result
# @lc code=end

Solution().subsets([1,2,3])