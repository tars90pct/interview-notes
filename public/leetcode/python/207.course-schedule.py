#
# @lc app=leetcode id=207 lang=python3
#
# [207] Course Schedule
#

# @lc code=start
from collections import deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        courses = {}
        reversed = {}
        for pre in prerequisites:
            current, prev = pre
            courses[current] = courses.get(current, set())
            courses[current].add(prev)
            courses[prev] = courses.get(prev, set())

            reversed[prev] = reversed.get(prev, set())
            reversed[prev].add(current)
        
        dep = deque([])
        for key in courses.keys():
            if len(courses[key]) == 0:
                dep.append(key)

        while dep:
            course = dep.popleft()
            del courses[course]
            prev = reversed.get(course, set())
            for k in prev:
                courses[k].remove(course)
                if len(courses[k]) == 0:
                    dep.append(k)
        return len(courses) == 0
        
        
        
# @lc code=end
Solution().canFinish(4, [[0,1], [1,2], [1,3]])
