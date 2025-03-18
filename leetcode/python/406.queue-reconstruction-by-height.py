#
# @lc app=leetcode id=406 lang=python3
#
# [406] Queue Reconstruction by Height
#

# @lc code=start
from typing import List


class Solution:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        people.sort(key=lambda x: (-x[0], x[1]))
        queue = []
	
        for p in people:
            queue.insert(p[1], p)
        return queue
# @lc code=end

