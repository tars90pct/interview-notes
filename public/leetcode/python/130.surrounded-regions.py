#
# @lc app=leetcode id=130 lang=python3
#
# [130] Surrounded Regions
#

# @lc code=start
from collections import deque


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        queue = deque()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'O':
                    if i == 0 or i == len(board) - 1 or j == 0 or j == len(board[i]) - 1:
                        queue.append((i, j))
                        board[i][j] = 'T'

        while queue:
            (x,y) = queue.popleft()
            for (i, j) in [
                (x+1, y),
                (x-1, y),
                (x, y+1),
                (x, y-1)
            ]:
                if i < 0 or i >= len(board):
                    continue
                if j < 0 or j >= len(board[i]):
                    continue
                if board[i][j] == 'O':
                    queue.append((i, j))
                    board[i][j] = 'T'

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != 'T':
                    board[i][j] = 'X'
                else:
                    board[i][j] = 'O'
# @lc code=end

