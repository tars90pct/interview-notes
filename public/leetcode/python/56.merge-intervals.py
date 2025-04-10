#
# @lc app=leetcode id=56 lang=python3
#
# [56] Merge Intervals
#

# @lc code=start
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) <= 1:
            return intervals
        intervals.sort(key=lambda x: x[0])
        result = [intervals[0]]
        for i in range(1, len(intervals)):
            if intervals[i][0] <= result[-1][1]:
                result[-1][1] = max(intervals[i][1], result[-1][1])
            else:
                result.append(intervals[i])
        return result

        # if len(intervals) <= 1:
        #     return intervals
        # intervals.sort(key=lambda x: x[0])
        # result = [intervals[0]]
        # for i in range(1, len(intervals)):
        #     if intervals[i][0] <= result[-1][1]:
        #         result[-1][1] = max(intervals[i][1], result[-1][1])
        #     else:
        #         result.append(intervals[i])
        # return result
        
# @lc code=end

Solution().merge([[1,4],[0,2],[3,5]]
)