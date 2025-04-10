#
# @lc app=leetcode id=48 lang=python3
#
# [48] Rotate Image
#

# @lc code=start
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        edge = len(matrix)
        top = 0
        bottom = edge - 1
        while top < bottom:
            for col in range(edge):
                temp = matrix[top][col]
                matrix[top][col] = matrix[bottom][col]
                matrix[bottom][col] = temp
            top += 1
            bottom -= 1
        
        for i in range(edge):
            for j in range(i + 1, edge):
                temp = matrix[i][j]
                matrix[i][j] = matrix[j][i]
                matrix[j][i] = temp
        return matrix
        # edge = len(matrix)
        # top = 0
        # bottom = edge - 1
        # while top < bottom:
        #     for col in range(edge):
        #         temp = matrix[top][col]
        #         matrix[top][col] = matrix[bottom][col]
        #         matrix[bottom][col] = temp
        #     top += 1
        #     bottom -= 1
        # for row in range(edge):
        #     for col in range(row+1, edge):
        #         temp = matrix[row][col]
        #         matrix[row][col] = matrix[col][row]
        #         matrix[col][row] = temp
        # return matrix

# @lc code=end
Solution().rotate([[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]])
