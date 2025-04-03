#
# @lc app=leetcode id=1584 lang=python3
#
# [1584] Min Cost to Connect All Points
#

# @lc code=start
import heapq
from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        min_cost = 0
        pq = [(0,0)]
        visited = [False for i in points]
        cache = {}
        while pq:
            cost, curr = heapq.heappop(pq)

            if visited[curr]:
                continue

            visited[curr] = True
            min_cost += cost
            for i in range(len(points)):
                if visited[i]:
                    continue
                dist = abs(points[curr][0] -  points[i][0]) + abs(points[curr][1] -  points[i][1])
                if dist < cache.get(i, dist + 1):
                    cache[i] = dist
                    heapq.heappush(pq, (dist, i))
        return min_cost


# @lc code=end

