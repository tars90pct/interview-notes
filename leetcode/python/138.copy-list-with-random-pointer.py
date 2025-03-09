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
        dummy = Node(-1)
        dummy.next = head
        record = {}
        curr = head
        while curr:
            record[curr] = Node(curr.val)
            curr = curr.next
        
        curr = head
        while curr:
            curr_cpoy = record[curr]
            curr_cpoy.next = record.get(curr.next)
            curr_cpoy.random = record.get(curr.random)
            curr = curr.next
        return record.get(dummy.next)

# @lc code=end

