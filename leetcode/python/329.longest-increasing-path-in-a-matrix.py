#
# @lc app=leetcode id=329 lang=python3
#
# [329] Longest Increasing Path in a Matrix
#

# @lc code=start
from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        dp = [[-1] * len(matrix[i]) for i in range(len(matrix))]
        result = 1
        def dfs(i, j):
            if dp[i][j] != -1:
                return dp[i][j]
            current = matrix[i][j]
            for x, y in [
                [i+1,j],
                [i-1,j],
                [i,j+1],
                [i,j-1],
            ]:
                if x >= 0 and x < len(dp) and y >= 0 and y < len(dp[x]):
                    if current > matrix[x][y]:
                        dp[i][j] = max(dp[i][j], dfs(x,y)+1)
                        nonlocal result
                        result = max(result, dp[i][j])
            if dp[i][j] == -1:
                dp[i][j] = 1
            return dp[i][j]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                dfs(i, j)
        return result
                        

        
# @lc code=end
Solution().longestIncreasingPath([[3,4,5],[3,2,6],[2,2,1]])
