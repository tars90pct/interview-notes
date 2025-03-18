#
# @lc app=leetcode id=860 lang=python3
#
# [860] Lemonade Change
#

# @lc code=start
from typing import List

class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        changes = {
            5: 0,
            10: 0,
            20: 0
        }
        for i in bills:
            if i == 10:
                if changes[5] == 0:
                    return False
                else:
                    changes[5] = changes[5] - 1
            elif i == 20:
                if changes[5] > 0 and changes[10] > 0:
                    changes[5] -= 1
                    changes[10] -= 1
                elif changes[5] > 2:
                    changes[5] -= 3
                else:
                    return False
            changes[i] = changes[i] + 1
        return True
# @lc code=end

Solution().lemonadeChange([5,5,5,10,20])