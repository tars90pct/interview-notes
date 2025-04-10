#
# @lc app=leetcode id=435 lang=python3
#
# [435] Non-overlapping Intervals
#

# @lc code=start
from typing import List

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        if len(intervals) <= 1:
            return 0
        intervals.sort(key=lambda x: x[0])
        result = 0
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i-1][1]:
                result += 1
                intervals[i][1] = min(intervals[i][1], intervals[i-1][1])
        return result
        # if not intervals:
        #     return 0
        # intervals.sort(key=lambda x: x[0])
        # result = 0
        # for i in range(1, len(intervals)):
        #     if intervals[i][0] < intervals[i-1][1]:
        #         result += 1
        #         intervals[i][1] = min(intervals[i][1], intervals[i-1][1])
        # return result
        
# @lc code=end

