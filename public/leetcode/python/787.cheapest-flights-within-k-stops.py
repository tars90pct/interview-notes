#
# @lc app=leetcode id=787 lang=python3
#
# [787] Cheapest Flights Within K Stops
#

# @lc code=start
from collections import defaultdict
import heapq


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        graph = defaultdict(list)
        for frm, to, price in flights:
            graph[frm].append((to, price))
        visited = {}
        pq = [(0, 0, src)]
        while pq:
            price, stop, city = heapq.heappop(pq)
            if stop > k + 1:
                continue
            if city == dst:
                return price
            if city in visited and visited[city]==stop:
                continue
            visited[city] = stop
            for nei,p in graph[city]:
                if nei not in visited or visited[nei]>stop:
                    heapq.heappush(pq,(price+p,stop+1,nei))
        return -1
        # while heap:
        #     price,stops,city = heapq.heappop(heap)

        #     if stops>k+1:
        #         continue
            
        #     if city==dst:
        #         return price

        #     if city in visited and visited[city]==stops:
        #         continue

        #     visited[city] = stops

        #     for nei,p in graph[city]:
        #         if nei not in visited or visited[nei]>stops:
        #             heapq.heappush(heap,(price+p,stops+1,nei))

        # return -1
# @lc code=end

