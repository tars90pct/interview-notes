# Identify the K Most Shared Articles in Various Time Windows

想像您正在為 NewsHub 開發一個新功能。NewsHub 是一個受歡迎的線上新聞聚合網站與行動應用程式，彙集了來自全球數千個來源的文章。

## 目標：

NewsHub 希望在其首頁和應用程式內顯示「即時熱門趨勢」（Trending Now）區塊。這些區塊需要向使用者展示當前在各種平台（例如社群媒體、電子郵件、即時通訊應用程式等）上被最積極分享的文章。具體來說，他們需要三個不同的列表：

1.  **「即時瘋傳」（Viral Right Now）**（過去 5 分鐘內前 5 名）：捕捉近期人氣急劇飆升的文章。此列表需要頻繁更新。
2.  **「每小時熱議」（Hourly Buzz）**（過去 1 小時內前 10 名）：顯示過去一小時內持續引起關注的文章。
3.  **「每日熱選」（Daily Hot Picks）**（過去 24 小時內前 20 名）：識別在一天內整體分享活躍度顯著的文章。

## 分享追蹤方式（系統輸入）：

每當使用者透過 NewsHub 應用程式或網站內的「分享」按鈕分享一篇文章時（例如，分享到 Twitter、Facebook、WhatsApp、電子郵件，或複製連結），就會產生一個「分享事件」。此事件至少包含：

- `article_id`：被分享文章的唯一識別碼。
- `timestamp`：分享發生的確切時間。
- `user_id`（可選）：分享者的使用者識別碼。
- `platform`（可選）：分享的目的地平台（例如：'twitter', 'facebook', 'email'）。

## 需解決的問題（系統輸出）：

您需要設計的系統必須能夠持續處理這股大量湧入的分享事件串流。它必須能夠高效率地計算並在收到請求時，檢索出：

- 在**當前 5 分鐘滑動時間窗口**內，分享次數最高的 **K=5** 個 `article_id`。
- 在**當前 1 小時滑動時間窗口**內，分享次數最高的 **K=10** 個 `article_id`。
- 在**當前 24 小時滑動時間窗口**內，分享次數最高的 **K=20** 個 `article_id`。

您的系統會針對每個請求的時間窗口和 K 值，回傳 `article_id` 的列表。接著，NewsHub 前端會從另一個服務獲取相應的文章標題/圖片，並顯示「即時熱門趨勢」列表。

## Details to Know:

- At its core - what algorithm would you use? Count Min Sketch? or some other?
- How will you ensure that each new update (share) is fast?
- How do you use caching to improve read performance?
- How will you scale this as updates get very frequent?

## Functional Requirements

- Event Ingestion:
  - 系統必須能夠接收來自外部（例如：網站前端、APP 後端）的文章分享事件。
  - 每個分享事件至少需包含 article_id (文章的唯一標識符) 和 timestamp (分享發生的精確時間)。
  - 事件可包含 user_id 或 share_platform (如 'facebook', 'twitter', 'email') 等額外資訊，但核心計數功能主要基於 article_id 和 timestamp。
- Count Tracking and Aggregation:
  - 系統需要為每一篇 article_id 追蹤其在特定時間內的分享次數。
  - 系統必須能夠針對Sliding Time Windows(5 分鐘, 1 小時, 24 小時)匯總分享計數
  - Sliding Time Window意味著時間窗口是相對於當前時間動態計算的，而非固定的日曆時間區塊。
- Top K Querying:
  - 系統必須提供一個介面（例如 RESTful API），允許客戶端查詢在指定時間窗口內，分享次數最多的前 K 名文章。
  - 查詢應能指定時間窗口參數（例如 window=5m, window=1h, window=24h）和 K 值參數（例如 k=5, k=10, k=20）。
  - API 回應應包含排序後的 article_id 列表，通常按分享數降序排列，回應可包含對應的分享計數。
  - Configurable K:
    - 系統應允許為不同的時間窗口配置不同的 K 值（例如 5 分鐘窗口 K=5，1 小時窗口 K=10，24 小時窗口 K=20）。

## Non-Functional Requirements

- CAP Theorem
  - Availability
  - Eventual Consistency。一個新的分享事件可能不需要在毫秒內立即反映在所有查詢結果中，但應在幾秒鐘內被計入並最終反映出來。對於趨勢計算，微小的計數延遲通常是可接受的。
