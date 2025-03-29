#
# @lc app=leetcode id=875 lang=python3
#
# [875] Koko Eating Bananas
#

# @lc code=start
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l = 1
        r = max(piles)

        def is_possible(k):
            result = 0
            for p in piles:
                result += p // k
                if p % k != 0:
                    result += 1
                if result > h:
                    return False
            return result <= h

        while l <= r:
            mid = (l+r) // 2
            if is_possible(mid):
                r = mid - 1
            else:
                l = mid + 1
        return l

        # def possible(k):
        #     result = 0
        #     for p in piles:
        #         if p % k != 0:
        #             result += 1
        #         result += p // k
        #         if result > h:
        #             return False
        #     return True

        # l = 1
        # r = max(piles)
        # while l <= r:
        #     mid = (l + r) // 2
        #     if possible(mid):
        #         r = mid - 1
        #     else:
        #         l = mid + 1
        # return l
# @lc code=end

