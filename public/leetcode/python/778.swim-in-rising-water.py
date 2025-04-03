#
# @lc app=leetcode id=778 lang=python3
#
# [778] Swim in Rising Water
#

# @lc code=start
import heapq


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        visited = set()
        pq = [(grid[0][0], 0, 0)]
        visited.add((0,0))
        while pq:
            t, r, c = heapq.heappop(pq)
            if r == n - 1 and c == n - 1:
                return t
            for x,y in [
                [r+1, c],
                [r-1, c],
                [r, c+1],
                [r, c-1],
            ]:
                if x >= 0 and x < n and y >= 0 and y < n:
                    if (x,y) not in visited:
                        visited.add((x,y))
                        heapq.heappush(pq, (
                            max(t, grid[x][y]),
                            x,
                            y
                        ))
        
# @lc code=end

