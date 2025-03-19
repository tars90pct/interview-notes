#
# @lc app=leetcode id=343 lang=python3
#
# [343] Integer Break
#

# @lc code=start
import math


class Solution:
    def integerBreak(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[0] = 0
        dp[1] = 1
        dp[2] = 1
        for i in range(3, n + 1):
            for j in range(1, i // 2 + 1):
                dp[i] = max(dp[i], j * (i - j), j * dp[i-j])
        return dp[-1]
# @lc code=end

Solution().integerBreak(11)