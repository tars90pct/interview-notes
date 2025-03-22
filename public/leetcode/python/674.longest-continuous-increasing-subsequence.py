#
# @lc app=leetcode id=674 lang=python3
#
# [674] Longest Continuous Increasing Subsequence
#

# @lc code=start
class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        dp = [1] * len(nums)
        result = 1
        for i in range(1, len(dp)):
            if nums[i] > nums[i-1]:
                dp[i] = dp[i - 1] + 1
                result = max(result, dp[i])
        return result

# @lc code=end

