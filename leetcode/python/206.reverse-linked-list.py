#
# @lc app=leetcode id=206 lang=python
#
# [206] Reverse Linked List
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
    def reverseList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        def link(prev, head):
            if head is None:
                return None
            next = head.next
            head.next = prev
            if next is None:
                return head
            return link(head, next)
        
        return link(None, head)
        
# @lc code=end

