#
# @lc app=leetcode id=846 lang=python3
#
# [846] Hand of Straights
#

# @lc code=start
from typing import List


class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False
        counter = {}
        for i in hand:
            freq = counter.get(i, 0)
            counter[i] = freq + 1
        keys = sorted(counter.keys())
        for k in keys:
            if counter.get(k) > 0:
                start_count = counter.get(k)
                for i in range(k, k + groupSize):
                    if counter.get(i, 0) < start_count:
                        return False
                    counter[i] = counter.get(i, 0) - start_count
        return True
# @lc code=end

