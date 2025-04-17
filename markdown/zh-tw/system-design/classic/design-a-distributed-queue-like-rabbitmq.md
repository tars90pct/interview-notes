# Design a Distributed Queue like RabbitMQ

我們要設計一個Distributed Queue（分散式佇列系統），功能類似於 RabbitMQ。這個系統的核心目標是作為一個Message Broker（訊息中介軟體）。

它的本質是解決應用程式之間的解耦 (Decoupling) 和非同步通訊 (Asynchronous Communication) 問題。
想像一下，系統中有兩類角色：

- 生產者 (Producer)： 產生訊息（例如：訂單建立事件、使用者操作記錄）並將其發送到佇列系統。生產者不需要知道誰會處理這些訊息，也不需要等待處理結果，發送後即可繼續執行自己的任務。
- 消費者 (Consumer)： 從佇列系統中讀取並處理訊息。消費者不需要知道訊息是哪個生產者發送的。

這個佇列系統像一個中間緩衝區 (Intermediate Buffer)，主要解決以下問題：

- Decoupling： 生產者和消費者互相獨立，可以獨立開發、部署和擴展。一方的變更或故障通常不會直接影響另一方。
- Load Leveling / Peak Shaving： 當生產者的訊息產生速率突然高於消費者的處理速率時（例如：促銷活動導致訂單暴增），佇列可以暫存訊息，防止消費者系統被壓垮。消費者可以按照自己的步調處理訊息。
- 非同步處理： 對於不需要立即返回結果的任務（例如：發送郵件、產生報表），生產者可以將任務訊息放入佇列，然後立即響應使用者，由後端的消費者非同步處理，提升使用者體驗和系統吞吐量。
- 可靠性 (Reliability)： 訊息放入佇列後，即使生產者或消費者短暫離線，訊息也不會丟失（如果設計得當），待其恢復後可以繼續處理。

## Functional Requirements

- Message Publishing (訊息發布):
  - Producers 必須能夠透過 API 將 Messages 發布到系統中。
  - 發布時應能指定目標 Exchange 和一個可選的 Routing Key。
  - 訊息應包含 Payload 以及可選的屬性 (例如：持久化標誌、標頭)。
- Message Routing (訊息路由):
  - 需支援 Exchange 的概念。Producers 會將訊息發布到 Exchanges。
  - 需支援 Queue 的概念。Consumers 從 Queues 接收訊息。
  - 系統需支援 Binding 的概念，用於連接 Exchanges 和 Queues。
  - Binding 應基於 Routing Key 或 Message Headers 將訊息從 Exchange 路由到符合條件的 Queue。
  - 至少應支援常見的 Exchange Types：Direct, Fanout, Topic。
- Message Consumption:
  - Consumers 必須能夠透過 API 從指定的 Queue 訂閱或拉取 Messages。
  - 系統應支援將單一 Queue 的訊息分發給多個 Consumers 中的一個（競爭消費模式）。
- Message Acknowledgement:
  - 為了確保可靠傳遞，Consumers 在成功處理訊息後，必須能夠向 Broker 發送 Acknowledgement (確認，簡稱 ack)。
  - 如果 Consumer 處理失敗或崩潰，未被確認的訊息應能被重新傳遞。
  - 應支援 Negative Acknowledgement，允許 Consumer 告知 Broker 訊息處理失敗，並可選擇是否要求重新排隊。
- Queue Management:
  - 應提供 API 或管理工具來創建、刪除、查詢 Queues 及其屬性 (例如：是否持久化、是否自動刪除)。
  - 應提供 API 或管理工具來創建、刪除 Exchanges 和 Bindings。
- Message Persistence (訊息持久性):
  - 系統應提供選項，允許將標記為 Persistent 的 Messages 儲存到磁碟。
  - 與 Durable Queues 結合使用時，這些訊息在 Broker 節點重啟後應仍然存在。
