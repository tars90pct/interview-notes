#
# @lc app=leetcode id=211 lang=python3
#
# [211] Design Add and Search Words Data Structure
#

# @lc code=start
class WordDictionary:

    def __init__(self):
        self.trie = {}

    def addWord(self, word: str) -> None:
        current = self.trie
        for w in word:
            current[w] = current.get(w, {})
            current = current[w]
        current['end'] = True
        

    def search(self, word: str) -> bool:
        def dfs(current: dict, remain):
            if len(remain) == 0:
                return current.get('end', False)
            if remain[0] == '.':
                for key in current.keys():
                    if key == 'end':
                        continue
                    if dfs(current[key], remain[1:]):
                        return True
                return False
            if remain[0] in current:
                return dfs(current[remain[0]], remain[1:])
            else:
                return False

        if len(word) == 0:
            return True
        return dfs(self.trie, word)
                


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)
# @lc code=end

a = WordDictionary()
a.addWord("at")
a.addWord("and")
a.addWord("an")
a.addWord("add")
a.search("a")

# ["addWord","addWord","addWord","addWord","search","search","addWord","search","search","search","search","search","search"]
# [["at"],["and"],["an"],["add"],["a"],[".at"],["bat"],[".at"],["an."],["a.d."],["b."],["a.d"],["."]]
