#
# @lc app=leetcode id=39 lang=python3
#
# [39] Combination Sum
#

# @lc code=start
from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        def backtracking(path, result, current, start):
            if current == target:
                result.append(path[:])
                return
            if current > target:
                return
            
            for i in range(start, len(candidates)):
                
                path.append(candidates[i])
                current += candidates[i]
                backtracking(path, result, current, i)
                current -= candidates[i]
                path.pop()
        result = []
        backtracking([], result, 0, 0)
        return result

        # def backtracking(path, result, current, start):
        #     if current > target:
        #         return
        #     if current == target:
        #         result.append(path[:])
        #         return
            
        #     for i in range(start, len(candidates)):
        #         path.append(candidates[i])
        #         current += candidates[i]
        #         backtracking(path, result, current, i)
        #         current -= candidates[i]
        #         path.pop()
        # result = []
        # backtracking([], result, 0, 0)
        # return result
        
# @lc code=end

