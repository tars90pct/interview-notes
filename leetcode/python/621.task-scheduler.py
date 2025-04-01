#
# @lc app=leetcode id=621 lang=python3
#
# [621] Task Scheduler
#

# @lc code=start
from collections import deque
import heapq
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        freq = {}
        for task in tasks:
            freq[task] = freq.get(task, 0) + 1
        heap = []
        for v in freq.values():
            heapq.heappush(heap, -v)
        
        cooldown = deque([])
        timer = 0
        while heap or cooldown:
            if len(heap) > 0:
                task = -heapq.heappop(heap)
                if task > 1:
                    cooldown.append((task - 1, timer + n + 1))
            timer += 1
            while cooldown and cooldown[0][1] == timer:
                task, _ = cooldown.popleft()
                heapq.heappush(heap, -task)
        return timer
        # while heap or cooldown:
        #     if heap:
        #         task = -heapq.heappop(heap)
        #         if task > 1:
        #             cooldown.append((task-1, timer+n+1))
        #     timer+=1
        #     while cooldown and cooldown[0][1] == timer:
        #         task_count, _ = cooldown.popleft()
        #         heapq.heappush(heap, -task_count)
        # return timer
        
# @lc code=end

