# Range Sum Query - Immutable

[Leetcode 303](https://leetcode.com/problems/range-sum-query-immutable/description/)

::Question

::

## 釐清題意

- 範例

  **輸入**: height = \[1,8,6,2,5,4,8,3,7]
  **輸出**: 49
  **解釋**: left = 1, right = 8, max(n\[left], n\[right]) \* (right - left) = 49

## Pattern

::TIPS
{{FILE|markdown/zh-tw/problem-solving/prefix-sum-pattern.md}}
::

## 實作

- python

```python
{{LEETCODE|leetcode/python/303.range-sum-query-immutable.py}}
```

## 複雜度分析

- 時間複雜度
- 空間複雜度
