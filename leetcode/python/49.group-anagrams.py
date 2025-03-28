#
# @lc app=leetcode id=49 lang=python3
#
# [49] Group Anagrams
#

# @lc code=start
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        def get_key(s):
            return ''.join(sorted(list(s))) 
        
        lookup = {}
        for s in strs:
            key = get_key(s)
            current = lookup.get(key, [])
            current.append(s)
            lookup[key] = current
        result = []
        for v in lookup.values():
            result.append(v)
        return result

        
# @lc code=end

