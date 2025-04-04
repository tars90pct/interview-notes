#
# @lc app=leetcode id=139 lang=python3
#
# [139] Word Break
#

# @lc code=start
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [False] * (len(s) + 1)
        dp[0] = True
        for i in range(1, len(s) + 1):
            for word in wordDict:
                if i < len(word):
                    continue
                if i == len(word) and s[:i] == word:
                    dp[i] = True
                elif dp[i - len(word)] and s[i - len(word):i] == word:
                    dp[i] = True
        return dp[-1]

        # dp = [False] * (len(s) + 1)
        # dp[0] = True
        # for i in range(1, len(s) + 1):
        #     for word in wordDict:
        #         if i >= len(word):
        #             dp[i] = dp[i] or (dp[i - len(word)] and word == s[i-len(word):i])
        # return dp[-1]
# @lc code=end

Solution().wordBreak("leetcode", ["leet","code"])