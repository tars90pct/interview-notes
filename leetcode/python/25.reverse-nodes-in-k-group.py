#
# @lc app=leetcode id=25 lang=python3
#
# [25] Reverse Nodes in k-Group
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
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None:
            return None
        
        count = k - 1
        current = head

        def reverse(prev, curr):
            if curr is None:
                return prev
            temp = curr.next
            curr.next = prev
            return reverse(curr, temp)

        while current and count > 0:
            current = current.next
            count -= 1

        if count == 0 and current:
            next_head = current.next
            current.next = None
            new_head = reverse(None, head)
            head.next = self.reverseKGroup(next_head, k)
            return new_head
        return head

       
# @lc code=end