- Scalability
  - 系統必須能夠水平擴展以處理大量文章（可能達百萬級別）和極高流量的分享事件（可能達到每秒數千至數萬次）。
  - 讀取（查詢 Top K）和寫入（攝取事件）操作都需要高吞吐量。
- Latency

  - Top K 查詢請求的回應時間應非常低，尤其是對於 5 分鐘和 1 小時的窗口，以支援近乎即時的用戶體驗。例如，P99 延遲應低於 100-200 毫秒。
  - 事件處理和計數更新應快速完成，避免事件積壓，確保資料新鮮度。
  - 對於 5 分鐘和 1 小時這樣較短的時間窗口，應該能在極短的時間內（例如幾秒鐘內）影響到 Top K 的計算結果。

- Durability
  - 系統需要具備高可用性，因為它通常驅動著網站或應用的核心用戶功能（如「熱門文章」）。目標可用性應達到 99.9% 或更高。系統應能容忍單點故障。
- Fault Tolerance
  - 系統應盡力確保分享事件不丟失，保證計數的準確性。

## Capacity Estimation

- Assumptions

  - Daily Active Users, DAU: 10000000(10 Million) DAU
  - 每日總分享數: 假設平均每天總共有 1 億 (100 Million) 次文章分享事件發生（包含所有使用者和平台）。這是一個核心指標，比假設單個用戶分享率更直接。
  - 活躍文章數量: 假設在任何時間點，系統中約有 500 萬 (5 Million) 篇活躍的文章（即近期可能被分享的文章）。
  - Peak Load Factor: 假設高峰時段的流量（讀取和寫入）是平均流量的 3 倍
  - Read Query Frequency: 假設每個 DAU 平均每天觸發 5 次 Top K 查詢（可能包含頁面加載、下拉刷新、不同時間窗口的查詢）
  - Size per Share Event: 假設每個分享事件傳輸到後端的資料大小約為 500 Bytes (包含 article_id, timestamp, 可能的 user_id, platform 等元數據)
  - Size per Query Response: 假設每次 Top K 查詢的回應（例如，返回 K 個 article_id 列表）平均大小為 1 KB (考慮到 K 最大為 20，可能還包含少量額外資訊)
  - 資料保留策略:
    - 原始分享事件：假設只保留 7 天 用於可能的除錯或重新處理。
    - 匯總計數：需要至少能覆蓋 24 小時 的滑動窗口

- Write Load Estimation - Share Events

  - Average Shares Per Second, SPS: 100,000,000 / 86,400 = 1,157 SPS
  - Peak SPS: 1,157 SPS \* 3 = 3,471 SPS -> 3,500 SPS

- Read Load Estimation - Top K Queries

  - Total Queries per Day = 10,000,000 DAU \* 5 次查詢/DAU = 50,000,000 Queries/Day
  - 平均每秒查詢數 (Average Queries Per Second, QPS): 50,000,000 次查詢 / 86,400 秒 ≈ 579 QPS
  - 高峰每秒查詢數 (Peak QPS): 579 QPS \* 3 (高峰因子) ≈ 1,737 QPS (我們可以估算為 約 1,800 QPS)

- Storage Estimation

  - Raw Event Storage - (保留1天): 每日事件數 \* 單一事件大小 = 100,000,000 \* 500 Bytes = 50,000,000,000 Bytes = 50,000 MB = 50 GB / 天
  - Aggregated Count Storage: 這部分儲存需求高度依賴於具體的實現架構（例如，使用 Redis 的 Sorted Sets、時間序列資料庫等）
    - 粗略估計: 我們需要為 500 萬活躍文章維護不同時間粒度（例如分鐘級、小時級）的計數器。
    - 分鐘級計數 (覆蓋最近 1-2 小時): 5M 文章 \* 120 分鐘 \* (Article ID + Counter 大小) -> 幾 GB 級別。
    - 小時級計數 (覆蓋最近 24 小時): 5M 文章 \* 24 小時 \* (Article ID + Counter 大小) -> 幾 GB 級別。
    - 總體來看，用於即時計算的熱數據（計數器）可能需要數十 GB 的快速儲存（如記憶體或 SSD）來保證低延遲查詢。這部分的儲存壓力相對原始事件較小，但對速度要求更高。

