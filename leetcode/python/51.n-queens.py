#
# @lc app=leetcode id=51 lang=python3
#
# [51] N-Queens
#

# @lc code=start
from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        chessboard = ['.' * n for _ in range(n)]
        def isValid(row: int, col: int, chessboard: List[str]) -> bool:
            for i in range(row):
                if chessboard[i][col] == 'Q':
                    return False

            i, j = row - 1, col - 1
            while i >= 0 and j >= 0:
                if chessboard[i][j] == 'Q':
                    return False
                i -= 1
                j -= 1

            # 检查 135 度角是否有皇后
            i, j = row - 1, col + 1
            while i >= 0 and j < len(chessboard):
                if chessboard[i][j] == 'Q':
                    return False
                i -= 1
                j += 1
            return True  
        def backtracking(row, chessboard, result):
            if row == n:
                result.append(chessboard[:])
            for col in range(n):
                if isValid(row, col, chessboard):
                    chessboard[row] = chessboard[row][:col] + 'Q' + chessboard[row][col+1:]  # 放置皇后
                    backtracking(row + 1, chessboard, result)
                    chessboard[row] = chessboard[row][:col] + '.' + chessboard[row][col+1:]
            return
        result = []
        backtracking(0, chessboard, result)
        return result
        
# @lc code=end