- Dead Letter Queues (死信佇列):
  - 提供一種機制，將無法成功處理（例如：達到最大重試次數）或過期 (TTL - Time-To-Live) 的訊息，自動路由到一個預先配置的 Dead Letter Exchange。
- Message Ordering (訊息排序):
  - 在標準情況下，對於單一 Queue 中的訊息，應保證其按照發布到該 Queue 的順序 (FIFO - 先進先出) 傳遞給單一 Consumer (消費者)。 注意：跨多個 Consumer 或涉及 Sharding 時，排序保證可能更複雜。

## Non-functional Requirements

- Scalability

  系統必須能夠水平擴展 (Horizontally Scalable)，透過增加更多伺服器節點來處理更高的訊息吞吐量、更多的佇列以及更多的併發連接。讀寫操作都應能擴展。

- Availability:

  - 系統必須是高可用的 (Highly Available)。單一節點的故障不應導致整個服務中斷。
  - 應具備 Fault Tolerance (容錯性)，能夠自動從節點故障中恢復。

- Durability:

  當訊息和佇列被標記為持久時，已成功提交到 Broker (代理) 的數據在節點或叢集重啟後必須依然存在。

- Performance:

  - Low Latency : 從訊息發布到可被消費的時間應盡可能短。
  - High Throughput: 系統應能處理大量訊息/秒。具體目標值需根據預期負載確定 (例如：每秒處理數十萬或百萬條訊息)。

- Consistency

  在分散式環境下，需要定義一致性模型。對於佇列狀態的副本之間，可以接受短暫的 Eventual Consistency (最終一致性)，但訊息操作（如確認刪除）應具有較強的一致性保證，以防訊息丟失或重複處理（在 "至少一次" 語義下重複是可能的，但要避免因系統內部不一致導致的異常）。

## Capacity Estimation (容我偷懶跳過一下)

## Core Entities

- Message: 系統中傳遞的基本數據單元。包含：

  - Payload: 實際的訊息內容。
  - Properties/Attributes: 元數據，例如 Routing Key, Headers, Content-Type, Timestamp, Message ID, Priority, Expiration, Persistence 標誌等。

- Queue: 儲存 Message 的緩衝區，等待 Consumer 處理。具有以下屬性：

  - Name: 佇列的唯一識別符。
  - Durability: Durable (持久，Broker 重啟後存在) 或 Transient (短暫，Broker 重啟後消失)。
  - Auto-delete: 當最後一個 Consumer 解除訂閱後是否自動刪除。
  - Exclusive: 是否為宣告它的 Connection 獨佔。
  - Arguments: 其他可選參數，例如 Message TTL, Max Length, Dead Letter Exchange 關聯等。

- Exchange: 從 Producer 接收 Message，並根據 Binding 規則將其路由到一個或多個 Queue。具有以下屬性：
  - Name: 交換機的唯一ID。
  - Type: 決定路由邏輯的類型，如 Direct, Fanout, Topic, Headers。
  - Durability: Durable 或 Transient。
  - Auto-delete: 當不再有 Queue 綁定到它時是否自動刪除。
  - Arguments: 其他可選參數，例如 Alternate Exchange。
- Binding: 連接 Exchange 和 Queue 的規則。定義了 Message 如何從 Exchange 路由到 Queue。包含 Source Exchange, Destination Queue, Routing Key (用於 Direct/Topic Exchange) 或 Header 匹配條件 (用於 Headers Exchange) 等資訊。
- Producer: 將 Message 發送到 Exchange 的客戶端應用程式。
- Consumer: 從 Queue 接收並處理 Message 的客戶端應用程式。
- Connection: Producer 或 Consumer 與 Broker 之間建立的物理網絡連接 (例如 TCP 連接)。
- Channel: 在單一 Connection 內建立的Multiplexing的虛擬連接。大多數操作 (如發布、消費) 都在 Channel 上進行，以減少 TCP 連接的開銷並允許併發處理。
- Broker: 佇列系統的伺服器端應用程式。負責管理 Exchange, Queue, Binding，處理 Message 的接收、儲存、路由和傳遞。在分散式設計中，Broker 由多個 Node 組成。

