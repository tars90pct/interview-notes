#
# @lc app=leetcode id=239 lang=python3
#
# [239] Sliding Window Maximum
#

# @lc code=start
from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        q = deque()

        for i in range(len(nums)):
            while q and q[-1] < nums[i]:
                q.pop()
            q.append(nums[i])

            if i >= k and q[0] == nums[i - k]:
                q.popleft()
            if i >= k - 1:
                res.append(q[0])
        return res
# @lc code=end

