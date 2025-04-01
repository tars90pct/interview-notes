#
# @lc app=leetcode id=1046 lang=python3
#
# [1046] Last Stone Weight
#

# @lc code=start
import heapq
from typing import List


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = []
        for i in stones:
            heapq.heappush(heap, i * -1)
        while len(heap) > 1:
            l = heapq.heappop(heap)
            r = heapq.heappop(heap)
            mid = abs(l-r)
            if mid != 0:
                heapq.heappush(heap, mid * -1)
        return 0 if len(heap) == 0 else heap[0] * -1
            
# @lc code=end