## API or System Interface

Publish:

- publish(channel, exchange_name, routing_key, properties, body)

Consume

- consume(channel, queue_name, consumer_tag, callback, no_ack, exclusive, arguments)
- ack(channel, delivery_tag, multiple): 對收到的 Message (由 delivery_tag 標識) 發送肯定確認。
- nack(channel, delivery_tag, multiple, requeue): 對收到的 Message 發送否定確認，可選擇是否要求 Broker 將其重新排隊 (requeue)。

## High Level Design

- Core Components

  - Producers: 產生訊息並將其發送到系統的應用程式。
  - Consumers: 從系統訂閱並接收、處理訊息的應用程式。
  - Broker Cluster: 一組相互協調的伺服器節點，負責接收、儲存、路由和分發訊息。這是系統的核心，其分散式特性是關鍵。
  - Coordination Service (e.g., ZooKeeper, etcd): 用於集群成員管理、Leader Election、設定資訊共享、分散式鎖等協調任務。雖然不是絕對必要（有些系統採 Gossip Protocol），但常用於簡化管理。
  - Load Balancers: 在 Broker Cluster 前端，用於分發 Producer 和 Consumer 的連接請求。
  - Queue: 用來儲存當前還沒消化完的訊息

  [TODO: 補一張圖：Producers -> (Load Balancer) -> Broker Cluster <- (Load Balancer) <- Consumers，Broker Cluster，Queue(內部互相連結)，並與 Coordination Service 溝通]

