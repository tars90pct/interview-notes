#
# @lc app=leetcode id=475 lang=python3
#
# [475] Heaters
#

# @lc code=start
from typing import List


class Solution:
    def findRadius(self, houses: List[int], heaters: List[int]) -> int:
        def possible(mid):
            heater_pointer = 0
            for i in range(len(houses)):
                h = houses[i] 
                while heater_pointer < len(heaters) and (heaters[heater_pointer] - mid > h or heaters[heater_pointer] + mid < h):
                    heater_pointer += 1
                if heater_pointer == len(heaters):
                    return False
            return True

        houses.sort()
        heaters.sort()
        l = 0
        r = 10e9
        while l <= r:
            mid = (l + r) // 2
            if possible(mid):
                r = mid - 1
            else:
                l = mid + 1
        return int(l)
        
# @lc code=end

Solution().findRadius([1,5],[10])