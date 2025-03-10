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
            return head
        lookup = {}
        curr = head
        while curr:
            lookup[curr] = Node(curr.val)
            curr = curr.next
        
        curr = head
        while curr:
            node = lookup.get(curr)
            node.next = lookup.get(curr.next)
            node.random = lookup.get(curr.random)
            curr = curr.next
        
        return lookup.get(head)
# @lc code=end

