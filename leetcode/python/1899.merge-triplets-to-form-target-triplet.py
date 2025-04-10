#
# @lc app=leetcode id=1899 lang=python3
#
# [1899] Merge Triplets to Form Target Triplet
#

# @lc code=start
class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        good = set()
        for t in triplets:
            if t[0] > target[0] or t[1] > target[1] or t[2] > target[2]:
                continue

            for index, key in enumerate(t):
                if key == target[index]:
                    good.add(index)
        return len(good) == 3




        # good = set()
        # for i in triplets:
        #     if i[0] > target[0] or i[1] > target[1] or i[2] > target[2]:
        #         continue
        #     for index, k in enumerate(i):
        #         if k == target[index]:
        #             good.add(index)
        # return len(good) == 3

# @lc code=end

