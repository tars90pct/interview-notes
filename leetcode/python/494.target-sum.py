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
        target_nums_sum = nums_sum + target
        if target_nums_sum % 2 == 1:
            return 0
        if abs(target) > nums_sum:
            return 0
        weight = target_nums_sum // 2
        dp = [0] * (weight + 1)
        dp[0] = 1
        for num in nums:
            for j in range(weight, num - 1, -1):
                dp[j] += dp[j - num]
        return dp[-1]

# @lc code=end
Solution().findTargetSumWays([1,1,1,1,1], 3)
