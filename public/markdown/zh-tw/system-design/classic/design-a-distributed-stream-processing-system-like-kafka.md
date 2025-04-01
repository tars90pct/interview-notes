# Design a Distributed Stream Processing System like Kafka

讓我們先來看看最初在LinkedIn激發Kafka誕生的核心問題。這個問題看似簡單：LinkedIn當時從多個服務中獲取大量日誌資料，包括日誌訊息、指標數據、事件資料，以及其他監控/可觀測性數據。他們希望以兩種方式利用這些資料：

- 建立能即時處理和分析這些資料的線上近即時系統
- 建立能長期處理這些資料的離線系統

多數處理都是為了分析目的，例如分析用戶行為、用戶如何使用LinkedIn等。

這是相當常見的問題，若未曾接觸過，可以舉一個簡單的應用場景：推薦系統驅動。當用戶在LinkedIn搜索某間公司時，廣告引擎應該能即時捕捉這個行為，並在廣告中近即時地向用戶推薦該公司的職缺。而離線系統則可能利用這個資訊，在該公司發布職缺時寄送電子郵件通知用戶。此外，分析團隊還能藉此了解用戶如何搜索公司，以及如何透過LinkedIn平台求職。

問題本身容易理解，但解決方案可能顯得相當複雜。這是由於該問題本身具有多重限制條件和需求，例如：

- 高度可擴展性：熱門產品每天可能產生數十TB甚至數百TB的事件、指標和日誌資料！這需要近乎線性擴展的分散式系統來處理如此高的吞吐量
- 極高流量支援：需輕鬆處理每秒數十萬條訊息。事實上，LinkedIn在2015年的技術部落格就提到每秒約1300萬條訊息的處理量！單一節點根本無法應付，系統必須是分散式架構
- 生產者-消費者模式：需允許「生產者」發送訊息，並讓「消費者」訂閱特定訊息。這點至關重要，因為同一條訊息可能有多個消費者（如我們討論的線上/離線系統），且訊息傳遞通常是非同步的
- 消費自主性：消費者應能自主決定如何及何時消費訊息。例如在討論的案例中，我們需要一個消費者立即處理訊息，另一個則每隔幾小時批量處理
- 簡化設計：訊息具有不可變性（畢竟日誌資料無需刪除），不需要交易式語義或複雜的傳遞保證機制

簡而言之：這是一個超高吞吐量的訊息傳輸系統，重點在於將海量資料從生產者端傳遞到多個消費者端，不需要追求極速傳輸，也無需複雜機制或交易功能，只需最簡潔的方式實現大規模資料傳輸。

使用場景：

- 訊息佇列（Message Queue，MQ）
  - 消費者（Consumer）可以選擇何時從佇列中讀取資料。
  - 訊息可以長時間存在於佇列中，直到消費者讀取。
  - 適合處理異步（Asynchronous）工作，例如工作排程（Job Scheduling）。
  - 也適合需要依照順序處理的場合：當User進入活動服務時，Event Service會將User訊息丟進Waiting Queue，然後繼續處理之前存入Waiting Queue中的訊息。(Ticket Master Waiting Queue)
  - 解耦服務架構：例如Leetcode服務會將使用者上傳的程式碼交至不同的Consumer runtime
- 串流處理（Stream Processing）
  - 接近Real-time的廣告點擊數據統計（Ad Click Aggregator）
    - 當使用者點擊廣告（如 Nike 廣告），該點擊事件會被放入 Kafka 佇列中。消費者（如 Apache Flink）即時讀取該串流數據，並進行累加計算。最終，我們可以向廣告商提供「這則廣告的點擊數據」。
  - Pub/Sub
    - 如果希望一個訊息可以同時被多個消費者處理，則可以使用Pub/Sub模式。
    - 即時通訊（Messenger）和Facebook Live 直播評論

## Functional Requirements

- 數據收集與傳輸
  - 支援日誌、指標、事件等多類型數據格式（JSON/Protobuf/Plain Text）
  - 允許分散式生產者（Producers）跨地域/服務推送數據
  - 單叢集處理能力：每日TB級數據（目標：每秒百萬級訊息）
  - 線性擴展架構，可透過增加節點提升吞吐量
