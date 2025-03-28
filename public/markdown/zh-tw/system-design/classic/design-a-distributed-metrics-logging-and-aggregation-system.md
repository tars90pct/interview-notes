# Design a Distributed Metrics Logging and Aggregation System

- Let's assume the logs are generated from a distributed system, e.g, an EC2 compute cluster.
- How to collect logs efficiently from distributed systems?
- How to store and index logs for fast retrieval?
- When you search for logs, what happens?
- How about live streaming logs? How would that work?

## 題目理解：

- 資料類型

  - Server Logs

    - [2023-10-01 14:22:35] ERROR: User jordan tried to access unauthorized endpoint /admin

  - Structured Data

    ```json
    {
      "sender": "megan_fox",
      "recipient": "jordan",
      "timestamp": "2023-10-01T14:25:00Z",
      "content": "Check out this new project!",
      "metadata": { "priority": "high" }
    }
    ```

  - Time-Windowed Metrics

    - `jordan.received_dms.count = 22 (time_window: 2023-10-01T00:00:00/24h)`

  - Unstructured Data

    - 任意格式的payload存儲
      - 第三方API response
      - IoT設備原始二進位stream

## Functional Requirements:

我們需要設計一個分散式的指標記錄與彙總系統，以處理來自水平擴展（horizontally scaled）大規模服務中，分佈在許多不同的節點上的數據來源。我們的系統必須能夠有效地儲存、查詢、分析 這些數據，以支援debugging、business analytics等用途。

- 高吞吐量與可擴展性
  - 需處理來自水平擴展（horizontally scaled）服務器集群的高吞吐量數據
  - 數據來源多樣化：應用服務器、微服務、分散式節點等
  - 需支援每秒數十萬至百萬級事件處理
- 多種類型的數據存儲與處理
  - Time Series: 如系統監控指標（CPU、記憶體、請求延遲）
  - Text Logs: 用於除錯與錯誤追蹤（例如伺服器錯誤堆疊）
  - Structured Data: 可直接映射到資料庫的物件（如 JSON 結構）
  - Unstructured Data: 需後續轉換為結構化格式的原始數據（如未經處理的用戶行為軌跡）
- Data Enrichment
  - 動態關聯外部資料來源（例如將 User ID 與用戶資料庫 JOIN）
  - 支援即時或批次數據增強（如添加地理位置、用
- 高效查詢與分析
  - 長期儲存原始數據以供回溯分析（冷儲存與熱儲存分層設計）
  - 支援即時查詢（Real-time Query）與離線分析（Batch Processing）
  - 提供聚合視圖（Aggregated Views）供業務分析（如每分鐘請求數、錯誤率儀表板）
  - 可能需要支援 索引 (indexing) 或 分片 (sharding) 來優化查詢效能。

## Non-functional Requirements

- CAP Theorem:
  - AP為主
  - 監控系統需要即時收集和存儲大量數據，即使部分節點發生故障，也應確保數據能繼續寫入和查詢。
  - 最終一致性（Eventual Consistency） 是可以接受的，因為大多數監控與日誌數據允許短暫的不一致，但最終會同步。
- Environment Constraints

  - 雲端 vs. 本地部署
    - 雲端部署（Cloud-based）：適合高彈性需求，能夠利用 AWS S3、Google Cloud Storage、Azure Blob 來存儲大量日誌和指標數據。
    - 本地部署（On-Premise）：如果數據量過大或有合規要求（如 GDPR、HIPAA），可能需要本地存儲（如 HDFS、Ceph）。
  - 網路條件
    - 若日誌來自全球不同地區的伺服器，則需要 CDN 或邊緣計算（Edge Computing） 來減少延遲和頻寬使用

- Scalability

  - Kafka、Elasticsearch、Cassandra 等技術能夠透過增加節點來提升吞吐量。
  - 分散式數據存儲（Sharding）：將日誌數據切分到不同的節點，以減少單一節點的負擔。

