#
# @lc app=leetcode id=83 lang=python
#
# [83] Remove Duplicates from Sorted List
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
    def deleteDuplicates(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        dummy = ListNode()
        dummy.next = head
        prev = dummy
        curr = head
        while curr:
            while curr.next and curr.next.val == curr.val:
                curr = curr.next
            prev.next = curr
            prev = curr
            curr = curr.next
        return dummy.next
        
# @lc code=end

