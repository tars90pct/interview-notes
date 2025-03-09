#
# @lc app=leetcode id=86 lang=python
#
# [86] Partition List
#

class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# @lc code=start
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def partition(self, head, x):
        """
        :type head: Optional[ListNode]
        :type x: int
        :rtype: Optional[ListNode]
        """
        lessHead = ListNode()
        greaterHead = ListNode()
        less = lessHead
        greater = greaterHead
        curr = head
        while curr:
            if curr.val < x:
                less.next = curr
                less = curr
            else:
                greater.next = curr
                greater = curr
            curr = curr.next
        greater.next = None
        less.next = greaterHead.next
        return lessHead.next
# @lc code=end

