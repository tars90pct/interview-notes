#
# @lc app=leetcode id=743 lang=python3
#
# [743] Network Delay Time
#

# @lc code=start
import heapq
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        adj = {i: [] for i in range(1, n+1)}
        network = {i: float('inf') for i in range(1, n+1)}
        for t in times:
            adj[t[0]].append((t[1], t[2]))
        network[k] = 0
        heap = [(0, k)]
        while heap:
            now, cur = heapq.heappop(heap)
            for (next, weight) in adj[cur]:
                new_time = weight + now
                if new_time < network[next]:
                    network[next] = new_time
                    heapq.heappush(heap, (new_time, next))
        result = max(network.values())
        return -1 if result == float('inf') else result
        
# @lc code=end

Solution().networkDelayTime(times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2)