- Bandwidth Estimation

  - Ingress Bandwidth - Writes: 高峰 SPS \* 單一事件大小 = 3,500 events/sec \* 500 Bytes/event = 1,750,000 Bytes/sec = 1.75 MB/sec = 1.75 \* 8 Mbps -> 14 Mbps
  - Egress Bandwidth - Reads: 高峰 QPS \* 單一查詢回應大小 = 1,800 queries/sec \* 1 KB/query = 1,800 KB/sec = 1.8 MB/sec = 1.8 \* 8 Mbps -> 14.4 Mbps

- 總結：

  - 寫入峰值: 約 3,500 SPS。
  - 讀取峰值: 約 1,800 QPS。
  - 每日原始事件儲存: 約 50 GB。
  - 熱數據/計數器儲存: 數十 GB (需快速存取)。
  - 峰值頻寬: 入口約 14 Mbps，出口約 14.4 Mbps。

## Core Entities

- Article / News
  - 這代表系統中一篇獨立的新聞報導或內容。它是被分享、追蹤和排名的基本單位。
  - article_id (獨一無二的文章標識符)。其他可能的屬性包括標題、URL、發布時間等，但對於計數系統而言，article_id 是最重要的。
  - 系統角色: 是計數和排名的主要對象。
- Share Event

  - 這代表一篇文章被使用者分享的一次具體動作。這是系統需要接收和處理的主要輸入資料流。
  - 關鍵屬性:
    - article_id: 指向被分享的那篇文章。
    - timestamp: 分享動作發生的精確時間戳。
    - user_id, platform (分享到的平台) 等。
    - 系統角色: 是計數增加的觸發器，系統根據事件的 timestamp 將其歸入相應的時間窗口。

- Time Window
  - 這與其說是一個數據實體，不如說是一個核心的概念和參數，它定義了聚合分享事件和執行查詢的時間範圍。
  - 關鍵方面:
    - 持續時間 (Duration): 問題中明確定義了三種：5 分鐘、1 小時、24 小時。
    - 類型 (Type): 滑動窗口 (Sliding Window)。這意味著窗口的起訖時間是相對於「現在」這個時間點動態計算的（例如，「過去 5 分鐘」），而不是固定的時間區塊。
  - 系統角色: 作為聚合規則和查詢時的關鍵參數，用來界定哪些 分享事件 應該被納入計算範圍。

API or System Interface

- RESTful API

```
GET /trending?window=5m&k=5
GET /trending?window=1h&k=10
GET /trending?window=1d&k=20
```

## High Level Design

- Naive implementation

  - 假設我們在一台超大的server上開始實作
  - 將Share Event存入Kafka裡面(High throughput)
  - 維護一個包含前K個新聞的min heap
  - 維護一個包含article_id和count的cache
  - 當consumer收到share event後，用automatic operation更新cache中count。如果count >= heap[0]（即該新聞屬於前 1,000 名），我們會將其更新/插入到heap中並在總長度>K的時候使用heappop將當下最不熱門的新聞彈出。
  - Cons:
    - Missing Time Window Logic
    - Single Point of Failure - SPOF
    - Low Write Throughput
    - Heap/Cache Contention Point
    - Memory Limitation

- Refinement

  - Distributed Stream Processing Framework

    使用 Apache Flink 或 Apache Spark Streaming。這些框架天生就是分散式的，可以水平擴展處理能力，並內建了處理時間窗口的功能。

    - SPOF: Flink/Spark 運行在叢集上，單節點故障通常可以容忍（需配置高可用）。
    - 處理瓶頸: 可以增加 Flink/Spark 的 Task Manager/Executor 數量和並行度來處理更高的事件速率。
    - 時間窗口: 這些框架的核心功能就是處理各種窗口（滑動窗口 Sliding Windows 最適合此場景）。

  - Implement Time Window Aggregation

    - 在 Flink/Spark 任務中，從 Kafka 讀取 share-events
    - 按 article_id 分組 (keyBy)。
    - 同時定義三個滑動窗口：
      - window(SlidingEventTimeWindows.of(Minutes(5), Seconds(30))) // 5分鐘窗口，每30秒滑動一次
      - window(SlidingEventTimeWindows.of(Hours(1), Minutes(1))) // 1小時窗口，每1分鐘滑動一次
      - window(SlidingEventTimeWindows.of(Hours(24), Minutes(10))) // 24小時窗口，每10分鐘滑動一次 (滑動間隔可以根據即時性需求調整)
    - 在每個窗口內聚合（aggregate）計算分享次數。
    - 核心的時間窗口邏輯問題。框架會自動處理事件時間、窗口觸發和狀態清理。

  - Distributed Cache/Store for Ranking
    - 放棄單機 Heap 和 Cache。改用分散式儲存方案來維護排名，Redis Sorted Set 是絕佳選擇。
    - 為每個時間窗口創建一個 Sorted Set (e.g., trending:5m, trending:1h, trending:24h)。
    - Flink/Spark 任務計算出窗口結果 (window_type, article_id, count) 後，使用 ZADD <set_name> <count> <article_id> 命令更新 Redis 中的分數。Redis 的 ZADD 操作相對高效且原子。
    - 讀取 Top-K 時，使用 ZREVRANGE <set_name> 0 K-1
    - Pros:
      - 寫入吞吐量/競爭: Redis Cluster 可以分散寫入負載，單一 Sorted Set 的操作比單機 Heap 的全局鎖競爭要好得多。
      - 記憶體限制: Redis Cluster 可以將數據分片儲存在多個節點上。
      - SPOF: Redis Sentinel 或 Cluster 提供高可用性。

