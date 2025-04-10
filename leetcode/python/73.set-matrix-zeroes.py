#
# @lc app=leetcode id=73 lang=python3
#
# [73] Set Matrix Zeroes
#

# @lc code=start
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    for r in range(len(matrix[i])):
                        if matrix[i][r] != 0:
                            matrix[i][r] = '0'
                    for c in range(len(matrix)):
                        if matrix[c][j] != 0:
                            matrix[c][j] = '0'
        
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == '0':
                    matrix[i][j] = 0
        return matrix
        
# @lc code=end

Solution().setZeroes([[0,1,2,0],[3,4,5,2],[1,3,1,5]]
)