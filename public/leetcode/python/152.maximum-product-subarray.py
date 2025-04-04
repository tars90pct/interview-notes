#
# @lc app=leetcode id=152 lang=python3
#
# [152] Maximum Product Subarray
#

# @lc code=start
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        max_val = nums[0]
        min_val = nums[0]
        result = nums[0]
        for i in range(1, len(nums)):
            v = nums[i] * max_val
            max_val = max(nums[i], v, nums[i] * min_val)
            min_val = min(nums[i], v, nums[i] * min_val)
            result = max(max_val, result)
        return result
# @lc code=end

