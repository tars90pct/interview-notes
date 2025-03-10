# Elasticsearch

Elasticsearch 是一款基於 Apache Lucene 的開源分散式搜尋與分析引擎，專為處理大規模數據設計。其核心特性包括：

- 全文搜索：快速從海量文本中找出相關結果。
- 即時分析：聚合統計、視覺化數據趨勢。
- 分散式架構：自動分片（Sharding）與副本（Replication），支援水平擴展。
- 多用途：日誌管理（ELK Stack）、電商商品搜尋、推薦系統等。

## Inverted Index

Inverted Index是 Elasticsearch 高效搜索的核心技術，其設計邏輯與傳統Forward Index截然不同：

- Forward Index
  - 映射關係: 文件 → 詞項
  - 範例: 文件1：["蘋果", "手機", "5G"]
- Inverted Index
  - 映射關係: 文件 → 詞項
  - 範例: "蘋果" → [文件1, 文件3]

可搜尋TF-IDF理解細節

## Elasticsearch 分散式架構

- 分片（Shard）與副本（Replica）
  分片：將索引水平拆分為多個子集，分散儲存至不同節點。

  - Primary Shard：處理寫入與讀取。
  - Replica Shard：備份Primary Shard，提升容錯性與讀取吞吐。

- 當節點故障時，副本分片自動提升為主分片。
- 單一分片建議 10-50GB。預留擴展空間（分片數建立後不可修改）。
- 設定範例：

```
PUT /products
{
  "settings": {
    "number_of_shards": 3,   // 主分片數（建立後不可改）
    "number_of_replicas": 1  // 每個主分片的副本數（可動態調整）
  }
}
```

## ELK Stack and Beats

- Elasticsearch：數據儲存與搜索。
- Logstash：數據收集與處理管道。
- Kibana：數據視覺化儀表板。
- Beats：輕量級數據採集器（如 Filebeat 收集日誌）。

## Full-Text Search

- 場景：電商商品搜尋引擎
- 需求：用戶輸入關鍵字（如「無線藍牙耳機」），即時返回相關商品，支援模糊搜尋與同義詞擴展。
- 實作：

  1.定義索引 Mapping

  ```
  PUT /products
  {
  "mappings": {
    "properties": {
      "title": { "type": "text", "analyzer": "ik_max_word" },  // 中文分詞
      "description": { "type": "text", "analyzer": "ik_smart" },
      "price": { "type": "double" },
      "category": { "type": "keyword" }
    }
  }
  }
  ```

  2. 插入資料：

  ```
  POST /products/_doc/1
  {
  "title": "高音質無線藍牙耳機",
  "description": "支援降噪，續航 20 小時",
  "price": 2999,
  "category": "電子產品"
  }
  ```

  3. 全文搜索查詢：

  ```
  GET /products/_search
  {
  "query": {
    "match": {
      "title": {
        "query": "藍芽耳機",
        "fuzziness": "AUTO"  // 模糊匹配（容錯 1-2 字元）
      }
    }
  }
  }
  ```

  結果：即使輸入「藍芽」（同義詞）或拼寫錯誤（如「籃牙」），仍能匹配「藍牙」相關商品。

## Geospatial Index

- 場景：外送平台餐廳搜尋
- 需求：用戶定位後，顯示方圓 3 公里內評分 4 星以上的餐廳，按距離排序。
- 實作：

  1. 定義地理空間 Mapping：

  ```
  PUT /restaurants
  {
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "location": { "type": "geo_point" },  // 地理座標
      "rating": { "type": "float" }
    }
  }
  }
  ```

  2. 插入餐廳資料（經緯度格式）：

  ```
  POST /restaurants/_doc/1
  {
  "name": "老王牛肉麵",
  "location": { "lat": 25.0330, "lon": 121.5654 },  // 台北 101 座標
  "rating": 4.5
  }
  ```

  3. 地理空間查詢：

  ```
  GET /restaurants/_search
  {
  "query": {
    "bool": {
      "must": [
        { "range": { "rating": { "gte": 4.0 } } },
        { "geo_distance": {
          "distance": "3km",
          "location": { "lat": 25.0345, "lon": 121.5647 }  // 用戶當前位置
        }}
      ]
    }
  },
  "sort": [
    { "_geo_distance": {
      "location": "25.0345,121.5647",
      "order": "asc",
      "unit": "km"
    }}
  ]
  }
  ```

  結果：返回符合評分條件且距離用戶最近的餐廳，並按距離排序。

## Vector Index

- 場景：電商圖片相似推薦
- 需求：用戶瀏覽商品時，推薦視覺風格相似的產品（如同色系、同材質）。

  1. 定義向量索引 Mapping：

  ```
  PUT /products_vector
  {
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "image_vector": {
        "type": "dense_vector",
        "dims": 512,
        "index": true,
        "similarity": "cosine"  // 餘弦相似度計算
      }
    }
  }
  }
  ```

  2. 插入向量資料：

  ```
  POST /products_vector/_doc/1
  {
  "title": "紅色羊毛大衣",
  "image_vector": [0.12, -0.05, ..., 0.78]  // 512 維向量
  }
  ```

  3. 向量相似度查詢：

  ```
  GET /products_vector/_search
  {
  "knn": {
    "field": "image_vector",
    "query_vector": [0.15, -0.03, ..., 0.75],  // 目標圖片向量
    "k": 5,  // 返回最相似的 5 筆
    "num_candidates": 100
  }
  }
  ```

  結果：根據向量相似度，推薦視覺特徵接近的商品。

## 同步機制：CDC + Elasticsearch

- 架構（資料流）：[主資料庫] → [Debezium CDC] → [Kafka] → [Elasticsearch 消費者] → [更新索引]
- 優點：
  - 異步處理：不影響主資料庫寫入效能。
  - 容錯能力：Kafka 保存變更日誌，避免資料遺失。
- 缺點：
  - 資料延遲：從寫入主庫到索引更新可能有數秒延遲。
  - 維護成本：需監控 CDC Pipeline 與 Elasticsearch 集群健康狀態。
