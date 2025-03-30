#
# @lc app=leetcode id=19 lang=python3
#
# [19] Remove Nth Node From End of List
#
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        if not head:
            return None
        dummy = ListNode()
        dummy.next = head
        curr = dummy
        for _ in range(n):
            head = head.next
        
        while head:
            head = head.next
            curr = curr.next
        
        curr.next = curr.next.next
        return dummy.next
        
# @lc code=end