- Mechanism

  - Message Routing

    實現 Producer 發送訊息到 Exchange，Exchange 根據類型（Direct, Fanout, Topic, Headers）和 Bindings（綁定 Queue 與 Exchange 的規則，含 Routing Key）將訊息路由到一個或多個 Queues。

    - Coordination Service: 將 Exchange 定義、Queue 定義、Bindings 等meta data儲存在 ZooKeeper/etcd 中。Broker 節點啟動時載入或訂閱這些元數據的變更。當收到訊息時，Broker 查詢local cached meta data來決定路由路徑。
    - Routing:
      - 當訊息到達任一 Broker 節點（入口點）時，該節點根據訊息指定的 Exchange 和 Routing Key，查找匹配的 Bindings
      - 根據 Binding 找到目標 Queue(s)。
      - 確定負責目標 Queue(s) 的 Broker 節點（基於 Sharding/Partitioning 策略）。
      - 將訊息轉發到對應的 Broker 節點上的目標 Queue

  - Message Publishing / Consumption

    Producers 能可靠地發布訊息，Consumers 能有效地消費訊息。支援多 Producers 和多 Consumers。

    - Publishing

      - Producer 透過 Coordination Service 或專門的服務發現機制找到可用的 Broker 節點，並直接連接(或透過LB連接)。Producer 發送訊息後，需要 Broker 的確認（Acknowledgement）。確認的時機和強度（例如，僅 Leader 接收 vs. 已持久化 vs. 已複製到 N 個副本）影響可靠性和延遲。

    - Consumption

      - Model:
        - Push Model (RabbitMQ): Broker 主動將訊息推送給已連接並訂閱的 Consumer。需要 Broker 管理 Consumer 狀態和流控 (Flow Control)。
        - Pull Model (Kafka): Consumer 主動向 Broker 拉取訊息。Broker 較簡單，由 Consumer 控制消費速率。
      - Multiple Consumers 處理方案:
        - Competing Consumers: 多個 Consumers 訂閱同一個 Queue，Broker 將訊息輪流（或其他策略）分發給其中一個活躍的 Consumer。適用於提高單一 Queue 的處理能力。
        - Partitioning/Sharding: 將一個邏輯 Queue 分割成多個 Partitions/Shards，每個 Partition 通常只由一個 Consumer 實例消費（在 Consumer Group 內）。有利於水平擴展和維持 Partition 內的訊息順序。

  - Message Acknowledgement (Consumer Side)

    確保 Consumer 成功處理訊息後，訊息才從 Queue 中被真正移除，防止 Consumer 失敗導致訊息遺失。

    - Acknowledgement 機制:
      - Automatic Ack: Broker 發送訊息後立即視為已確認。效能好但可靠性低。
      - Manual Ack: Consumer 處理完訊息後，顯式發送 ACK (Acknowledgement) 或 NACK (Negative Acknowledgement) 給 Broker。Broker 收到 ACK 後才將訊息標記為可移除。這是保證「At-Least-Once Delivery」的基礎。
    - Broker 狀態管理:
      - Broker 需要追蹤哪些訊息已被分發但尚未收到 ACK（unacked messages）。這通常需要與 Consumer 的連接狀態綁定。
      - 如果 Consumer 連接斷開，其 unacked 訊息需要被重新排隊（Requeue）以便分發給其他 Consumer。此狀態資訊本身也需要高可用（例如，記錄在 WAL 或複製到其他節點）。

  - High Throughput

    最大化單位時間內能處理的訊息數量。

    - Partitioning/Sharding: 將 Queue 的負載分散到多個 Broker 節點上。是水平擴展的核心。
    - Asynchronous Operations & Non-Blocking I/O: Broker 內部使用異步處理模型（如 Netty, asyncio）避免線程阻塞，提高併發處理能力。
    - Batching: 允許 Producers 批量發送訊息，允許 Consumers 批量拉取/接收訊息。減少網路來回和系統呼叫開銷。
    - Efficient Data Structures: 內部 Queue 的實現（記憶體、磁碟）需要高效。例如，類似 Kafka 的 Log Segment 結構有利於順序讀寫；傳統 Queue 可能需要優化的資料結構。
    - Optimized Replication: 選擇合適的複製策略（同步 vs. 異步，Quorum 寫入）來平衡吞吐量和一致性。

  - Persistence

    訊息在 Broker 重啟或崩潰後不遺失，盡量不犧牲高吞吐量。

    - Write-Ahead Log (WAL):
      - 所有改變狀態的操作（接收新訊息、ACK 訊息）先寫入持久化的 Log 文件，再更新記憶體狀態或執行其他操作。確保即使崩潰，重啟時可從 Log 恢復狀態。
      - 可以group commit / fsync以減少 I/O 次數，提高吞吐量，但會增加一點點訊息持久化的延遲。
    - Message Store:
      - File-based Log + Index: 將訊息本體追加到數據文件（Log Segment），並維護索引文件（例如，基於 offset 或 message ID）以便快速查找。類似 Kafka 的做法，對順序寫友好。
      - Embedded KV Store: 使用如 RocksDB, LevelDB 等嵌入式資料庫存儲訊息及其狀態。提供事務性和索引能力。
      - Dedicated Storage Layer: 可能使用分散式文件系統或對象儲存，但可能引入較大延遲。
    - Persistence 與 Throughput 的平衡:
      - Synchronous fsync: 最高可靠性，確保寫入物理磁碟，但影響吞吐量。
      - Asynchronous fsync / OS Cache: 吞吐量高，但在 OS 崩潰或斷電時可能丟失最後緩存的數據。
      - Replication: 將訊息複製到多個節點的 WAL 或內存中，即使單一節點硬體故障（連同其磁碟），只要其他副本還在，訊息就不會丟失。可以配置成 Producer 等待 N 個副本確認後才算成功，提供不同等級的持久化保證。

  - Support for Multiple Consumers and Producers

## Deep Dives

