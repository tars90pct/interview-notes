#
# @lc app=leetcode id=347 lang=python3
#
# [347] Top K Frequent Elements
#

# @lc code=start
import heapq
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        lookup = {}
        for i in nums:
            lookup[i] = lookup.get(i, 0) + 1

        heap = []
        for i in lookup.keys():
            heapq.heappush(heap, (lookup.get(i) * -1, i))
        
        result = []
        for i in range(k):
            item = heapq.heappop(heap)
            result.append(item[1])
        return result

# @lc code=end

