#
# @lc app=leetcode id=4 lang=python3
#
# [4] Median of Two Sorted Arrays
#

# @lc code=start
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Ensure nums1 is the smaller array
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        
        # Get the lengths of the two arrays
        len1, len2 = len(nums1), len(nums2)
        
        # Set the range for binary search on nums1
        left, right = 0, len1
        
        while left <= right:
            # Partition nums1 and nums2
            partition1 = (left + right) // 2
            partition2 = (len1 + len2 + 1) // 2 - partition1
            
            # Find the maximum elements on the left of the partition
            max_left1 = nums1[partition1-1] if partition1 > 0 else float('-inf')
            max_left2 = nums2[partition2-1] if partition2 > 0 else float('-inf')
            max_left = max(max_left1, max_left2)
            
            # Find the minimum elements on the right of the partition
            min_right1 = nums1[partition1] if partition1 < len1 else float('inf')
            min_right2 = nums2[partition2] if partition2 < len2 else float('inf')
            min_right = min(min_right1, min_right2)
            
            # Check if the partition is correct
            if max_left <= min_right:
                # If the total length is even, return the average of the two middle elements
                if (len1 + len2) % 2 == 0:
                    return (max_left + min_right) / 2
                # If the total length is odd, return the middle element
                else:
                    return max_left
            elif max_left1 > min_right2:
                right = partition1 - 1
            else:
                left = partition1 + 1
        
# @lc code=end

