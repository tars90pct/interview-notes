#
# @lc app=leetcode id=417 lang=python3
#
# [417] Pacific Atlantic Water Flow
#

# @lc code=start
from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        def dfs(x, y, visited, start):
            if x < 0 or x >= len(heights):
                return
            if y < 0 or y >= len(heights[x]):
                return
            if (x,y) in visited:
                return
            if heights[x][y] < start:
                return
            visited.add((x, y))
            for (i, j) in [
                (x+1, y),
                (x-1, y),
                (x, y+1),
                (x, y-1)
            ]:
                dfs(i, j, visited, heights[x][y])

        pacific = set()
        atlantic = set()
        rows = len(heights)
        cols = len(heights[0])

        for col in range(cols):
            dfs(0, col,pacific, heights[0][col]) #top row
            dfs(rows-1, col, atlantic, heights[rows-1][col]) #bottom row
        
        for row in range(rows):
            dfs(row, 0, pacific,heights[row][0]) #1st col
            dfs(row, cols-1, atlantic, heights[row][cols-1]) 

        return [[r[0], r[1]] for r in atlantic & pacific]
        
# @lc code=end

Solution().pacificAtlantic(
    [
        [19,16,16,12,14,0,17,11,2,0,18,9,13,16,8,8,8,13,17,9,16,9,4,7,1,19,10,7,0,15],
        [0,11,4,14,9,0,6,13,16,5,19,9,4,5,4,12,0,13,0,7,9,12,13,15,3,7,4,9,15,1],
        [13,14,12,12,12,16,6,15,13,1,8,9,11,14,14,10,19,11,10,0,5,18,4,12,7,13,17,15,18,1],
        [16,14,19,5,8,2,11,17,7,1,4,6,5,18,7,15,6,19,18,12,1,14,2,2,0,9,15,14,13,19],
        [17,4,12,9,12,10,12,10,4,5,12,7,2,12,18,10,10,8,6,1,5,13,10,3,5,3,11,4,8,11],
        [8,19,18,9,6,2,7,3,19,6,0,17,9,12,11,1,15,11,18,1,8,11,1,11,16,7,8,17,15,0],
        [7,0,5,11,1,7,12,18,12,1,5,2,11,7,18,12,0,11,9,18,5,2,3,1,1,1,8,14,19,5],
        [2,14,2,16,17,19,10,16,1,16,16,3,19,12,13,17,19,12,16,10,16,8,16,12,6,12,13,17,9,12],
        [8,1,10,5,7,0,15,19,8,15,4,12,18,18,13,11,5,2,8,3,15,4,3,7,7,14,15,11,6,16],
        [0,5,13,19,1,1,2,4,16,2,16,9,15,15,10,10,18,11,17,1,5,14,5,19,7,0,13,7,13,7],
        [11,6,16,12,4,2,9,11,17,19,12,10,6,16,17,5,1,18,19,7,15,1,14,0,3,19,7,3,4,13],
        [4,11,8,10,10,19,7,18,4,2,2,14,6,9,18,14,2,16,5,3,19,17,4,3,7,1,12,2,4,3],
        [14,16,3,11,13,13,6,16,18,0,17,19,4,1,14,12,4,17,5,19,8,13,15,3,15,4,1,14,12,10],
        [13,2,12,2,16,12,19,10,19,12,19,14,12,17,16,3,13,7,3,15,16,7,10,15,14,10,6,5,2,18]
    ]
)