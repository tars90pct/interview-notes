#
# @lc app=leetcode id=647 lang=python3
#
# [647] Palindromic Substrings
#

# @lc code=start
class Solution:
    def countSubstrings(self, s: str) -> int:
        dp = [[False] * len(s) for _ in range(len(s))]
        result = 0
        for i in range(len(s) - 1, -1, -1):
            for j in range(i, len(s)):
                if s[i] == s[j]:
                    if j - i <= 1:
                        dp[i][j] = True
                    else:
                        dp[i][j] = dp[i+1][j-1]
                if dp[i][j] == True:
                    result += 1
        return result
        # dp = [[False] * len(s) for _ in range(len(s))]
        # result = 0
        # for i in range(len(s)-1, -1, -1):
        #     for j in range(i, len(s)):
        #         if s[i] == s[j]:
        #             if j - i <= 1:
        #                 dp[i][j] = True
        #                 result += 1
        #             elif dp[i + 1][j - 1]:
        #                 result += 1
        #                 dp[i][j] = True        
        # return result


# @lc code=end

