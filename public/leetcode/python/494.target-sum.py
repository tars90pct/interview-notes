#
# @lc app=leetcode id=494 lang=python3
#
# [494] Target Sum
#

# @lc code=start
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        nums_sum = sum(nums)
        if (target + nums_sum) % 2 == 1:
            return 0
        if abs(target) > nums_sum:
            return 0
        amount = (target + nums_sum) // 2
        dp = [0] * (amount + 1)
        dp[0] = 1
        for num in nums:
            for i in range(amount, num -1, -1):
                dp[i] += dp[i - num]
        return dp[-1]

# @lc code=end
Solution().findTargetSumWays([1,1,1,1,1], 3)
