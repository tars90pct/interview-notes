#
# @lc app=leetcode id=739 lang=python3
#
# [739] Daily Temperatures
#

# @lc code=start
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        result = [0] * len(temperatures)
        for i in range(len(temperatures)):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                result[stack[-1]] = i - stack[-1]
                stack.pop()
            stack.append(i)
        return result
# @lc code=end