- 訊息傳遞模型
  - Pub-Sub模式
  - 生產者與消費者解耦，允許多消費者群組獨立訂閱相同數據流
    - 即時消費者（Online）：近即時處理（如廣告推薦引擎）
    - 離線消費者（Offline）：批次處理（如每日用戶行為分析
- 數據處理與分析
  - 消費節奏自主性
    - 即時消費者：觸發式處理（如事件驅動架構）
    - 離線消費者：窗口式批次拉取（如每小時同步至Hadoop）
  - 位移管理（Offset Control）
    - 消費者可自主重置讀取位置（如重播歷史數據）
    - 支援自動提交（At-least-once）與手動提交（Exactly-once）語義
- 訊息儲存
  - 系統必須能夠儲存大量的訊息數據。
  - 訊息數據可以是不可變的（Immutable）。
    - 寫入後禁止修改/刪除，確保數據稽核軌跡
    - 基於timestamp的訊息順序性保證
  - 訊息數據的儲存不需要複雜的交易語意。
- 高吞吐量與可擴展性
  - 系統必須支援極高的吞吐量（例如：每秒數十萬至數百萬條訊息）。
  - 系統必須具有高度的可擴展性，能夠處理每日數十至數百TB的數據。
  - 系統必須是分布式系統。
- 系統必須支援非同步訊息處理

## Non-functional Requirements

## Core Entities

- Topics:

  每個 Topic 都被分割成一個或多個Partition。每個分區都是一個有序且不可變的訊息序列。Producers將訊息發布到特定的 Topic，而Consumers則訂閱他們感興趣的Topic，以接收這些訊息。

- Broker:

  擁有那些"Queues"的服務器(不論物理或虛擬)，一個Broker可以管理多個partitions。

- Partition:

  Queue本體。Kafka中訊息儲存的基本單位。每個分區都是一個有序且不可變的訊息序列，以日誌檔案形式(log file)存在。它們基本上是只追加（append-only）的系統，用來存儲訊息。可以將分區看作是日誌檔案（log file），而每條訊息則像是該日誌檔案中的一行（line）。

- Producers:

  針對Topic寫入messages/records，指定一個主題（Topic）、一則訊息、一個可選的鍵（Key）和可選的元數據（Metadata），然後將其發送到Broker。

- Consumers (Consumer groups):

  針對Topic讀取messages/records，它會持續向Broker輪詢關於該主題上的任何訊息。在每次輪詢請求中，消費者會指定它最後接收到的訊息以及其他一些可配置的參數。消費者通常會是消費者群組（Consumer Group）的一部分。一般來說，不是單一消費者監聽一個主題（Topic），而是消費者群組監聽主題。消費者群組由多個消費者組成，與 RabbitMQ 不同，Kafka 的消費者群組允許多個消費者共享一個 Topic，但同一條訊息只會被其中一個消費者處理。

- Messages:
  - 由headers, key, value, timestamp組成

## API or System Interface

- Producer create and publish a message

```
...
const producer = kafka.producer()
producer.send({
  topic: 'topic-name',
  messages: [
    {key: 'key1', value: 'value1'},
    {key: 'key2', value: 'value2'},
  ]
})

```

- When Kafka receives messages from producers:

  - Message中有Partition Key -> 使用Partition Key, 沒有就Round-Robin分配一個
  - 確定Broker(擁有Partition的)，傳送訊息至Broker
  - Broker appends message to correct partition
  - 每則message 都有一個offset

- Consumer reads next message based on offset:
  - consumer會定期的commit當下offset至Kafka。
  - 由於commit offset的特性，當consumer失能時，另外一個consumer便可以接替上一個任務。

```
const consumer = kafka.consumer({groupId: 'group-id'})
consumer.subscribe({topic: 'topic-name'})
consumer.run((message)=>{
  // callback
})
```

## High Level Design

![kafka-1]({{BASEURL}}/markdown/zh-tw/system-design/classic/kafka-1.png "kafka-1")

## Deep Dives

