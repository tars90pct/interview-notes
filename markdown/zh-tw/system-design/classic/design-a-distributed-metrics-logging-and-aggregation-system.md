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

## API or System Interface

- snedMetric(source, payload, timestamp)：更新資料至sendMetric
- fetchDataset(seriesId, timeRange)：從特定特徵取回資料

## High Level Design

![distributed-metric-hld]({{BASEURL}}/markdown/zh-tw/system-design/classic/distributed-metric-hld.png "distributed-metric-hld")

- Data Source & Publishing

  - 指標數據的來源通常來自伺服器（Server），這些數據可能具有突發性（Bursty），導致消費端無法即時處理。因此，我們通常會先發佈（Publish）數據至Message Queue，再由後續流程處理。
  - Message Queue(Kafka)
    - 由伺服器發佈事件流至 Kafka，確保數據可擴展（Scalable）且不會因消費端超載而丟失數據。
    - 數據格式
      - Structured Data: Avro、Thrift、Protobuf
      - Unstructured Data: JSON、XML

- Stateful Consumer

  數據發佈後，下一步是由 狀態型消費者（Stateful Consumer） 來處理與增強數據。

  - Spark Streaming：以微批（Mini-batch）方式處理訊息，提升效能。
  - Apache Flink：可逐條處理（Event-by-Event），適合低延遲需求。

  - Windowing: 數據具有時間序列(Time-Series)特性，可以使用 時間窗口（Time Window） 來進行聚合
  - Enrichment
    - 透過關聯外部數據（如用戶資訊），豐富事件內容
    - 方法
      - 查詢資料庫
      - 使用快取（如 Flink State、Redis）
      - 透過 Kafka CDC（Change Data Capture），將資料庫變更發送至 Kafka，並由 Flink/Spark 進一步處理。
  - Storage & Aggregation
    - File Storage
      - ParquetParquet 檔案格式：高效的列式存儲格式，適合分析型應用。
      - 存放位置：
        - Amazon S3: 便宜、適合長期存儲，但需要讀取回記憶體後才能進行計算
        - HDFS（Hadoop Distributed File System）（可本地計算，加快查詢但，運維成本較高。
      - Data Warehouse
        - 適合根據時間以外的維度進行分區（Partitioning），支援複雜查詢
        - BigQuery / Snowflake（雲端數據倉儲，易於擴展）
        - Amazon Redshift（AWS 整合性強）
        - Apache Hive（適用於 Hadoop 生態系統）
      - Search Index
        - Elasticsearch（支援倒排索引，適合日誌查詢）
        - 可根據時間、關鍵字等條件進行高效查詢。
        - 可擴展至多個分區，處理大量數據。
  - Time-Series Database, TSDB
    - 存放窗口化的時間序列指標數據（如監控數據）
    - 選擇：
      - Prometheus
      - TimescaleDB
      - InfluxDB
    - 優勢：
      - 高效插入（寫入速度快）
      - 支持 Hypertable & Chunk Table（可快速插入與刪除數據）

## Deep Dives

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

- **Text Logs**

  在分散式指標記錄與彙總系統中，文字日誌（Text Logs） 是最基本但又非常重要的數據來源之一。日誌通常由伺服器或應用程式產生，以純文字（String）形式儲存，記錄系統的執行狀況、錯誤訊息或關鍵業務事件。由於日誌數量龐大，如何有效地存儲、檢索與分析這些日誌數據是一個重要的設計考量。

  - 常用功能：

    - 查看完整日誌記錄

      - 例如，某台伺服器執行了一次作業（Run），我們希望查看該次執行期間產生的所有日誌。
      - 這類查詢通常按照 時間範圍（Time Range） 進行，因此可以使用 時序數據庫（Time Series Database, TSDB） 來儲存日誌。
      - 每條日誌紀錄可以包含：

        - 時間戳記（Timestamp）
        - 日誌內容（Log String）
        - 伺服器 ID（Server ID）
        - 應用程式名稱（Application Name）

      - 透過 TSDB，我們可以快速取得特定時間區間內的完整日誌記錄。

    - Search by Keyword
      - 由於日誌數據量龐大，直接遍歷（Full Scan）所有日誌進行關鍵字搜尋的成本極高，因此需要高效的檢索機制。
      - 最常見的方式是 倒排索引（Inverted Index）：
      - 針對日誌內容中的關鍵字建立索引，將關鍵字映射到所有包含該關鍵字的日誌行號（Line ID）。
      - 例如，當用戶搜尋「error」時，系統可以透過倒排索引迅速找到所有包含「error」的日誌行，而不必遍歷整個日誌庫。
      - 此技術與 全文搜尋引擎（如 Elasticsearch、Apache Solr） 的索引機制類似。

  - Partitioning Strategy
    - 為了提高查詢效能，日誌數據通常按照 伺服器 和 時間範圍 進行分區。例如：
      - Server A 的今日日誌 存放在 Partition A
      - Server A 的昨日日誌 存放在 Partition B
      - Server B 的今日日誌 存放在 Partition C
    - 同一台伺服器的日誌存放在同一個分區內，允許快速檢索當前運行的日誌。
    - 查詢近期日誌時，能夠避免全庫掃描，提高查詢速度。
    - 理想上可以把多天同一個server的log放在同一個partition，雖然大部分情況下還是要使用distributed query來滿足搜索條件。

