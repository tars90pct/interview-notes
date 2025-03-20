#
# @lc app=leetcode id=135 lang=python3
#
# [135] Candy
#

# @lc code=start
from typing import List

class Solution:
    def candy(self, ratings: List[int]) -> int:
        len_ratings = len(ratings)
        candies = [1] * len_ratings

        for i in range(1, len_ratings):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1
        
        for i in range(len_ratings - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)
        return sum(candies)
# @lc code=end

