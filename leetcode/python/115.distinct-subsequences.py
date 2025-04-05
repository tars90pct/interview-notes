#
# @lc app=leetcode id=115 lang=python3
#
# [115] Distinct Subsequences
#

# @lc code=start
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
        for i in range(len(s)+1):
            dp[i][0] = 1
        for j in range(len(t)+1):
            dp[0][j] = 0
        dp[0][0] = 1
        for i in range(1,len(s) + 1):
            for j in range(1,len(t)+1):
                if s[i-1] == t[j-1]:
                    dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
                else:
                    dp[i][j] = dp[i-1][j]
        return dp[-1][-1]
        # dp = [[0] * (len(t) + 1) for _ in range (len(s) + 1)]
        # for i in range(len(dp)):
        #     dp[i][0] = 1
        # for j in range(len(dp[0])):
        #     dp[0][j] = 0
        # dp[0][0] = 1
        # for i in range(1, len(dp)):
        #     for j in range(1, len(dp[i])):
        #         if s[i - 1] == t[j - 1]:
        #             dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
        #         else:
        #             dp[i][j] = dp[i-1][j]
        # return dp[-1][-1]
# @lc code=end