- Scalability

  - 約束條件:
    - Kafka 沒有對message大小的硬性限制（受硬體條件影響）
    - 建議單個message大小不要超過 1MB，以確保最佳效能，避免過度消耗網路或記憶體。
    - 常見錯誤：將完整的媒體檔案（如影片）存入 Kafka
    - 更好的做法：在 Kafka 內部只存儲 S3 URL，而不存影片本身。
    - 在高效能硬體上，單個 Kafka Broker 可存儲 約 1TB 的數據，並可處理約 10,000 條message/秒。
  - 擴展 Kafka 的方法
    - 增加 Broker 數量: 增加伺服器，提升記憶體與磁碟容量，以便儲存與處理更多消息。
    - 選擇適當的 Partition Key（最重要）
      - Partition Key 決定數據如何分佈在 Brokers 上。
      - 選擇不佳的 Key 可能導致 熱分區（Hot Partition），即某些分區流量過載，而其他分區閒置。
      - 良好的 Partition Key 應該能均勻分佈數據。
    - 熱分區（Hot Partition）處理
      - 熱分區問題：如果某個 Key 的數據過於集中，可能導致某個 Broker 負載過高，影響效能。廣告點擊分析的例子來說：
        - 數據格式：User A 點擊了 Ad B
        - 常見做法：根據 Ad ID 進行分區。
        - 問題：如果 Nike 發佈 LeBron James 新廣告，該廣告的流量可能會極度集中在某個分區，導致負載不均。
      - 解決熱分區的方法：
        - 移除 Partition Key（適用於不要求順序的場景）: 若數據無需有序，則可將消息隨機分佈到不同分區。
        - 使用複合 Partition Key（適用於需要保持局部順序的場景）
          - 例如：Ad ID: 隨機數（1~10）: 這樣能確保相同的 Ad ID 數據分佈在 10 個不同分區，降低單一分區的負擔。
          - 也可使用 Ad ID + User ID，或使用 User ID 前綴 來達到分流效果。
      - Backpressure
        - 讓 Producer 檢測 Kafka 負載，若某個分區超載則減慢發送速率。適用於某些場景，但並非所有系統都適用。
    - 雲端Kafka 服務（Managed Kafka Services）
      - 這些服務能自動處理許多擴展問題，如 自動擴展 Broker，但仍需手動選擇 Partition Key。

- Fault Tolerance & Durability

  - PartitionLeader Partition 與 Follower Partition
    - Kafka 叢集由 Leader Partition 和 Follower Partition 組成。
    - Leader Partition：處理讀寫請求。
    - Follower Partition：負責複製 Leader Partition 的數據，當 Leader 故障時可接管。
    - Kafka 叢集設定檔（config file）中有兩個重要參數：
      - acks（確認機制）:決定寫入時需要多少 Follower 確認消息後才能繼續處理下一條消息。
        - acks=all：所有 Follower 需確認，確保最大耐久性（Durability）。
        - acks=1 或更小：僅需部分 Follower 確認，提高效能，但降低耐久性。
      - replication.factor（複製因子）: 決定每個 Partition 需要多少個 Follower 來進行複製。
        - 預設為 3（1 個 Leader + 2 個 Follower）。
        - 增加數值 可提高數據耐久性，但會消耗更多儲存空間。
        - 減少數值 可節省空間，但會降低容錯能力。
  - Consumer 失敗處理
    - 單一 Consumer 故障
      - Consumer 讀取消息後，會提交 offset 給 Kafka。
      - 若 Consumer離線，重新啟動後會從最後提交的 offset 繼續處理。
    - Consumer Group 內有 Consumer 故障
      - Consumer Group 內，每個 Consumer 負責不同的 Partition 範圍。
      - 若某個 Consumer離線，Kafka 會進行 Rebalancing，將該 Partition 分配給其他 Consumer。
  - Offset Commit 時機決定了數據是否可靠處理，請確認任務成功執行後再提交。

