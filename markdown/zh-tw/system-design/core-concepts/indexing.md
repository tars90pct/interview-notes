# Indexing

索引的核心目標是加速資料查詢。在許多系統中，我們能容忍較慢的寫入，但無法接受讀取延遲。索引的過程即是建立一種資料結構，以優化讀取效率。

## 基本索引方法

- Hash Map：

  以特定鍵值儲存資料，查詢時可達 O(1) 時間複雜度。

  - 優勢：無需掃描整個資料集即可快速定位資料。

- Sorted List：

  資料按順序儲存，透過**Binary Search**實現 O(log n) 查詢。

  - 常見應用：資料庫的 B-Tree 索引。
  - 核心原則：透過前期少量運算，換取讀取效能的大幅提升。

## 資料庫中的Index

- 關聯式資料庫（如 PostgreSQL）：可為任意欄位或欄位組合建立索引。

- NoSQL 資料庫（如 DynamoDB）：支援多個次要索引（Secondary Indexes）。

- 記憶體資料庫（如 Redis）：需自行設計索引策略（如使用 Sorted Set）。

::TIPS
最佳實踐：優先使用資料庫內建索引功能，其經過數十年實戰驗證，避免重造輪子。
::

## 特化型的Index

- Geospatial Index

  - 應用場景: 位置查詢（如尋找最近的餐廳）
  - 技術案例: PostGIS

- Vector Index

  - 應用場景: 高維度資料相似性搜索（如圖像、文件比對）
  - 技術案例: Pinecone、Milvus

- Full-Text Index
  - 應用場景: 文字內容搜索（如文件、推文檢索）
  - 技術案例: Elasticsearch（基於 Lucene）

## Elasticsearch 作為次要索引方案

- 核心優勢：多功能索引支援（全文搜索、地理空間、向量索引）。

- 異步資料同步：透過 CDC（Change Data Capture）監聽資料庫變更，自動更新索引。
