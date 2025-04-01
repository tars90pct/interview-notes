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
        def isValid(i,j):

        
# @lc code=end