- Solution:

  - Components 介紹：

    - Event Collector / Ingestion Service: 接收來自各種來源（例如 NewsHub 網站/App 的分享按鈕點擊、可能的第三方平台回饋）的分享事件。
    - Message Queue: 例如 Kafka 或 Google Cloud Pub/Sub。作為事件收集器和處理器之間的中介，提供緩衝、解耦和可靠性，應對流量高峰
    - Stream Processor: 例如 Apache Flink、Apache Spark Streaming 或 Kafka Streams。負責從訊息佇列讀取事件，並根據時間窗口進行聚合計算。
    - Counting & Ranking Store: 用於儲存中間計算結果（例如每個文章在特定時間段內的分享數）以及最終的 Top-K 排名列表。Redis 或類似的記憶體資料庫是常見選擇，因其高效的讀寫和排序功能。
    - Results Cache / Storage: 儲存最終計算出的 Top-K 文章列表，供 API 快速讀取。通常使用 Redis 或 Memcached
    - Trending API: 提供 RESTful API 端點，供 NewsHub 前端（網站/App）查詢不同時間窗口的熱門文章列表。

  - Data Flow:
    - 事件收集: 分享事件（包含 article_id, timestamp 等資訊）被傳送到 Event Collector。
    - 事件注入: Event Collector 驗證過的事件推送到 Message Queue 中的特定主題（例如 share-events）。
    - 事件處理: Stream Processor 訂閱 share-events 主題，讀取分享事件。
    - 時間窗口聚合: 處理器根據 article_id 分組，並應用不同的時間窗口邏輯（例如，5分鐘、1小時、24小時的滑動窗口），計算每個窗口內各文章的分享總數。
    - 排名計算與儲存: 聚合結果（例如 (window_type, article_id, count, window_end_time)）被發送。一個獨立的服務或處理器內的邏輯，利用這些計數來更新Counting & Ranking Store中的 Top-K 列表（例如，使用 Redis 的 Sorted Set）。
    - 快取更新: 最新的 Top-K 列表被寫入 Results Cache。
    - 前端請求: NewsHub 前端向 Trending API 發送請求，查詢特定時間窗口（或全部）的熱門文章。
    - Trending API從 Results Cache 中讀取相應的 Top-K 列表，並返回給前端。

## Deep Dives

- Message Queue

  - Topic: 使用單一主題 share-events 或根據事件類型/來源劃分主題。
  - Partitioning: 考慮按 article_id 進行分區，這樣同一個文章的事件會被同一個串流處理器實例處理，有利於狀態管理和聚合效率。但需注意熱點問題（某些文章分享量遠超其他）。若熱點明顯，可考慮兩階段處理或使用隨機分區。

- Stream Processing & Windowing

  - 滑動窗口 (Sliding Windows): 最適合此場景，因為我們需要持續更新的趨勢。
    - 5分鐘窗口: 大小=5分鐘，滑動間隔=例如10秒或30秒（決定更新頻率）。
    - 1小時窗口: 大小=1小時，滑動間隔=例如1分鐘或5分鐘。
    - 24小時窗口: 大小=24小時，滑動間隔=例如10分鐘或15分鐘。
    - 滑動間隔越小，結果更新越即時，但計算負載越高。
  - 狀態管理: 串流處理器需要維護每個窗口內每個 article_id 的計數。需要可靠的狀態後端（例如 Flink 使用 RocksDB）。
  - 浮水印 (Watermarks): 處理事件時間（event_timestamp）時，需要使用浮水印機制來處理亂序事件和延遲事件，確保窗口計算的準確性。
  - 聚合邏輯: keyBy(article_id) -> window(...) -> aggregate(countFunction)。

