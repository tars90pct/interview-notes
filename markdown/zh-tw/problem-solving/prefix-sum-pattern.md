Prefix Sum觸發條件：
給你一個Array，需要取出之前累加後的成果：

Pattern:

- 依照題意產生prefix sum
- 可能需要輔助的hashmap來處理不同的結果
  - 例如題目想要求K: current_sum - previous_sum = k，則我們會將previous_sum作為key
- 由prefix sum的結果來取得不同的值

```python
nums = [2,3,1,4,5]
prefix_sum = []
current = 0
for n in nums:
  # n = -1 if n == 0 else 1 -> 視情況修改要append prefix sum的值
  current += n
  # 有時候可能是hashtable來存某個sum出現過的次數
  prefix_sum.append(current)
```
