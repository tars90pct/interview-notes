#
# @lc app=leetcode id=1049 lang=python3
#
# [1049] Last Stone Weight II
#

# @lc code=start
from typing import List


class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        sum_stones = sum(stones)
        half = sum_stones // 2

        dp = [0] * (half + 1)
        for s in stones:
            for j in range(len(dp) - 1, s - 1, -1):
                dp[j] = max(dp[j], dp[j - s] + s)
        return abs(sum_stones - dp[-1] * 2)
        
# @lc code=end

Solution().lastStoneWeightII([2,7,4,1,8,1])