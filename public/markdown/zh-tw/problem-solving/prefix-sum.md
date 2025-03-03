# Prefix Sum

前綴和（Prefix Sum）的作法是預先處理一個陣列：建立一個新陣列，其中每個索引 i 處的元素代表原陣列從起始位置到索引 i 的元素總和。這種方式能讓子陣列的求和查詢變得高效。

當你需要對子陣列進行*多次求和查詢*，或是需要*計算累積總和*時，即可採用這種模式。

## 特性：

- P\[j] = A\[j] + A\[j-1] + ... + A\[0]
- 要找到索引 i 和 j 之間的總和，請使用以下公式：P\[j] - P\[i-1]

![prefix-sum]({{BASEURL}}/markdown/zh-tw/problem-solving/prefix-sum.jpg "prefix-sum")
