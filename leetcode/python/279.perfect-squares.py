#
# @lc app=leetcode id=279 lang=python3
#
# [279] Perfect Squares
#

# @lc code=start
import math

class Solution:
    def numSquares(self, n: int) -> int:
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if j * j > i:
                    break
                dp[i] = min(dp[i], dp[i-j] + dp[j], dp[i - j * j] + 1)
        return dp[-1]
# @lc code=end
Solution().numSquares(12)
