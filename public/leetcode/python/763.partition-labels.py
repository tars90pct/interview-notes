#
# @lc app=leetcode id=763 lang=python3
#
# [763] Partition Labels
#

# @lc code=start
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        right_most = {}
        for i in range(len(s)):
            right_most[s[i]] = i
        
        result = []
        left = 0
        right = 0
        for i in range(len(s)):
            right = max(right, right_most[s[i]])
            if right == i:
                result.append(right - left + 1)
                left = i + 1
        return result
# @lc code=end

