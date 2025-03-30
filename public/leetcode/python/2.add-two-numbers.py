#
# @lc app=leetcode id=2 lang=python3
#
# [2] Add Two Numbers
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
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        current = dummy
        carry = 0
        while l1 and l2:
            val = l1.val + l2.val + carry
            if val >= 10:
                val = val - 10
                carry = 1
            else:
                carry = 0
            l1 = l1.next
            l2 = l2.next
            current.next = ListNode(val=val)
            current = current.next
        
        rest = l1 or l2

        while carry != 0:
            val = carry
            if rest:
                val += rest.val
                if val >= 10:
                    carry = 1
                    val = val - 10
                else:
                    carry = 0
                rest = rest.next
            else:
                carry = 0
            current.next = ListNode(val=val)
            current = current.next
        current.next = rest
        return dummy.next
        
# @lc code=end

