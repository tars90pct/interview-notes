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
        itinerary = {}
        for t in sorted(tickets, reverse=True):
            itinerary[t[0]] = itinerary.get(t[0], [])
            itinerary[t[0]].append(t[1])
        st = ['JFK']
        result = []
        while st:
            if itinerary.get(st[-1]):
                st.append(itinerary[st[-1]].pop())
            else:
                result.append(st.pop())
        return result[::-1]
        
# @lc code=end

Solution().findItinerary([["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"]])