#
# @lc app=leetcode id=853 lang=python3
#
# [853] Car Fleet
#

# @lc code=start
from typing import List


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = []
        for i in range(len(position)):
            cars.append((position[i], speed[i]))
        cars.sort(key=lambda x: x[0], reverse=True)
        
        stack = []
        for car in cars:
            time = (target - car[0]) / car[1]
            if stack:
                if stack[-1] < time:
                    stack.append(time)    
            else:
                stack.append(time)
        return len(stack)
# @lc code=end
