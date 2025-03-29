#
# @lc app=leetcode id=74 lang=python3
#
# [74] Search a 2D Matrix
#

# @lc code=start
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        l = 0
        r = len(matrix) - 1
        x = l
        while l <= r:
            mid = (l + r) // 2
            if matrix[mid][0] <= target and matrix[mid][-1] >= target:
                x = mid
                break
            elif matrix[mid][0] > target:
                r = mid -1
            else:
                l = mid + 1
        
        l = 0
        r = len(matrix[0]) - 1
        while l <= r:
            mid = (l + r) // 2
            if matrix[x][mid] == target:
                return True
            elif matrix[x][mid] > target:
                r = mid - 1
            else:
                l = mid + 1
        return False


# @lc code=end

