#
# @lc app=leetcode id=3272 lang=python3
#
# [3272] Find the Count of Good Integers
#

# @lc code=start
from math import factorial


class Solution:
    def countGoodIntegers(self, n: int, k: int) -> int:
        if n == 1:
            total = 0
            for i in range(1, 10):
                if i % k == 0:
                    total += 1
            return total

        fact = [1]
        for i in range(1, n + 1):
            fact.append(fact[-1] * i)
        
        seen = set()
        ans = 0
        for left in range(10 ** ((n - 1) // 2), 10 ** ((n + 1) //2)):
            l = str(left)
            r = l[::-1]
            if n % 2 == 1:
                r = r[1:]
            t = l + r
           
            if int(t) % k != 0:
                continue

            s = "".join(sorted(list(t)))
            if s in seen:
                continue
            seen.add(s)

            count = Counter(t)

            total = fact[n]
            for key in count.keys():
                total //= fact[count[key]]

            ans += total
            
            
            if count["0"] >= 1:
                total_non_zero = fact[n - 1]
                count["0"] -= 1
                for key in count.keys():
                    total_non_zero //= fact[count[key]]
                ans -= total_non_zero

       

        return ans
                
# @lc code=end
Solution().countGoodIntegers(n = 3, k = 5)
