#
# @lc app=leetcode id=200 lang=python3
#
# [200] Number of Islands
#

# @lc code=start
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def dfs(i, j):
            if i < 0 or i >= len(grid):
                return
            if j < 0 or j >= len(grid[i]):
                return
            if grid[i][j] == '0':
                return

            grid[i][j] = '0'
            for loc in [
                (i + 1, j),
                (i - 1, j),
                (i, j + 1),
                (i, j - 1)
            ]:
                dfs(loc[0], loc[1])
        result = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '1':
                    dfs(i, j)
                    result += 1
        return result
        
# @lc code=end
Solution().numIslands(
    [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
        ])
