#
# @lc app=leetcode id=70 lang=python3
#
# [70] Climbing Stairs
#

# @lc code=start
class Solution:
    def climbStairs(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[0] = 1
        for j in range(1, n + 1):
            for num in [1, 2]:
                if j >= num:
                    dp[j] += dp[j-num]
        return dp[-1]
        
# @lc code=end

