#
# @lc app=leetcode id=1162 lang=python3
#
# [1162] As Far from Land as Possible
#

# @lc code=start
from collections import deque
from typing import List


class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:
        queue = deque([])
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    queue.append((i, j))
        if len(queue) == len(grid) * len(grid[0]):
            return -1
        result = 0
        while queue:
            result +=1
            for _ in range(len(queue)):
                current = queue.popleft()
                (x, y) = current
                for point in [(x+1, y),(x-1, y),(x, y+1),(x, y-1)]:
                    (new_x, new_y) = point
                    if new_x < 0 or new_x >= len(grid):
                        continue
                    if new_y < 0 or new_y >= len(grid[0]):
                        continue
                    if grid[new_x][new_y] == 0:
                        grid[new_x][new_y] = 1
                        queue.append((new_x, new_y))
        return result - 1
# @lc code=end