- **Structured data**

  在分散式指標記錄與彙總系統中，除了日誌與時序數據外，應用程式也可能會產生 結構化數據（Structured Data）。這些數據通常來自業務物件，例如 購物車資訊、使用者行為數據、交易記錄 等，並且可以進行序列化（Serialization）和反序列化（Deserialization），以便儲存與查詢分析。

  - 數據結構已知，可以根據 Schema 來組織與最佳化存儲。
  - 支持序列化/反序列化
  - 通常需要支援 SQL 查詢，以利進行分析，例如：「哪些商品被加入購物車但沒有結帳？」
  - 需要有效率的存儲與傳輸，避免浪費頻寬與存儲空間。
  - 在處理結構化數據時，我們通常會使用 Schema 驅動（Schema-Driven） 的格式，例如：
    - Protocol Buffers（ProtoBuf）
    - Apache Thrift
    - Apache Avro
  - 這些格式與 JSON 或 XML 最大的不同點是不需要在數據中存儲欄位名稱：
    - 例如，在 JSON 中，每一條數據都包含完整的欄位名稱（如 "name"），但在 ProtoBuf 或 Avro 中，接收方已經擁有 Schema，因此可以只傳輸數據內容，節省空間。
    - 更小的數據體積：比起傳輸完整的鍵值對（如 {"name": "Jordan","size_in_inches": 13}），"1:Jordan,2:13"更加節省空間與頻寬。
  - Schema Registry
    - 集中化Schema存儲庫
    - Schema版本管理
    - 支持多種格式：Protobuf/Thrift/Avro
    - 運作流程：
      - 生產者端註冊Schema → Kafka傳輸編碼數據 → Flink消費端查詢Registry解析
      - Flink本地緩存Schema
      - 狀態化消費者設計
      - 減少Registry查詢次數

- **Unstructured Data**

  在處理非結構化數據時，我們通常無法預先定義固定的 Schema，這主要是因為：

  - 這些數據可能來自外部 API，而我們無法控制它們的數據格式。
  - 這些 API 可能會變動，而我們無法取得它們的 ProtoBuf、Avro、Thrift Schema。
  - 這導致我們無法直接使用 Schema 驅動的數據格式來解析，而只能先儲存為 JSON，然後後續再進行規範化（Normalization）。

  - 處理流程
    ```
    外部API → JSON原始數據 → Kafka傳輸 → Flink聚合 → Hadoop原始存儲 → Spark ETL轉換 → 結構化存儲
    ```
    - Streaming Ingestion
      - 數據來源：來自外部 API、日誌系統等
      - 傳輸格式：通常是 JSON，因為 JSON 具有靈活的結構
      - 數據管道：透過 Kafka 進行流式傳輸
    - Flink預處理
      - Flink 讀取 Kafka 數據
      - 數據仍然是非結構化的 JSON
      - Flink 進行簡單的聚合（Aggregation）
        - 將多條 JSON 日誌合併成一個文件
        - 轉存為純文字檔（TXT / JSON 文件）
    - Temporary Storage
      - Flink 會將處理後的 JSON 文件存入 Hadoop HDFS
      - HDFS 主要用於臨時存儲，之後我們會使用 Spark 來轉換數據
    - Spark 進行 ETL（Extract, Transform, Load）
      - Spark 會讀取 HDFS 中的 JSON 文件，並進行轉換
      - Parquet (HDFS中依照Column儲存的格式)
      - 轉換為結構化數據（如 Avro / ORC）
      - 清理數據（去除異常值、格式錯誤的數據）
      - 標準化數據結構（轉換成可用的 Schema 格式）
    - Sync to Data Warehouse
      - 處理完成的數據可同步至：
        - HDFS（長期存儲）
        - Amazon S3（雲端存儲）
        - 數據倉庫（Snowflake、BigQuery、Redshift）
      - 最終結果可以透過 SQL 查詢分析

