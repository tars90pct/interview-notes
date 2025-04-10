#
# @lc app=leetcode id=1851 lang=python3
#
# [1851] Minimum Interval to Include Each Query
#

# @lc code=start
import bisect
from heapq import heappop, heappush
from typing import List


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort()
        q = sorted([[qu, i] for i, qu in enumerate(queries)])
        result = [-1] * len(q)
        k = 0
        pq = []
        for i in range(len(q)):
            qu, q_index = q[i]

            while pq and pq[0][2] < qu:
                heappop(pq)
            
            while k < len(intervals) and intervals[k][0] <= qu:
                if intervals[k][1] >= qu:
                    heappush(pq, (intervals[k][1]-intervals[k][0]+1, intervals[k][0], intervals[k][1]))
                k += 1
            
            if pq:
                result[q_index] = pq[0][0]

        return result
# @lc code=end

Solution().minInterval([[1,4],[2,4],[3,6],[4,4]]
,[2,3,4,5]
)