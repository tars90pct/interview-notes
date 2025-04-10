#
# @lc app=leetcode id=54 lang=python3
#
# [54] Spiral Matrix
#

# @lc code=start
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        moves = [(0,1), (1,0), (0,-1), (-1,0)]
        start = 0
        result = []
        x = 0
        y = 0
        exists = set()
        len_matrix = len(matrix) * len(matrix[0])
        for i in range(len_matrix):
            result.append(matrix[x][y])
            exists.add((x,y))
            new_x = x + moves[start][0]
            new_y = y + moves[start][1]
            if i == len_matrix - 1:
                break
            while new_x < 0 or new_x >= len(matrix) or new_y < 0 or new_y >= len(matrix[0]) or (new_x, new_y) in exists:
                start = (start + 1 ) % 4
                new_x = x + moves[start][0]
                new_y = y + moves[start][1]
            x = new_x
            y = new_y
        return result



        
# @lc code=end

Solution().spiralOrder([[1,2,3],[4,5,6],[7,8,9]]
)