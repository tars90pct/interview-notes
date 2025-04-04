#
# @lc app=leetcode id=63 lang=python3
#
# [63] Unique Paths II
#

# @lc code=start

class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        if not obstacleGrid or not obstacleGrid[0] or obstacleGrid[0][0] == 1:
            return 0
        
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        previous = [0] * n
        current = [0] * n
        previous[0] = 1
        
        for i in range(m):
            current[0] = 0 if obstacleGrid[i][0] == 1 else previous[0]
            for j in range(1, n):
                current[j] = 0 if obstacleGrid[i][j] == 1 else current[j-1] + previous[j]
            previous[:] = current
        
        return previous[n-1]
# @lc code=end

