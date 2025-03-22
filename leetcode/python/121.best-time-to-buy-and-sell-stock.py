#
# @lc app=leetcode id=121 lang=python3
#
# [121] Best Time to Buy and Sell Stock
#

# @lc code=start
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) == 1:
            return 0
        dp = [[0, 0] for _ in range(len(prices))]
        dp[0][1] = prices[0]
        for i in range(1, len(prices)):
            dp[i][0] = max(prices[i] - dp[i - 1][1], dp[i - 1][0])
            dp[i][1] = min(prices[i], dp[i-1][1])
        return dp[-1][0]
# @lc code=end

Solution().maxProfit([7,1,5,3,6,4])