#
# @lc app=leetcode id=525 lang=python
#
# [525] Contiguous Array
#

# @lc code=start
class Solution(object):
    def findMaxLength(self, nums):
        history = {}
        sum_val = 0
        max_len = 0
        for i, n in enumerate(nums):
            sum_val += -1 if n == 0 else 1
            if sum_val == 0:
                max_len = i + 1
            elif sum_val in history:
                max_len = max(max_len, i - history[sum_val])
            else:
                history[sum_val] = i
        return max_len
# @lc code=end

