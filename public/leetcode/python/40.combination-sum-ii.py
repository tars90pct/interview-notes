#
# @lc app=leetcode id=40 lang=python3
#
# [40] Combination Sum II
#

# @lc code=start
from typing import List

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        def backtracking(path, result, start, current):
            if current == target:
                result.append(path[:])
                return
            if current > target:
                return
            
            for i in range(start, len(candidates)):
                if i > start and candidates[i - 1] == candidates[i]:
                    continue
                path.append(candidates[i])
                current += candidates[i]
                backtracking(path, result, i + 1, current)
                current -= candidates[i]
                path.pop()
        result = []
        backtracking([], result, 0, 0)
        return result
        # candidates = sorted(candidates)
        # def backtracking(path, result, start, current):
        #     if current == target:
        #         result.append(path[:])
        #         return
            
        #     for i in range(start, len(candidates)):
        #         if i > start and candidates[i] == candidates[i - 1]:
        #             continue
        #         if current + candidates[i] > target:
        #             break

        #         path.append(candidates[i])
        #         current += candidates[i]
        #         backtracking(path, result, i + 1, current)
        #         current -= candidates[i]
        #         path.pop()
        # result = []
        # backtracking([], result, 0, 0)
        # return result
# @lc code=end