- Counting, Ranking & Storage

  - 使用 Redis Sorted Sets:
  - Top-K 查詢: 使用 ZREVRANGE <key> 0 K-1 命令即可高效獲取分數最高（分享最多）的前 K 個 article_id。
  - 資料清理/過期
    - 方法1: 由於滑動窗口會自動移除舊數據，串流處理器的輸出 count 自然反映了當前窗口的計數。只需用最新的 count 更新 Redis 即可。如果某文章在一個窗口內不再有分享，它的計數會變為 0 或不再被輸出，但可能仍留在 Sorted Set 中。
    - 方法2: 可以額外設置一個清理任務，定期移除 Sorted Set 中分數為 0 或長時間未更新的成員。或者，在 ZADD 更新時，如果 count 很低或為 0，可以考慮移除該成員（ZREM）。
    - 方法3 (近似計數/TTL): 對於非常大的資料量，可以考慮使用 HyperLogLog 等近似計數演算法，並為 Redis 中的鍵設置 TTL（Time-To-Live），但這會犧牲一些準確性，且 TTL 與滑動窗口的精確對應較難。基於串流處理器的方法更精確。

- Flink 或 Spark Streaming 中實現Time Window Aggregation

  我們需要即時地統計在「最近 5 分鐘」、「最近 1 小時」和「最近 24 小時」這三個持續移動的時間窗口內，每一篇文章（article_id）被分享的總次數。

  - 基本原理與概念

    - 事件流 (Event Stream): 系統持續接收分享事件 (article_id, timestamp) 的數據流。
    - 事件時間 (Event Time): 這是處理的關鍵。我們關心的是事件實際發生的時間 (timestamp)，而不是事件被處理系統接收到的時間（Processing Time）。這確保了即使事件因為網路延遲等原因亂序到達，計算結果也能反映真實發生情況。
    - 浮水印 (Watermarks): 為了處理事件時間，系統需要知道「時間進行到哪裡了」。Watermark 是一種特殊的記錄，插入到事件流中，表示「不會再有時間戳小於等於 W 的事件到達了」（允許一定的延遲容忍）。Watermark 的進展驅動著窗口的計算和關閉。
    - 按鍵分區 (Keyed Partitioning - keyBy(article_id)): 為了獨立計算每篇文章的分享數，我們必須將事件流按照 article_id 進行分區（或稱 Keying）。這樣，同一個 article_id 的所有事件都會被送到同一個處理實例（Task/Executor），使得狀態管理（計數）變得高效且一致。
    - 窗口 (Window): 將無限的事件流切割成有限的、可管理的片段（稱為窗口），以便在這些片段上進行計算（例如求和、計數）。
    - 狀態 (State): 由於計算是跨越多個事件的（例如一個窗口內的總數），流處理器需要維護狀態（例如每個窗口中每個 article_id 的當前計數）。這個狀態需要是容錯的。

  - 滑動窗口 (Sliding Windows)

    - 為什麼是滑動窗口？ 因為我們需要的是「最近 N 分鐘/小時」的趨勢，這個時間段是隨著當前時間不斷向前移動的。Tumbling Windows會將時間切成不重疊的塊，不適合這種「即時熱門」的需求。
    - 定義 (Size & Slide):
      - Size: 窗口的總時長 (例如 5 分鐘)。
      - Slide: 窗口向前滑動的步長 (例如 30 秒)。
      - Slide < Size。這意味著窗口之間會互相重疊。
    - 窗口的產生與分配:
      - 對於 SlidingEventTimeWindows.of(Minutes(5), Seconds(30))：
        - 第一個窗口可能是 \[00:00:00, 00:05:00)
        - 第二個窗口是 \[00:00:30, 00:05:30) (向前滑動了 30 秒)
        - 第三個窗口是 \[00:01:00, 00:06:00) (再滑動 30 秒)
    - 事件如何分配到窗口？ 一個帶有時間戳 T 的事件會被分配到所有滿足 window_start <= T < window_end 的窗口實例中。例如，一個時間戳為 00:03:10 的事件會同時屬於 \[00:00:00, 00:05:00), [00:00:30, 00:05:30), ..., [00:03:00, 00:08:00) 等多個（在這個例子中是 10 個）重疊的窗口實例。

  - Aggregation within Windows
    - 狀態管理 (State Management):
      - 當 stream 按 article_id 分組後，框架會為 每一個 Key（article_id） 和 每一個活躍的窗口實例 維護一個獨立的狀態。
      - 對於我們的計數需求，這個狀態就是一個Counter。例如，狀態可以想像成一個複雜的、分佈式的 Map：Map<Window, Map<ArticleID, Count>>。
      - 聚合函數 (Aggregation Function):
        - 我們需要的是 count()。
        - 當一個屬於 article_id = A 的事件到達，並且被分配到窗口實例 W 時：
          - 框架查找 (W, A) 對應的當前計數 C。
          - 將計數更新為 C + 1。
          - 將新計數存回狀態。
    - Flink 提供了高效的內建聚合函數（如 sum(), reduce(), aggregate()），可以直接使用或自訂邏輯。aggregate() 函數允許更複雜的聚合，包含初始化累加器、累加每個元素、合併累加器（在某些場景下需要）和提取最終結果。對於簡單計數，可以直接使用 count() 或類似的簡化操作。
  - Triggering

    - 何時計算並輸出窗口的最終結果？這由觸發器 Trigger 決定。
    - 在事件時間處理中，最常見的觸發器是基於 Watermark 的。當 Watermark 的時間戳超過了某個窗口的結束時間 (window_end)，觸發器就會啟動，表示這個窗口接收數據的時間已經結束（或達到了允許的延遲上限）。
    - 觸發時，框架會讀取該窗口的最終狀態（聚合結果），並將其發送到下游。

  - 同時處理多個 Window

    - 在 Flink/Spark 中，你不需要建立多個完全獨立的數據流管道。通常做法是：

      - 讀取 Kafka 源 DataStream<ShareEvent> sourceStream = ...
      - 按 Key 分區 KeyedStream<ShareEvent, String> keyedStream = sourceStream.keyBy(event -> event.getArticleId())
      - 基於同一個 keyedStream 應用不同的窗口定義：

        ```
        // Flink 範例語法 (概念)
        DataStream<ArticleCount> result5m = keyedStream
            .window(SlidingEventTimeWindows.of(Minutes(5), Seconds(30)))
            .aggregate(new CountAggregator()); // 或者 .count() 如果API支持

        DataStream<ArticleCount> result1h = keyedStream
            .window(SlidingEventTimeWindows.of(Hours(1), Minutes(1)))
            .aggregate(new CountAggregator());

        DataStream<ArticleCount> result24h = keyedStream
            .window(SlidingEventTimeWindows.of(Hours(24), Minutes(10)))
            .aggregate(new CountAggregator());
        ```

      - 框架會智能地管理這三個並行的窗口操作，共享底層的 Keyed Stream 和事件處理。每個窗口定義會有自己獨立的窗口分配邏輯、狀態和觸發機制。

