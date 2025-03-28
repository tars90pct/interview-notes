#
# @lc app=leetcode id=1 lang=python3
#
# [1] Two Sum
#

# @lc code=start
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        lookup = {}
        for i in range(len(nums)):
            other = target - nums[i]
            if other in lookup:
                return [lookup[other], i]
            lookup[nums[i]] = i
        return []
# @lc code=end

