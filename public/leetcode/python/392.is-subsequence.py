#
# @lc app=leetcode id=392 lang=python3
#
# [392] Is Subsequence
#

# @lc code=start
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
        result = 0
        for i in range(1, len(s) + 1):
            for j in range(1, len(t) + 1):
                if s[i - 1] == t[j - 1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    result = max(result, dp[i][j])
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return result == len(s)
# @lc code=end