- Error & Retries

  - Producer Retry:
    - retries
    - 支持指數退避（Exponential Backoff）：可以設定間隔時間逐漸增長。
    - Idempotent Producer Mode: 確保消息不重複
  - Consumer Retry:
    - Kafka 不內建 Consumer 端的重試機制
    - 常見的重試模式
      - 主題（Topic）架構
        - Main Topic：存放待處理的消息，例如 WebCrawler 需要爬取的 URL。
        - Retry Topic：當 Consumer 失敗時，將消息放入 Retry Topic 重新嘗試。
        - Dead Letter Queue（DLQ）：若超過最大重試次數（如 5 次），消息將被移至 DLQ 供工程師調查。
      - 處理流程
        - Consumer 從 Main Topic 讀取 URL 並嘗試爬取。
        - 若請求失敗，則將 URL 轉存至 Retry Topic，記錄重試次數。
        - Retry Consumer 負責讀取 Retry Topic 並重新執行任務。若重試超過 5 次，則將消息放入 DLQ，不再處理。
  - Dead Letter Queue（DLQ）
    - 失敗超過最大重試次數的消息將存放於 DLQ Topic。
    - 無 Consumer 會讀取 DLQ，消息將長期保留（或定期清除）。
    - 工程師可手動檢查 DLQ，調查失敗原因並進行 Debug。

- Performance Optimizations
  - Batch messages in producer
  - Compress messages in producer
- Retention Poicies
  - retention.ms (default 7 days)
  - retention.bytes (default 1 GB)
- 為什麼訊息代理（Message Brokers）不適用?
  如果你熟悉訊息代理（Message Brokers，如 RabbitMQ、ActiveMQ 等），你可能會認為它們能夠解決這個問題。但實際上，它們並不適用。讓我們以 RabbitMQ 為例，來看看它為何無法滿足需求。

  - Message Batching

    在高吞吐量系統中，消費者一次性拉取多條訊息（批次處理）比逐條拉取更有效率。否則，大部分時間會浪費在網路請求上。然而，大多數訊息代理並非為超高吞吐量設計，因此它們通常不提供良好的批次處理機制。

  - Different consumers with different consumption requirements
    先前的介紹中提到，系統有兩種類型的消費者：

    - 線上系統 需要即時處理訊息
    - 離線系統 可能會處理過去 12 到 24 小時 內的訊息

    這種模式與大多數訊息代理（如 RabbitMQ）不兼容，因為 RabbitMQ 採用推送（push-based）模式，會將訊息立即推送給消費者，而消費者無法決定何時消費訊息。此外，RabbitMQ 的佇列並不適合長時間存儲大量訊息，因為其設計並非針對超大佇列，當佇列變大時，效能會嚴重下降。由於缺乏對消費者的彈性支持（例如批次處理、歷史訊息消費等），再加上主要依賴推送機制，因此很難滿足我們的需求。

  - Small, simple messages
    大多數訊息代理的訊息大小較大，這並非錯誤，而是它們的設計使然。例如：

    - 提供複雜的訊息路由選項
    - 訊息可靠性保證（Message Guarantees）
    - 每條訊息的個別確認機制（Acknowledge per message）

    這些功能導致訊息標頭變得很大。如果訊息數量不多、也不需要存儲，那麼這沒問題。但我們的系統需要高吞吐量並持久化存儲大量訊息，這與典型的訊息代理不符。

  - Distributed high-throughput system

    我們的系統需要支持每秒數十萬甚至數百萬條訊息，單節點無法承受這種負載，因此必須是分散式架構。雖然 RabbitMQ 確實支持分散式叢集（Cluster），但其效能遠低於 Kafka，因為 RabbitMQ 並非為超大規模系統設計。

  - Large Queues

    不同的訊息代理（Message Brokers）對於大規模佇列的支援程度不一，這取決於所使用的訊息代理及其配置。然而，網路上有許多開發者反映訊息代理的佇列大小限制帶來的問題。這是因為大多數訊息代理的設計理念是快速處理和傳遞訊息，而不是長時間存儲大量訊息。當佇列變大時，系統可能會遇到效能下降、延遲增加，甚至訊息丟失的問題。這使得訊息代理無法滿足我們對於高吞吐量和持久化存儲的需求。

## 資料來源：

- [medium](https://medium.com/better-programming/system-design-series-apache-kafka-from-10-000-feet-9c95af56f18d)
- [youtube](https://www.youtube.com/watch?v=DU8o-OTeoCc)
