#
# @lc app=leetcode id=138 lang=python
#
# [138] Copy List with Random Pointer
#

class Node:
    def __init__(self, x, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random

# @lc code=start
"""
# Definition for a Node.
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random
"""
class Solution(object):
    def copyRandomList(self, head):
        """
        :type head: Node
        :rtype: Node
        """
        if head is None:
            return None
        lookup = {}
        current = head
        while current:
            lookup[current] = Node(
                current.val
            )
            current = current.next
        current = head
        while current:
            node = lookup[current]
            if current.next:
                node.next = lookup[current.next]
            if current.random:
                node.random = lookup[current.random]
            current = current.next
        return lookup.get(head)
# @lc code=end

