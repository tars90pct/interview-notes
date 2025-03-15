#
# @lc app=leetcode id=332 lang=python3
#
# [332] Reconstruct Itinerary
#

# @lc code=start
from collections import defaultdict
from typing import List

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        targets = defaultdict(list)
        for ticket in tickets:
            targets[ticket[0]].append(ticket[1]) 
        
        for key in targets:
            targets[key].sort(reverse=True)
        
        result = []
        def backtracking(airport, targets, result):
            while targets[airport]:
                next_airport = targets[airport].pop()  # 弹出下一个机场
                backtracking(next_airport, targets, result)  # 递归调用回溯函数进行深度优先搜索
            result.append(airport)
        backtracking("JFK", targets, result)
        return result[::-1]
        
# @lc code=end

Solution().findItinerary([["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"]])