- 和 Kafka 的比較：

  - 設計理念：
    - RabbitMQ: 傾向於智慧型 Broker (Smart Broker) 的設計。Broker 負責確保消息的可靠傳遞，追蹤每個消息的狀態，並在消息被消費者確認 (ACK) 之前保留消息。
    - Kafka: 傾向於傻瓜型 Broker (Dumb Broker) 的設計。Broker 的主要職責是持久化消息，並不主動追蹤消息的消費狀態。消息的消費進度由消費者自行管理。
  - 消息儲存與持久化
    - RabbitMQ: 通常使用每個佇列 (Queue) 一個或多個內部資料結構來儲存消息。消息的持久化可以透過將消息標記為 durable 並將佇列也設定為 durable 來實現。Broker 會將這些持久化消息寫入磁碟。
    - Kafka: 將所有消息儲存在一個或多個主題 (Topic) 的分區 (Partition) 中。每個 Partition 都是一個有序且不可變的日誌 (Log)。消息的持久化是 Kafka 的核心特性，它會將所有寫入 Partition 的消息都持久化到磁碟。
  - 消息傳遞保證
    - RabbitMQ: 提供多種消息傳遞保證，包括：
      - At most once: 消息可能會丟失，但不會重複傳遞。
      - At least once: 消息至少會被傳遞一次，可能會有重複。
      - Exactly once: 消息只會被傳遞一次，這是最嚴格的保證，需要透過事務 (Transactions) 或生產者確認 (Publisher Confirms) 等機制來實現。
    - Kafka: 主要提供 At least once 的傳遞保證。雖然在較新的版本中也引入了對 Exactly once 的支援，但其實現方式與 RabbitMQ 不同，通常涉及到生產者和消費者的協同。
  - Consumption Model
    - RabbitMQ: 使用 推 (Push) 模型。Broker 會主動將消息推送到已訂閱該佇列的消費者。消費者需要建立一個連線並等待接收消息。
    - Kafka: 使用 拉 (Pull) 模型。消費者主動向 Broker 發送請求，從指定 Topic 的 Partition 中拉取消息。消費者需要自己管理消費的偏移量 (Offset)，以追蹤已經消費的消息。
  - Acknowledgement
    - RabbitMQ: 消費者在成功處理消息後，需要向 Broker 發送確認 (ACK)。Broker 收到 ACK 後才會將該消息從佇列中移除。如果消費者在處理消息過程中失敗或未發送 ACK，消息可以被重新投遞給其他消費者（取決於配置）。
    - Kafka: 消費者透過提交其消費的偏移量來表示已經消費了該消息。Broker 不會追蹤每個消息的消費狀態，而是依賴消費者來管理偏移量。
  - Scalability
    - RabbitMQ: 佇列的擴展通常涉及到叢集 (Clustering) 和鏡像 (Mirroring) 等機制。雖然可以實現高可用性，但在高吞吐量場景下的水平擴展可能相對複雜。
    - Kafka: 從設計上就具有良好的水平擴展性。Topic 可以被劃分為多個 Partition，每個 Partition 可以獨立地被多個 Broker 節點管理。消費者可以透過消費者群組 (Consumer Group) 的方式並行地消費不同 Partition 的消息，從而實現高吞吐量。
  - 使用場景
    - RabbitMQ: 更適合需要複雜路由、可靠性要求高、以及每個消息都需要被精確處理一次的場景，例如任務佇列、命令與控制等。
    - Kafka: 更適合高吞吐量、低延遲的流式資料處理場景，例如日誌聚合、事件追蹤、即時分析等。