- Flink/Spark Streaming Conceptual Internals
  - State Backend: Flink/Spark 需要地方儲存窗口狀態。
    - Flink: RocksDB 是生產環境常用選擇，它將狀態存在本地磁盤，並定期做快照到遠程持久化存儲（如 HDFS/S3）以實現容錯
    - Spark Streaming (DStream/Structured Streaming): 通常依賴於 Checkpointing 機制將狀態寫入 HDFS 或 S3 等可靠存儲
  - Window Assigner: 負責根據事件的時間戳和窗口定義，判斷事件屬於哪些窗口實例。
  - Trigger: 內建的 EventTimeTrigger 會根據 Watermark 的進展來觸發窗口計算。也可以自訂 Trigger 實現更複雜的觸發邏輯（例如，基於處理時間、事件數量等）。
  - State Cleanup: 當 Watermark 遠遠超過窗口的結束時間後，這個窗口的狀態就不再需要了。框架會自動清理過期的窗口狀態，防止狀態無限增長。清理時機由 Watermark 和窗口生命週期管理決定。
  - Fault Tolerance: 通過 Checkpointing/Snapshotting 機制實現。框架定期將所有任務的狀態快照保存到持久化存儲。如果某個節點失敗，可以從最近一次成功的快照恢復狀態，並重新處理快照之後的事件，保證結果的 Exactly-Once 或 At-Least-Once（取決於配置和 Sink 的實現）
