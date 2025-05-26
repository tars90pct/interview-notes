#
# @lc app=leetcode id=127 lang=python3
#
# [127] Word Ladder
#

# @lc code=start
from collections import defaultdict, deque
from typing import List


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList or not endWord or not beginWord or not wordList:
            return 0
        len_w = len(beginWord)
        cache = defaultdict(list)
        for word in wordList:
            for i in range(len_w):
                key = word[:i] + '*' + word[i+1:]
                cache[key] = word
        visited = set()
        queue = deque([(beginWord, 1)])
        visited.add(beginWord)
        while queue:
            current, level = queue.popleft()
            for i in range(len_w):
                key = current[:i] + '*' + current[i+1:]
                for word in cache[key]:
                    if word == endWord:
                        return level + 1
                    visited.add(word)
                    queue.append((word, level + 1))
        return 0
# @lc code=end

Solution().ladderLength(beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"])