- Partitioned Queue

  將一個邏輯 Queue 明確地分割成多個 Partitions。每個 Partition 是一個獨立的、有序的訊息序列，可以看作一個小的、獨立的 Queue。系統將這些 Partitions 分配到不同的 Broker 節點上作為它們各自的 Primary。每個 Partition 同樣會被複製到其他 Follower 節點以實現高可用。

  - Producer 發送訊息時可以指定 Partition Key（例如使用者 ID、訂單 ID），系統根據 Key 將訊息路由到特定的 Partition，或者輪詢、隨機分配。Consumer Group 內的 Consumer 通常會被分配到一個或多個特定的 Partitions 進行消費。
  - Pros: 極大地提高了單一邏輯 Queue 的水平擴展能力和並行處理能力。是 Kafka 等高吞吐量訊息系統的核心設計。
  - Cons: 只保證 Partition 內部 的訊息順序，不保證跨 Partitions 的全域順序。需要更複雜的 Broker 端管理（Partition 分配、Rebalance）和客戶端邏輯（Producer 如何選擇 Partition，Consumer Group 如何協調）

- Fault Tolerance / High Availability

  - Replication: Queue 的數據和狀態需要在多個 Broker 節點上複製（例如，一主多從或基於 Raft/Paxos 的 Quorum 複製）。
  - Leader Election: 對於每個 Queue Partition 或 Shard，需要有 Leader Election 機制（通常依賴 Coordination Service），當 Leader 節點失效時能自動選出新的 Leader。
  - Failover: Producer 和 Consumer 需要能夠處理 Broker 節點故障，並自動重新連接到新的 Leader 或可用的 Broker 節點。

- Persistence Layer - WAL and Message Store

  將訊息和關鍵狀態變更可靠地寫入非揮發性儲存，以便在 Broker 重啟或崩潰後恢復。

  - Write-Ahead Log (WAL) 實作細節:

    任何狀態變更（接收訊息、確認訊息）必須先成功寫入 WAL，才能更新記憶體狀態或向客戶端確認。

    - fsync() 策略: 這是持久性與吞吐量的關鍵權衡點。
      - 每次操作都 fsync(): 最安全，確保數據落到物理磁碟，但磁碟同步操作非常慢，嚴重影響吞吐量。
      - 批量 fsync() (Group Commit): 累積一定數量（N 條記錄）或一定時間（T 毫秒）的 WAL 記錄後，執行一次 fsync()。顯著提高吞吐量，但在上次 fsync 後到系統崩潰（尤其是 OS 崩潰或斷電）之間，可能丟失少量數據。這是常見的折衷方案。
      - 依賴 OS 緩存: 完全不主動調用 fsync()，讓 OS 自行決定何時將頁緩存 (Page Cache) 刷到磁碟。吞吐量最高，但在 OS 崩潰或斷電時數據丟失風險最大。
      - 可配置性: 理想情況下，系統應允許配置 fsync 策略，甚至允許 Producer 指定單條訊息的持久化級別。
    - WAL 文件管理:
      - 分段 (Segmentation): 將 WAL 分割成固定大小的文件段。便於管理和清理。
      - 清理 (Cleanup): 當 WAL 段中的所有記錄對應的狀態都已安全持久化到 Message Store（如果有的話）或已被確認（例如，訊息已被所有 Consumer Group 確認消費），或者數據已成功複製到足夠多的副本，舊的 WAL 段可以被刪除或歸檔。

  - Message Store 選項:

    - Log-Structured Store (e.g., Kafka style):

      - Segment & Index: 訊息追加寫入數據 Segment 文件。同時更新索引文件（例如 Offset -> 物理位置映射）。索引可以是稀疏的（只索引部分 Offset）以節省空間，查找時先定位到索引點，再順序掃描。
      - Compaction & Deletion: 基於時間（保留最近 N 天）或大小（保留總量不超過 M GB）的策略刪除舊的 Segments。對於有 Key 的訊息 (類似 Kafka Topic)，可以執行 Log Compaction，只保留每個 Key 最新的值，刪除舊版本。

    - In-Memory Queue + Backing Store (e.g., Traditional MQ style):
      - 記憶體資料結構: 需要高效能、線程安全的佇列實現（如 ConcurrentLinkedQueue 或更複雜的 lock-free 結構）。可能需要管理記憶體使用，防止 OOM。
      - 何時將記憶體中的訊息寫入獨立的儲存文件？可能是訊息量達到閾值、記憶體壓力大時，或者周期性地進行。這部分寫入可能是隨機 I/O。
      - 狀態管理: 除了訊息本身，訊息的狀態（Visible, Unacked）也需要管理。ACK 操作需要能快速找到並更新訊息狀態，這對資料結構設計提出要求。
      - 恢復: 重啟時，需要讀取 WAL，重建記憶體中的佇列狀態和 unacked 訊息列表。這個過程可能較慢，取決於 WAL 大小和狀態複雜度。
    - Embedded KV Store (e.g., RocksDB):
      - Schema 設計: 如何用 KV 存儲訊息？例如 PartitionID_Offset -> MessagePayload，ConsumerID_MessageID -> AckStatus 等。
      - 利用特性: 可以利用 KV Store 的事務性來原子化更新訊息狀態和 Consumer Offset。利用其內建的快取 (Block Cache) 和索引。
      - 權衡: 增加了對第三方庫的依賴。效能調整依賴對 KV Store 內部原理的理解。可能比專門設計的 Log 結構有更高的 CPU 和 I/O 開銷。

