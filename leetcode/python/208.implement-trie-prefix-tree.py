#
# @lc app=leetcode id=208 lang=python3
#
# [208] Implement Trie (Prefix Tree)
#

# @lc code=start
class Trie:

    def __init__(self):
        self.trie = {}

    def insert(self, word: str) -> None:
        current = self.trie
        for w in word:
            current[w] = current.get(w, {})
            current = current[w]
        current['end'] = True

    def search(self, word: str) -> bool:
        current = self.trie
        for w in word:
            if w in current:
                current = current[w]
            else:
                return False
        return 'end' in current

    def startsWith(self, prefix: str) -> bool:
        current = self.trie
        for w in prefix:
            if w in current:
                current = current[w]
            else:
                return False
        return True
        


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
# @lc code=end

