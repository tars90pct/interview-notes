#
# @lc app=leetcode id=53 lang=python3
#
# [53] Maximum Subarray
#

# @lc code=start
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        result = float('-inf')
        count = 0
        for i in range(len(nums)):
            count += nums[i]
            if count > result:
                result = count
            if count < 0:
                count = 0
        return result
# @lc code=end

