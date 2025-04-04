#
# @lc app=leetcode id=5 lang=python3
#
# [5] Longest Palindromic Substring
#

# @lc code=start
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        longest = s[0]
        for i in range(n, -1, -1):
            for j in range(i, n):
                substring = s[i:j+1]
                if len(substring) == 1:
                    dp[i][j] = True
                elif s[i] == s[j]:
                    if len(substring) == 2:
                        dp[i][j] = True
                    else:
                        dp[i][j] = dp[i+1][j-1]
                if dp[i][j] == True:
                    if len(longest) < j - i + 1:
                        longest = s[i:j+1]
        return longest
                    
# @lc code=end

Solution().longestPalindrome("cbbd")