- Latency

  - 寫入延遲
    - 大量日誌與指標數據可能會導致高寫入壓力，需使用 Kafka、Pulsar 等消息隊列來緩衝流量。
    - 透過 批量處理（Batch Processing） 減少頻繁 I/O 開銷，如 Fluentd、Logstash。
  - 查詢延遲
    - 索引機制（Indexing）：例如 Elasticsearch 透過倒排索引（Inverted Index）加速全文檢索。
    - 快取機制（Caching）：如 Redis、Memcached，減少頻繁的查詢運算。

- Durability
  - 多副本存儲（Replication）：Kafka、Elasticsearch、HDFS 支持 多副本機制，確保即使部分節點失效，數據仍可恢復。
  - 持久性存儲（Persistent Storage）：使用 S3、GCS、HDFS 等分散式存儲確保數據長期可用。
  - 快照與備份（Snapshot & Backup）：透過 Elasticsearch Snapshot 定期將索引備份到 S3，以防止數據損毀。

## High Level Design

- **Data Sink**

  Data Sink 負責處理大量的日誌與指標數據，確保系統能夠有效地吸收這些數據，而不影響核心服務的穩定性與效能。

  - 為什麼不能直接發送數據到伺服器？

    - 流量突增可能導致伺服器過載: 如果某一時間點日誌流量暴增（如系統異常、DDoS 攻擊），伺服器可能無法即時處理這些請求，甚至可能崩潰。
    - 同步請求導致高延遲：若伺服器需要在接收數據的同時進行計算或轉發，可能無法跟上高併發的請求，導致整體系統效能下降。
    - 數據丟失風險：若系統發生故障，直接發送的數據可能無法可靠儲存，導致部分指標與日誌遺失。
    - 延遲問題：同步處理龐大日誌時，響應速度可能無法滿足需求。

  - 使用中介緩衝區（如 Kafka）

    為了解決上述問題，我們通常會選擇中介緩衝區（Message Queue / Event Streaming System）作為數據的「暫存區」，而 Kafka 是其中最受歡迎的選擇。

    - 資料持久化保存
    - 訊息複寫（replication）機制
    - 可依需求分區（partitioning）
    - 基於日誌的消息代理（Log-based Broker）
    - 支援串流處理框架

  - Aggregation
    - Flink / Spark Streaming 作為狀態型消費者（Stateful Consumer）：
      - 確保所有數據至少被處理一次（At-least-once Processing）。
      - 支援外部數據查詢與豐富化（Enrichment）：例如，透過 Join 操作，將指標數據與用戶資訊結合，提供更豐富的分析能力。
    - 例如，我們可以將每秒鐘的 CPU 使用率數據匯總成 1 分鐘的平均值，減少存儲成本。

