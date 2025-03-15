#
# @lc app=leetcode id=37 lang=python3
#
# [37] Sudoku Solver
#

# @lc code=start
from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        row_used = [set() for _ in range(9)]
        col_used = [set() for _ in range(9)]
        box_used = [set() for _ in range(9)]
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num == ".":
                    continue
                row_used[row].add(num)
                col_used[col].add(num)
                box_used[(row // 3) * 3 + col // 3].add(num)
        
# @lc code=end
Solution().solveSudoku([["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]])
