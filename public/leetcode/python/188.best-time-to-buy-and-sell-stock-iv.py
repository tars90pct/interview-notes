#
# @lc app=leetcode id=188 lang=python3
#
# [188] Best Time to Buy and Sell Stock IV
#

# @lc code=start
from typing import List


class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        if len(prices) == 0:
            return 0
        dp = [[0] * (2*k +1) for _ in range(len(prices))]
        for i in range(1, 2*k, 2):
            dp[0][i] = -prices[0]
        for i in range(1, len(prices)):
            for j in range(0, 2*k - 1, 2):
                dp[i][j+1] = max(dp[i-1][j+1], dp[i-1][j] - prices[i])
                dp[i][j+2] = max(dp[i-1][j+2], dp[i-1][j+1] + prices[i])
        return dp[-1][2*k]
        # dp = [[0] * (2*k+1) for _ in range(len(prices))]
        # for j in range(1, 2*k, 2):
        #     dp[0][j] = -prices[0]
        # for i in range(1, len(prices)):
        #     for j in range(0, 2*k-1, 2):
        #         dp[i][j+1] = max(dp[i-1][j+1], dp[i-1][j] - prices[i])
        #         dp[i][j+2] = max(dp[i-1][j+2], dp[i-1][j+1] + prices[i])
        # return dp[-1][2*k]
# @lc code=end

