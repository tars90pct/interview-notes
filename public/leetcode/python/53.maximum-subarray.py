#
# @lc app=leetcode id=53 lang=python3
#
# [53] Maximum Subarray
#

# @lc code=start
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        result = nums[0]
        if len(nums) == 1:
            return nums[0]
        dp = [0] * len(nums)
        dp[0] = nums[0]
        for i in range(1, len(nums)):
            dp[i] = max(dp[i - 1] + nums[i], nums[i])
            result = max(dp[i], result)
        return result
        # result = float('-inf')
        # count = 0
        # for i in range(len(nums)):
        #     count += nums[i]
        #     if count > result:
        #         result = count
        #     if count < 0:
        #         count = 0
        # return result
# @lc code=end

