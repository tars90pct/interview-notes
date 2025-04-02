#
# @lc app=leetcode id=210 lang=python3
#
# [210] Course Schedule II
#

# @lc code=start
from collections import deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        courses = {}
        depends = {}
        for i in range(numCourses):
            courses[i] = set()
            depends[i] = set()
        for pre in prerequisites:
            current, pre = pre
            courses[current].add(pre)
            depends[pre].add(current)

        queue = deque()
        result = []
        for key in courses.keys():
            if len(courses[key]) == 0:
                queue.append(key)
        while queue:
            free = queue.popleft()
            result.append(free)
            del courses[free]
            for next in depends.get(free, set()):
                courses[next].remove(free)
                if len(courses[next]) == 0:
                    queue.append(next)
        
        return result if len(courses) == 0 else []
        
# @lc code=end

