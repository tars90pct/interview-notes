#
# @lc app=leetcode id=36 lang=python3
#
# [36] Valid Sudoku
#

# @lc code=start
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        result = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                element = board[i][j]
                if element != '.':
                    result.append((i, element))
                    result.append((element, j))
                    result.append((i // 3, j // 3, element))
        return len(result) == len(set(result))
# @lc code=end

