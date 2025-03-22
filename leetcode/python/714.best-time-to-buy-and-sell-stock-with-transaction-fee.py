#
# @lc app=leetcode id=714 lang=python3
#
# [714] Best Time to Buy and Sell Stock with Transaction Fee
#

# @lc code=start
class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        hold = -prices[0]
        not_hold = 0
        for i in range(1, len(prices)):
            hold = max(hold, not_hold - prices[i])
            not_hold = max(not_hold, hold + prices[i] - fee)
        return not_hold
# @lc code=end