- Message Acknowledgement & Delivery Guarantees

  - 在 Producer、Broker、Consumer 之間提供可靠的訊息傳遞，並明確定義訊息可能丟失或重複的場景。
  - At-Least-Once Delivery (常見)
    - Flow
      - Producer 發送訊息 M。
      - Broker 收到 M，持久化/複製 M，然後向 Producer 發送確認 P-ACK。
      - Broker 將 M 分發給 Consumer。
      - Consumer 處理 M。
      - Consumer 處理完畢，向 Broker 發送確認 C-ACK。
      - Broker 收到 C-ACK，記錄 M 已被處理（例如更新 Offset 或標記刪除）
    - Duplication Points
      - P-ACK 丟失或延遲：Producer 超時未收到 P-ACK，會重發 M。Broker 需具備檢測和處理重複 M 的能力（見下文 Idempotent Producer）。
      - C-ACK 丟失或延遲：Consumer 已處理 M，但 Broker 未收到 C-ACK（或 Broker 記錄 C-ACK 前崩潰），Broker 會認為 M 未被處理，並在 Consumer 恢復或超時後重新分發 M 給同一個或另一個 Consumer。
    - Unacked Message Tracking:
      - Broker 必須為每個活躍的 Consumer 連接（或 Session）維護一個 unacked 訊息列表/狀態。
      - 這份狀態本身需要高可用（例如記錄在 WAL 或複製）。
      - 需要處理 Consumer 連接斷開的情況：將其 unacked 的訊息重新變為 ready 狀態，可以被重新分發。
      - 可以設置 unacked 訊息的超時時間 (Visibility Timeout)，超時後自動重新變為 ready，防止 Consumer 卡死導致訊息永遠不被處理。
  - Exactly-Once Delivery
    - 純粹的端到端 Exactly-Once 非常困難，通常需要 Producer 和 Consumer 共同參與。
    - Idempotent Producer:
      - Producer 為每個發送的訊息（或一批訊息）分配一個唯一的序列號 (Sequence Number or ID)。
      - Broker 記錄每個 Producer Session 最近成功處理的序列號。
      - 當 Broker 收到帶有已處理過（或更舊）序列號的訊息時，直接丟棄並返回成功的 P-ACK（模擬成功處理）。防止 Producer 重試導致的重複儲存。
    - Transactional Messaging:
      - 將訊息的生產/消費與外部系統（如數據庫）的操作綁定在一個原子事務中。
      - Producer 端: "Transactional Outbox" 模式。先將訊息寫入本地數據庫的 outbox 表，與業務操作在同一個事務中。一個獨立進程掃描 outbox 表，將訊息可靠地發送到 Broker，成功後再更新 outbox 表狀態。
      - Consumer 端: 在處理訊息時，將業務操作和 Offset Commit（或訊息 ACK）放在同一個本地事務中。
    - Consumer-Side Deduplication:
      - Consumer 在處理訊息時，記錄下已成功處理的訊息 ID（例如存在數據庫、Redis 或 Bloom Filter 中）。
      - 如果收到重複的訊息（根據訊息 ID 判斷），則直接忽略（但仍需發送 C-ACK）。
  - Negative Acknowledgement (NACK) / Requeue:
    - 當 Consumer 無法處理某條訊息時，可以發送 NACK。
    - Broker 收到 NACK 後的行為可以配置：
      - Requeue: 將訊息重新放回 Queue (或 Partition) 的頭部或尾部，稍後再次嘗試分發。需要小心處理可能導致無限重試的 "毒訊息"(Poison Pill)。
      - Discard: 直接丟棄訊息。
      - Dead Letter Queue (DLQ): 重試 N 次後，如果訊息仍然失敗，將其發送到一個特殊的 "死信佇列"。管理員可以稍後檢查 DLQ 來診斷問題。

