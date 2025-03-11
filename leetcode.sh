#!/bin/bash

# 輸入字串
input=$(pbpaste)

# 使用 . 分割字串
parts=(${input//./ })

# 取得題號和題目名稱
leetcode_number="${parts[0]}"
leetcode_title="${parts[1]}"
leetcode_title_capitalized=$(echo "$leetcode_title" | awk '{
    for (i=1; i<=NF; i++) {
        word = $i;
        if (word ~ /^[a-z]/) {
            first_char = substr(word, 1, 1);
            gsub("^"first_char, toupper(first_char), word);
            $i = word;
        }
    }
    print;
}')
# 將題目名稱的 '-' 替換為 ' '
leetcode_title_capitalized="${leetcode_title_capitalized//-/ }"

# 產生模板
template="# ${leetcode_title_capitalized//-/ }

[Leetcode ${leetcode_number}](https://leetcode.com/problems/${leetcode_title}/description/)

::Question
::

## 釐清題意

## Pattern

## 實作

- python

\`\`\`python
{{LEETCODE|leetcode/python/${leetcode_number}.${leetcode_title}.py}}
\`\`\`

## 複雜度分析

- 時間複雜度
- 空間複雜度
"

# 將模板複製到剪貼簿
echo -n "$template" | pbcopy

# 顯示成功訊息
echo "模板已複製到剪貼簿！"