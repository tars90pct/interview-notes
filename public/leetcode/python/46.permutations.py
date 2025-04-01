#
# @lc app=leetcode id=46 lang=python3
#
# [46] Permutations
#

# @lc code=start
from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def backtracking(path, result, used: set):
            if len(path) == len(nums):
                result.append(path[:])
                return 
            
            for i in range(len(nums)):
                if i in used:
                    continue
                used.add(i)
                path.append(nums[i])
                backtracking(path, result, used)
                path.pop()
                used.remove(i)

        result = []
        backtracking([], result, set())
        return result
        # def backtracking(path, result, used):
        #     if len(path) == len(nums):
        #         result.append(path[:])
        #         return
            
        #     for i in range(0, len(nums)):
        #         if nums[i] in used:
        #             continue
        #         used.add(nums[i])
        #         path.append(nums[i])
        #         backtracking(path, result, used)
        #         path.pop()
        #         used.remove(nums[i])
        # result = []
        # backtracking([], result, set())
        # return result
                
        
# @lc code=end
Solution().permute([1,2,3])