- Consumer Group Management & Rebalancing

  將 Topic/Queue 的 Partitions 有效地分配給一個 Consumer Group 內的活躍 Consumers，並在 Group 成員變化時自動調整分配（Rebalance）

  - Components:
    - Group Coordinator: 負責管理 Consumer Group 狀態、處理 Consumer 的加入/離開、執行 Rebalance 算法並通知 Consumers 結果。它可以是 Broker 集群中的一個特殊節點（如 Kafka），或者利用外部 Coordination Service (如 ZooKeeper) 的功能。
    - Consumer Client: 需要實現加入 Group、維持心跳 (Heartbeat)、提交 Offset、以及響應 Rebalance 指令的邏輯。
  - Flow:
    - Join Group: Consumer 啟動時向 Coordinator 發送 JoinGroup 請求。
    - Sync Group / Assignment: Coordinator 收集所有活躍成員，運行 Partition 分配策略（如 Range, RoundRobin, Sticky Assignor），將 Partition 分配給 Consumers。結果通過 SyncGroup 響應發回給各 Consumer。
    - Heartbeat: Consumers 定期向 Coordinator 發送心跳，表明自己還活著。如果 Coordinator 在 Session Timeout 內未收到心跳，會認為該 Consumer 失效，觸發 Rebalance。
    - Offset Commit: Consumers 定期或在處理完一批訊息後，向 Coordinator (或直接寫到 Broker/特定存儲) 提交已成功處理的 Offset。
    - Leave Group: Consumer 正常關閉時應發送 LeaveGroup 請求，可以更快地觸發 Rebalance。
  - Rebalancing 策略與挑戰:
    - "Stop-the-World" Rebalance: 最簡單的方式。Rebalance 期間，整個 Group 的所有 Consumer 暫停處理訊息，直到新的分配方案確定並下發。會導致短暫的消費停頓。
    - Cooperative Rebalancing (Incremental Rebalance - Kafka KIP-429): 旨在減少 Rebalance 期間的停頓。Consumers 不會一次性放棄所有 Partition，而是分階段地釋放和獲取 Partition。更複雜但用戶體驗更好。
    - Sticky Assignor: 盡量在 Rebalance 後保持 Consumer 持有原來的 Partition，減少不必要的 Partition 遷移，有利於保持緩存狀態。
    - 主要挑戰:
      - 減少 Rebalance 的 "Stop-the-World" 時間。
      - 避免因頻繁 Rebalance（例如 Client 不穩定）導致的系統抖動。
      - 確保 Offset 提交與 Rebalance 之間的原子性或一致性，防止因 Rebalance 丟失已處理但未提交的 Offset 狀態。