- **Column Oriented Storage Implementation**

  在Analytical Queries中，Column-Oriented Storage通常比傳統的Row-Oriented Storage更高效，因為：

  - 查詢時通常只關心某些特定欄位，而不是整行數據。
  - 欄式存儲能夠提高數據局部性（Data Locality），減少不必要的 I/O。

  舉例來說，假設我們有一張電子郵件註冊記錄表，如果我們想計算每天新註冊的用戶數，使用欄式存儲時，所有 註冊日期（signup_date） 欄位的數據都會被存儲在一起，而無需讀取不相關的欄位（如姓名、電子郵件等），這樣查詢速度會快很多。

  在現代數據系統中，PAX（Partition Attributes Across）格式是一種常見的欄式存儲方法，它將數據劃分為較小的塊，每個塊內部仍然是欄式存儲，這種方式兼具欄式存儲的優勢與部分列式存儲的靈活性。

  - Parquet

    - 一種欄式存儲格式，可以對數據進行高效的壓縮與編碼，降低存儲成本，並加快查詢速度。
    - Predicate Pushdown至：在文件標頭儲存 最小值（Min）、最大值（Max）、平均值（Avg） 等元數據，使查詢時可以跳過不必要的數據塊，提升查詢速度
    - Compression：壓縮編碼：針對不同數據類型自動選擇最佳壓縮算法（如RLE/Dictionary），減少存儲大小，提高 I/O 效率。

  - 存儲位置選擇
    - Blob Storage(S3)
      - 存儲成本低（存算分離）
      - 需網路傳輸數據
      - 無限水平擴展
      - 適用於冷數據/歸檔分析
    - Hadoop HDFS
      - 需同步擴展計算/存儲資源
      - 本地讀取速度更快
      - 受集群規模限制
      - 適用於已建置Hadoop生態的企業
    - 雲原生數據倉庫方案(Snowflake,Google BigQuery,Amazon Redshift)
      - 按查詢量計費
      - 預計算加速查詢
      - 自動彈性擴縮容
      - 高頻即時分析需求
  - Partitioning
    - Partitioning by Time: 適用於時間序列數據，如日誌數據、用戶行為數據等。
    - Partitioning by Business Logic: 例如電商網站的訂單數據，可能主要根據商家 ID（vendor_id）進行查詢，這樣按商家 ID 分區會更高效。
  - Indexing：
    - 建立Z-Order index 優化多欄位查詢
    - 利用數據倉庫的CLUSTER BY指令（如Redshift/Snowflake）

- **Stream Enrichment**

  Stream Enrichment是一個關鍵步驟，因為我們經常需要將即時事件流（Real-time Event Stream）與外部數據源（如用戶資訊）結合，以提供更完整的數據分析。

  - 應用場景：
    - 即時關聯事件流與維度表（如用戶點擊事件+用戶屬性資料）
    - 強化原始事件價值（例：點擊事件附加用戶等級/地域資訊）
    - 支援即時儀表板與告警系統
  - Stream Enrichment實作討論

    有幾種方式可以實作 即時數據增強（Stream Enrichment），但關鍵在於如何**高效地查詢用戶資訊表（User Info Table）**來豐富事件流數據。

    ## ![stream-enrichment]({{BASEURL}}/markdown/zh-tw/system-design/classic/stream-enrichment.png "stream-enrichment")

    - 直接查詢資料庫
      - 當 Flink 消費者（Flink Consumer）收到新的使用者點擊事件
      - 發送 SQL 查詢到資料庫
      - 獲取對應的用戶資訊，並合併到點擊事件
      - 優勢
        - 不需要額外的記憶體來存儲用戶資訊
        - 用戶資訊始終是最新的（最新狀態）
      - 缺點
        - 網路請求延遲高：每次查詢都會引發額外的網路開銷，導致處理速度變慢
        - 資料庫負擔大：如果點擊事件頻率很高，資料庫查詢可能成為系統瓶頸
    - 在 Flink 中快取（Cache）用戶資訊
      - 預載入（Preload）用戶資訊到 Flink 並提供定期更新
      - 當新的點擊事件到來時，直接從快取查找對應的 user_id
      - 如果快取中沒有對應資料，則回退（fallback）到資料庫查詢
      - 優勢
        - 查詢速度快（避免頻繁訪問資料庫）
        - 降低資料庫負擔（減少網路請求與 I/O 負擔）
      - 缺點
        - 需要考慮快取更新策略（如何確保快取中的資料不會過時）
        - 當用戶資訊表非常大時，快取的內存需求可能會很高
    - Partitioning
      - 如果用戶資訊表很大，我們可能無法一次性將所有數據快取到 Flink。這時候，我們可以根據 user_id 進行分區，只加載部分數據來快取
      - 將 Flink 消費者劃分為多個節點（Flink Task Slots），每個節點負責特定範圍的 user_id
      - 每個節點僅加載自己負責範圍內的用戶資訊
      - 當事件到來時，只查詢對應分區的快取，如果快取中沒有，則回退到資料庫查詢

## 推薦連結

- Detailed Solution from Google Engineer: [youtube.com](https://www.youtube.com/watch?v=p_q-n09B8KA)
- Good overview from Google Engineer: [youtube.com](https://www.youtube.com/watch?v=_KoiMoZZ3C8)
- Related - Ad Click Aggregation: [hellointerview.com](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator)
- Leetcode Discussion: [leetcode.com](https://leetcode.com/discuss/interview-question/system-design/622704/Design-a-system-to-store-and-retrieve-logs-for-all-of-eBay)
