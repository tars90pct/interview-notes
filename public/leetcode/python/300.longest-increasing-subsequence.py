#
# @lc app=leetcode id=300 lang=python3
#
# [300] Longest Increasing Subsequence
#

# @lc code=start
from typing import List

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1] * len(nums)
        result = 1
        for i in range(1, len(nums)):
            for j in range(0, i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
                result = max(result, dp[i])
        return result
        # dp = [1] * len(nums) 
        # result = 1
        # for i in range(1, len(dp)):
        #     for j in range(0, i):
        #         if nums[i] > nums[j]:
        #             dp[i] = max(dp[i], dp[j] + 1)
        #     result = max(result, dp[i])
        # return result
# @lc code=end

Solution().lengthOfLIS([10,9,2,5,3,7,101,18])