- **Data Aggregation**

  在設計分散式指標記錄與彙總系統時，數據彙總（Aggregation）是核心環節之一。彙總的主要目標是減少數據量，提高查詢效率，同時保留關鍵資訊以供分析。

  常見的數據彙總方法包含以下三種視窗（Windowing）機制：

  - Tumbling Window
    - 定義：固定視窗將時間切割成不重疊的區間（如每 10 分鐘一個視窗）
    - 每個數據點會被分類到對應的視窗中，確保所有數據都有且僅有一個歸屬的時間區間。
    - 適用場景：定期統計固定時段指標（如每 10 分鐘請求量）。12:15 的資料點會被歸入 12:10-12:20 的視窗。
  - Hopping Window

    - 與 Tumbling Window 類似，但視窗允許重疊，即一個數據點可能屬於多個視窗
    - 一個 Hopping Window 需要指定視窗大小（Window Size）與跳躍間隔（Hop Size）：
      - Window Size：視窗的總時長，例如 20 分鐘。
      - Hop Size：每次新建視窗的時間間隔，例如 10 分鐘（表示每 10 分鐘建立一個新的視窗，但每個視窗仍持續 20 分鐘）。
    - 假設我們有一個 Window Size = 20 分鐘，Hop Size = 10 分鐘 的 Hopping Window，則時間區間如下：
      - 12:00 - 12:20
      - 12:10 - 12:30
      - 12:20 - 12:40
    - 適用場景：平滑統計趨勢（如每 10 分鐘更新過去 20 分鐘的平均延遲）。

  - Sliding Window
    - 與 Hopping Window 類似，但 Sliding Window 沒有固定的起點，而是根據最新數據點來決定視窗範圍。
    - Sliding Window 會維持一個持續移動的時間範圍，例如「最近 20 分鐘內的所有數據」。
    - Sliding Window 使用鏈結串列（Linked List） 來管理數據，即新數據進來時會添加到尾端，並不斷刪除超過視窗範圍的舊數據。
    - 視窗無固定起訖時間，僅保留「當前時間點往前 N 分鐘」的資料。
    - 新資料加入末端，超時資料從前端移除。  
      例如：12:23 時收到新資料，若滑動視窗為 20 分鐘，則刪除 12:00 前的舊資料。
    - 適用場景：即時監控（如持續計算最近 5 分鐘的錯誤率）。

- **Time Series Database**

  在分散式指標記錄與彙總系統中，時序數據庫（TSDB）是專門用來存儲時間序列數據的解決方案。由於系統會定期產生大量的指標數據（例如，每 5 分鐘產生一筆新數據），需要高效的存儲與查詢機制來管理這些數據。因此，使用 TSDB 而非一般關聯式資料庫（如 MySQL 或 PostgreSQL），能夠帶來更好的效能與擴展性。

  - Hypertable and Chunk Table 設計
    - Hypertable由多塊chunk table組成，每個分塊表對應特定時間範圍與資料來源。
    - 範例：
      - `Server A 的今日資料` = 一個分塊表，
      - `Server A 的昨日資料` = 另一個分塊表。
    - 優勢：
      - 高效快取：單一分塊表（如單一來源+時間範圍）可完整載入記憶體，加速讀取。
      - LSM 樹優化：每個分塊表使用獨立的 LSM 樹（Log-Structured Merge Tree），因寫入集中在單一分塊表，LSM 樹規模更小，寫入與查詢效率更高。
      - 時間序寫入特性：若資料按時間戳嚴格順序寫入（如 12:00 → 12:01），可直接用有序列表取代 LSM 樹，待資料累積後再批量寫入 SS 表（Sorted String Table）。
      - Partitioning簡化：同一分塊表的資料自動歸類到相同分區，簡化分區規則設計。（例如：按「時間範圍+來源」分區，天然對齊分塊表邊界）
      - 寫入模式匹配：指標系統的資料具時間局部性（近期資料頻繁寫入，舊資料冷卻），分塊表設計完美契合此特性。
      - 查詢效率：常見查詢（如「某伺服器過去 1 小時指標」）對應單一分塊表，減少 I/O 與計算開銷。
      - 儲存成本控制：冷資料可快速批量刪除或歸檔，降低儲存壓力。
      - 高效刪除機制
        - 傳統 LSM 樹刪除問題：需寫入墓碑標記（Tombstone），再透過 Compaction 合併 SS 表，耗時且影響寫入效能。
        - 分塊表優勢：直接刪除整個分塊表（如過期資料），無需逐筆處理，避免與即時寫入競爭資源。

## 推薦連結

- Detailed Solution from Google Engineer: [youtube.com](https://www.youtube.com/watch?v=p_q-n09B8KA)
- Good overview from Google Engineer: [youtube.com](https://www.youtube.com/watch?v=_KoiMoZZ3C8)
- Related - Ad Click Aggregation: [hellointerview.com](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator)
- Leetcode Discussion: [leetcode.com](https://leetcode.com/discuss/interview-question/system-design/622704/Design-a-system-to-store-and-retrieve-logs-for-all-of-eBay)
