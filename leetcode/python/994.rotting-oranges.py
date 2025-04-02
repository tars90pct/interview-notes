#
# @lc app=leetcode id=994 lang=python3
#
# [994] Rotting Oranges
#

# @lc code=start
from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        result = 0
        fresh = 0
        rotten = deque([])
        exists = set()

        def rot(i, j):
            if i < 0  or i >= len(grid):
                return
            if j < 0 or j >= len(grid[i]):
                return
            if (i, j) in exists:
                return

            nonlocal fresh
            if grid[i][j] == 1:
                grid[i][j] = 2
                rotten.append((i, j))
                fresh -= 1
            exists.add((i, j))            
            
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    fresh += 1
                else:
                    if grid[i][j] == 2:
                        rotten.append((i, j))
                    exists.add((i, j))

        if fresh == 0:
            return 0

        while rotten and fresh > 0:
            result += 1
            for i in range(len(rotten)):
                x, y = rotten.popleft()
                for newX, newY in [
                    (x+1, y),
                    (x-1, y),
                    (x, y+1),
                    (x, y-1)
                ]:
                    rot(newX, newY)
        return result if fresh == 0 else -1

# @lc code=end

Solution().orangesRotting([[2,1,1],[1,1,0],[0,1,1]]
)