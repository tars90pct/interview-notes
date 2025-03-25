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
            if i >= len(grid) or i < 0:
                return
            if j >= len(grid[i]) or j < 0:
                return
            if grid[i][j] == -1:
                return
            if grid[i][j] == '0':
                return
            grid[i][j] = -1
            dfs(i - 1, j)
            dfs(i + 1, j)
            dfs(i, j - 1)
            dfs(i, j + 1)
        
        result = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '1':
                    result += 1
                dfs(i, j)
        return result
        
# @lc code=end

