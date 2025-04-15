#
# @lc app=leetcode id=394 lang=python3
#
# [394] Decode String
#

# @lc code=start
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        current = ''
        for c in s:
            if c.isdigit():
                current += c
                continue
            if current != '':
                stack.append(current)
                current = ''
            if c == ']':
                chars = ''
                while stack:
                    c = stack.pop()
                    if c == '[':
                        break
                    chars = c + chars
                d = int(stack.pop())
                stack.append(chars * d)
                continue
            stack.append(c)
        return ''.join(stack)
# @lc code=end

Solution().decodeString('3[a]2[bc]')