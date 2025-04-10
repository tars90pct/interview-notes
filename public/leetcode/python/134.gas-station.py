#
# @lc app=leetcode id=134 lang=python3
#
# [134] Gas Station
#

# @lc code=start
from typing import List

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        start = 0
        current = 0
        total = 0
        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            current += diff
            total += diff
            if current < 0:
                start = i + 1
                current = 0
        if total < 0:
            return -1
        return start
        # curr = 0
        # total = 0
        # start = 0
        # for i in range(len(gas)):
        #     diff = gas[i] - cost[i]
        #     curr += diff
        #     total += diff
        #     if curr < 0:
        #         curr = 0
        #         start = i + 1
        # if total < 0:
        #     return -1
        # return start
        
# @lc code=end

