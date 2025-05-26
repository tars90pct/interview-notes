#
# @lc app=leetcode id=1970 lang=python3
#
# [1970] Last Day Where You Can Still Cross
#

# @lc code=start
from collections import defaultdict
from typing import List


class Solution:
    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        def find(node):
            if root[node] != node:
                root[node] = find(root[node])
            return root[node]
        def union(x,y):
            root_x = find(x)
            root_y = find(y)
            root[root_x] = root_y
        def index(x,y):
            return 1 + x * col + y
        moves = [(1,0),(0,1),(-1,0),(0,-1)]
        root = [i for i in range(row * col + 2)]
        grid = [[1] * col for _ in range(row)]
        
        cells = [[x-1,y-1] for [x,y] in cells]
        for i in range(len(cells) - 1, -1, -1):
            x, y = cells[i]
            grid[x][y] = 0
            currentIdx = index(x, y)
            for dx, dy in moves:
                if x + dx >= 0 and x + dx < row and y + dy >= 0 and y + dy < col and  grid[x + dx][y + dy] == 0:
                    ind = index(x+dx, y+dy)
                    union(ind, currentIdx)
            if x == 0:
                union(0, currentIdx)
            if x == row - 1:
                union(row*col + 1, currentIdx)
            if find(0) == find(col*row+1):
                return i



# @lc code=end


[[1,2,5],[2,3,8],[1,5,1]]
g = defaultdict(list)
for x,y,t in [[1,2,5],[2,3,8],[1,5,1]]:
    g[t].append((x,y))

for k,v in sorted(g.items()):
    print(k)