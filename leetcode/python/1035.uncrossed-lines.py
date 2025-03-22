#
# @lc app=leetcode id=1035 lang=python3
#
# [1035] Uncrossed Lines
#

# @lc code=start
from typing import List

class Solution:
    def maxUncrossedLines(self, nums1: List[int], nums2: List[int]) -> int:
        dp = [[0] * (len(nums2) + 1) for _ in range(len(nums1) + 1)]
        result = 0
        for i in range(1, len(dp)): # text1
            for j in range(1, len(dp[i])): # text2
                if nums1[i - 1] == nums2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    result = max(result, dp[i][j])
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return result

# @lc code=end

