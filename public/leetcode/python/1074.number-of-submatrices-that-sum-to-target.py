#
# @lc app=leetcode id=1074 lang=python3
#
# [1074] Number of Submatrices That Sum to Target
#

# @lc code=start
class Solution:
    def numSubmatrixSumTarget(self, matrix, target):
        rows, cols = len(matrix), len(matrix[0])
        prefix_sum = [[0] * (cols + 1) for _ in range(rows + 1)]

        # Compute the 2D prefix sum
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                prefix_sum[i][j] = matrix[i - 1][j - 1] + \
                      prefix_sum[i - 1][j] + \
                    prefix_sum[i][j - 1] - \
                        prefix_sum[i - 1][j - 1]

        count = 0

        # Iterate through all possible pairs of columns
        for col1 in range(1, cols + 1):
            for col2 in range(col1, cols + 1):
                # Use a hashmap to count the number of subarrays with a given sum
                prefix_sum_map = {0: 1}
                current_sum = 0
                for row in range(1, rows + 1):
                    current_sum = prefix_sum[row][col2] - prefix_sum[row][col1 - 1]
                    if current_sum - target in prefix_sum_map:
                        count += prefix_sum_map[current_sum - target]
                    if current_sum in prefix_sum_map:
                        prefix_sum_map[current_sum] += 1
                    else:
                        prefix_sum_map[current_sum] = 1

        return count
        
# @lc code=end

Solution().numSubmatrixSumTarget([[1,2,3],[4,5,6],[7,8,9]], 0)