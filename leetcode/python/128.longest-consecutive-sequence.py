#
# @lc app=leetcode id=128 lang=python3
#
# [128] Longest Consecutive Sequence
#

# @lc code=start
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0  # Handle empty input case
        
        num_set = set(nums)
        long_seq = 0
        
        for ele in num_set:
            if ele - 1 not in num_set:  # Start of a new sequence
                x = ele
                count = 1
                while x + 1 in num_set:
                    x += 1
                    count += 1
                long_seq = max(long_seq, count)
        
        return long_seq
# @lc code=end

