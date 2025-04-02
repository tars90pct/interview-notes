# Design a Key-value Store

Key-Value Store，常被視為分散式雜湊表（Distributed Hash Table, DHT）概念的一種實際應用。其核心模型極為簡單：將一個唯一的「鍵」（Key）與一個特定的「值」（Value）相互關聯。

- 核心特性：

  - 值的靈活性： 系統通常不對value內部結構或資料類型做任何預設假設（schema-less）。值可以是一個非結構化的二進位大型物件（BLOB）、圖片、伺服器名稱、用戶設定，或任何應用程式需要透過唯一鍵來儲存和檢索的任意數據片段。
  - 鍵的唯一性與生成： key是存取對應值的唯一識別符。它通常透過雜湊函數（Hash Function）產生或進行映射定位，因此必須確保其唯一性。設計時需考慮並實作有效的雜湊碰撞（Hash Collision）處理機制。

- 使用建議與大型資料處理：
  - 為了維持高效能（特別是讀取和寫入延遲），通常建議將value的大小保持在相對較小的範圍內（例如，從幾 KB 到幾 MB）。
  - 若需儲存大型檔案（如影片、高解析度圖片），更佳的做法是將這些大型物件存放在專用的物件儲存系統（如 AWS S3、Google Cloud Storage 等）中，然後在鍵值儲存的value欄位僅存放指向該物件的連結（URL 或 URI）或唯一識別碼。

傳統的關聯式資料庫要在分散式環境下，同時兼顧強一致性（Strong Consistency）與高可用性（High Availability）進行水平擴展，往往面臨巨大的技術挑戰與成本。

相比之下，鍵值儲存因其簡單的資料模型、易於水平擴展以及通常對一致性要求（可調整，常選擇最終一致性）的放寬，在高流量、低延遲的應用場景中表現出色。許多大型網路服務（如 Amazon 的 DynamoDB、Facebook 的快取系統、Netflix 的用戶資料等）的核心架構都大量依賴基於主鍵（即 Key）進行快速存取的儲存方式，補充甚至替代了部分傳統線上交易處理（OLTP）資料庫的功能。

常見應用範例包括：

- 會話管理 (Session Management)： 儲存網頁應用的使用者登入狀態。
- 用戶偏好設定 (User Preferences)： 快速存取用戶的個人化設定。
- 購物車 (Shopping Carts)： 暫存用戶的購物清單。
- 排行榜與計數器 (Leaderboards & Counters)： 高效更新和讀取排名或計數。
- 產品目錄快取 (Product Catalogs)： 快取常用商品資訊以加速讀取。
- 即時推薦系統的基礎數據。

進行Funtional Requirement之前可以先提出下列問題與面試官討論一下：

- What is the size of the value stored for each key? -> 10 KB
- Do we prefer our data to be available or consistent? -> available
- Should we design the key-value store to support large datasets? -> Yes
- Should we be concerned about latency? -> Yes

## Functional Requirements

- Get(key)
- Put(key, value)
- Delete(key)
- CAS: Compare-and-Swap
- Batch Put/Get

## Non-functional Requirements

- CAP Theorem
  - Availability
    - 如果系統不可用，每次請求都需要重新查詢資料庫，這將帶來額外的負擔。
    - 為了減少對資料庫的查詢，我們應確保系統具有高可用性。
- Environment Constraints
  - Instance Memory Limitations
  - Network Capacity for Replication (R + W > N Constraint)
- Scalability
  - 不能僅依賴單一節點，當系統分佈於多個服務時，每個服務可能需要不同的快取 (cache)。
  - 需要能夠根據不同地理位置劃分快取，使其適應分散式系統的需求。
- Latency
  - 系統應能夠快速處理所有操作，確保低延遲和高吞吐量。
- Durability
  - LSM Tree
  - Hinted Handoff
- Fault Tolerance
  - Hinted Handoff
  - 當主節點失效時，系統自動將流量切換至健康副本。
  - 需搭配「心跳機制」檢測故障，並觸發 Leader Election（如 Raft 的選舉機制）。
  - Recovery
    - Vector Clocks
    - CRDTs

## Core Entities

- Key, Value
- Hash function

## API or System Interface

- Get(key)
- Put(key, value)
- Delete(key)
- CAS: Compare-and-Swap
- Batch Put/Get

## High Level Design

![img-key-value-store-min.jpg]({{BASEURL}}/markdown/zh-tw/system-design/classic/img-key-value-store-min.jpg "img-key-value-store-min")

- 目標是在系統內實作快取 (Cache)，提升讀取效能並減少對資料庫的查詢負擔。
- 單機版：
  - 以Hash Table 作為快取基礎
    - Pros
      - 提供高效能的 查找 (Get) 和 新增 (Put) 操作。
      - 適合作為 Key-Value 快取的基礎結構。
    - Cons
      - 快取大小有限，無法儲存所有資料。
      - 內存 (Memory) 成本昂貴，需考慮記憶體管理策略。
  - Cache Eviction Policies
    - 當快取達到容量上限時，決定哪些數據應被移除。
    - 沒有唯一標準，策略選擇取決於業務需求。
    - 常見策略
      - LRU (Least Recently Used，最近最少使用)
        - 移除最久未被存取的資料。
        - 適用於大多數一般應用場景。
        - 實作參考一下leetcode (Hash table + double linked list)
      - LFU (Least Frequently Used，最少使用頻率)
        - 移除使用次數最少的資料。
        - 適用於推薦系統，例如影片或熱門內容快取。
      - FIFO (First In First Out，先進先出)
- 分散式版：

  - Partition使用 Consistent Hashing（一致性雜湊）。
    - 原理：將key和節點node映射到一個虛擬環狀空間（hash ring）。
    - Pros
      - 新增或移除節點時，僅需重新映射「鄰近」的資料，避免大規模資料搬移。
      - 均勻分配負載virtual nodes解決熱點問題
  - Shard Allocation Strategy
    - 根據節點數量變化，自動將分片重新分配至適當節點，確保負載均衡（Auto-Rebalance）。
  - Replication

    - Primary-secondary approach
      - 每個分片預設 3 Replication(1 Leader + 2 Followers)
        - Leader：負責處理所有的讀寫請求，所有的操作會先在 Leader Replication上執行。
        - Followers: 負責備份資料，從 Leader 副本同步數據，確保資料不會因為單一節點故障而丟失，若 Leader 失效，Followers 能通過選舉機制升格為新 Leader
      - Raft 共識算法確保副本一致性與 Leader 選舉
        - Quorum 機制（R + W > N）: 平衡資料一致性（consistency）與可用性（availability）
          - N = 資料複本總數（如 3 個節點）。
          - W = 寫入時需確認成功的複本數（Write Quorum）。
          - R = 讀取時需確認成功的複本數（Read Quorum）。
    - Peer-to-peer approach
      - 無固定 Leader：每個節點均能處理讀寫請求
      - 使用一致性哈希（Consistent Hashing）分散數據，節點動態加入或離開時僅影響局部數據。
      - Eventual Consistency
        - 寫入操作只需傳播給部分節點，數據最終在所有副本同步（可能短暫不一致）。
        - QUORUM 策略亦可應用：例如設定W + R > N實現強一致性（犧牲部分可用性）。
      - 衝突處理機制
        - 向量時鐘（Vector Clocks）：記錄不同節點的寫入順序，合併時保留多版本，由應用層解決衝突。
        - Last Write Wins：以時間戳記（Timestamp）決定最新版本，簡單但可能丟失數據。

  - Storage Engine
    - LSM Tree(Log-Structured Merge Tree)
      - 寫入先寫入記憶體 MemTable，滿後轉為不可變的 SSTable 文件。
      - 背景合併（Compaction）減少讀取放大，提升查詢效率。
    - LRU Cache

## Deep Dives

- Data Consistency & Conflict Resolution

  - Data Versioning

    在 Key-Value Store 中，同一個鍵Key可能會被並行地更新多次。資料版本控制是指系統儲存一個鍵的多個數值版本，而不是簡單地用新值覆蓋舊值。

    - 目的： 這是處理「最終一致性」(Eventual Consistency) 系統中寫入衝突的主要機制。當多個寫入同時發生在不同副本上時，版本控制允許系統（或客戶端）之後檢測到這些並行更新，並進行Conflict Resolution。最常見的解決方式是Read Repair，客戶端讀取時發現多個版本，進行合併或選擇，然後寫回一個統一的版本。
    - Vector Clocks或其他邏輯時鐘（如 Lamport Timestamp）來標記每個值的版本，以判斷版本間的因果關係（是先後順序還是並行發生）。如果沒有版本控制，就容易發生Lost Updates的問題。

  - Vector Clocks

    一種用於在分散式系統中追蹤事件因果關係的機制。每個節點維護一個向量 \[node_id -> logical_counter]。

    - 比簡單的時間戳 (Timestamp) 更精確地判斷兩個資料版本之間是否存在因果關係，或者它們是否是並行更新（衝突）。這對於實現資料版本控制和正確的衝突解決至關重要。
    - 運作機制
      - 每個節點 i 維護一個向量時鐘 VC_i。
      - 當節點 i 發生內部事件或進行寫入時，遞增 VC_i\[i]。
      - 當節點 i 發送消息（包含資料及其向量時鐘 VC_i）給節點 j 時，節點 j 收到後：
        - 對於所有 k，更新 VC_j\[k] = max(VC_j\[k], VC_i\[k])。
        - 遞增 VC_j\[j]。
      - 判斷： 如果版本 A 的向量時鐘 VC_A 中的每個元素都小於等於版本 B 的向量時鐘 VC_B 的對應元素（且至少有一個嚴格小於），則 A 是 B 的祖先（A happened before B）。如果無法這樣比較（即 VC_A 在某些維度大於 VC_B，在另一些維度小於 VC_B），則 A 和 B 是並行發生的，需要進行衝突解決。

  - CRDTs: Conflict-free Replicated Data Types

    一種特殊的資料結構，其設計保證了即使在不同副本上進行並行更新，最終也能自動合併成一致的狀態，無需複雜的衝突解決邏輯。

    - 簡化分散式系統的設計，尤其是在需要高可用性和最終一致性的場景下。應用程式開發者不必擔心如何處理寫入衝突，CRDTs 保證了收斂性 (Convergence)
    - 類型： 主要有兩大類：
      - State-based CRDTs (Convergent Replicated Data Types - CvRDTs): 節點間交換整個資料狀態，狀態本身包含合併所需的所有信息。需要一個 merge(stateA, stateB) 操作，該操作需滿足交換律、結合律和冪等性。
      - Operation-based CRDTs (Commutative Replicated Data Types - CmRDTs): 節點間僅交換更新操作。要求操作滿足交換律（或經過設計使其等效於交換）。
    - 計數器 (Counters - G-Counter, PN-Counter)、集合 (Sets - G-Set, 2P-Set)、列表、圖、暫存器 (Registers - LWW-Register) 等。
    - CRDTs 並非萬能，可能不適用於所有資料模型，且某些 CRDTs 的儲存或計算開銷可能較高。

- Replication & Fault Tolerance Strategy

  - Quorum

    在分散式儲存系統中，為了保證資料的一致性和可用性，一份資料通常會有多個副本 (Replicas) 儲存在不同的節點上。定額是指執行讀取或寫入操作時，需要成功回應的最少副本數量。 在允許部分節點故障的情況下，仍能保證讀寫操作的一致性程度。

    - 參數:
      - N: 總副本數。
      - W: 寫入定額 (Write Quorum)。一次寫入操作需要至少 W 個副本確認成功。
      - R: 讀取定額 (Read Quorum)。一次讀取操作需要至少 R 個副本回應。
    - 一致性關係：
      - W + R > N: 強一致性 (Strong Consistency)。保證讀取操作至少能讀到一個包含最新寫入的副本。
      - W + R <= N: 最終一致性 (Eventual Consistency)。讀取可能讀到舊資料，但系統最終會達到一致狀態。
    - 類型：
      - 嚴格定額 (Strict Quorum): 讀寫操作必須在數據的「首選列表」(Preference List) 中的前 N 個節點裡，獲得 R/W 個成功回應。如果首選列表中的節點不足 R/W 個可用，操作失敗。
      - 寬鬆定額 (Sloppy Quorum): （常與 Hinted Handoff 配合）如果首選列表中的節點不足 W 個可用，系統會選擇其他健康的節點（可能不在首選列表中）來臨時接收寫入，以提高寫入可用性。

  - Hinted Handoff(提示移交)

    一種用於提高寫入可用性和持久性的機制，尤其是在使用寬鬆定額的系統中。當一個寫入請求的目標節點（該數據副本的歸屬節點）暫時不可用時，協調者 (Coordinator) 會將該寫入請求發送給另一個健康的節點（通常是首選列表中的下一個，或環上的下一個）。即使部分節點暫時故障，也能成功接收寫入請求，避免寫入失敗。確保數據最終能送達目標節點。

    - 機制：
      - 協調者嘗試向數據的 N 個首選節點寫入。
      - 如果某個首選節點 A 不可用，協調者選擇一個替代節點 D（該節點本身不負責該數據的副本）。
      - 節點 D 接收數據，並儲存一個「提示」(Hint)，標明該數據的真正目的地是節點 A。
      - 當節點 A 恢復運作後，節點 D 會檢測到（或被告知）A 已恢復。
      - 節點 D 將之前代為儲存的數據連同提示發送給節點 A。
      - 節點 A 確認接收後，節點 D 可以刪除本地的臨時數據和提示。
    - Hinted Handoff 是一種盡力而為的機制，如果持有提示的節點 D 在轉交數據給 A 之前也永久故障了，該筆寫入可能丟失（除非 W 已經滿足）。它主要用於處理暫時性故障。

- Data Repair & Synchronization

  - Merkle Tree

    一種雜湊樹 (Hash Tree)。樹的葉節點是數據塊 (Data Blocks) 的雜湊值，非葉節點是其所有子節點雜湊值的雜湊值。根節點的雜湊值代表了整個數據集的狀態。高效地比較兩個副本之間的大量數據，快速找出不一致的部分，而無需傳輸整個數據集。

    - 機制：

      - 兩個副本節點各自計算其數據的 Merkle Tree。
      - 比較兩個樹的根雜湊值。如果相同，則數據一致。
      - 如果根雜湊不同，則遞迴地比較子節點的雜湊值。
      - 沿著樹向下比較，直到找到雜湊值不同的葉節點。這些葉節點對應的數據塊就是不一致的部分。
      - 只需傳輸這些不一致的數據塊來進行同步。

  - Anti-entropy with Merkle Trees

    反熵是分散式系統中用於修復副本之間數據差異、確保最終一致性的後台同步過程。使用 Merkle Tree 是實現反熵的一種高效方法。定期檢測和修復由於節點故障、網路分區、Hinted Handoff 未完成等原因造成的副本間數據不一致。反熵是保證最終一致性的關鍵後台機制。如果沒有反熵，即使有 Quorum 和 Hinted Handoff，數據差異也可能永久存在。

    - 機制：
      - 節點之間定期（或觸發式）地啟動反熵過程。
      - 參與節點交換它們數據範圍對應的 Merkle Tree 的根雜湊。
      - 如果根雜湊不同，它們會交換下一層節點的雜湊，逐步向下比較，直到定位到存在差異的數據塊。
      - 數據從持有較新（或正確）版本的節點流向需要更新的節點。

- Storage Engine

  - LSM Tree - Log-Structured Merge Tree

    一種針對高寫入吞吐量優化的磁碟資料結構。許多現代 Key-Value Store（如 Cassandra, RocksDB, LevelDB）使用 LSM Tree 作為底層儲存引擎。將隨機寫入轉換為順序寫入，大幅提高寫入效能，特別是在使用傳統 HDD 時（對 SSD 也有益處）。

    - 機制：
      - Memtable: 一個在記憶體中的排序資料結構（如紅黑樹、跳表）。所有寫入請求首先進入 Memtable。
      - Commit Log / Write-Ahead Log (WAL): 為了持久性，寫入 Memtable 的同時，操作也會以順序追加的方式寫入磁碟上的 Commit Log。如果節點崩潰，可以通過重播 Commit Log 恢復 Memtable。
      - SSTable (Sorted String Table): 當 Memtable 達到一定大小後，會被「凍結」並以排序好的、不可變的形式刷新 (Flush) 到磁碟上，成為一個 SSTable 文件。
      - 多層級 SSTables: 隨著時間推移，磁碟上會累積多個 SSTable 文件，通常會分層組織（Level 0, Level 1, ...）。
      - Compaction (合併): 後台會定期執行 Compaction 操作，將來自同一層級或不同層級的多個 SSTable 合併成新的、更大的 SSTable。這個過程會：
        - 真正刪除被標記為刪除的鍵。
        - 合併同一鍵的多個版本，只保留最新版本。
        - 保持數據排序。
        - 減少 SSTable 文件數量，優化讀取效能。
    - 讀寫特性：
      - 寫入： 非常快，主要是記憶體操作和順序磁碟寫入 (Commit Log)。
      - 讀取： 可能較慢，因為需要依次檢查 Memtable、Level 0 的 SSTables、Level 1 的 SSTables... 直到找到數據或確認不存在。這個過程稱為「讀取放大」(Read Amplification)。
      - 空間放大 (Space Amplification): 在 Compaction 發生前，舊版本和已刪除的數據仍然佔用磁碟空間。
      - 布隆過濾器 (Bloom Filters) 常被用於快速判斷一個鍵是否可能存在於某個 SSTable 中，如果 Bloom Filter 說不存在，就無需讀取該 SSTable，可以顯著加速讀取不存在的鍵。

- Performance & Operational Considerations

  - Recovery

    指節點在發生故障（如崩潰、重啟）後，重新加入叢集並恢復其狀態的過程。確保節點恢復後，其數據狀態盡可能與故障前一致，並能與其他節點協同工作，維護系統的可用性和數據持久性。恢復過程可能需要較長時間，特別是需要同步大量數據時。快速恢復對於維持高可用性至關重要。

    - 機制：
      - 重播 Commit Log (WAL): 節點啟動時，首先讀取 Commit Log，將其中記錄的、尚未刷新到 SSTable 的寫入操作重新應用到空的 Memtable 中，恢復記憶體狀態。
      - 與其他副本同步 (Anti-entropy): 節點恢復後，其數據可能已經落後於其他副本（因為在它離線期間發生了寫入）。需要啟動反熵過程（使用 Merkle Tree）與其他副本比對數據，拉取差異部分。
      - 處理 Hinted Handoff: 如果該節點在離線前是某些數據的 Hinted Handoff 接收者，它需要將這些數據轉交給真正的目標節點（如果目標節點已恢復）。如果該節點是某些數據的原始目標節點，它需要能夠接收來自其他節點的 Hinted Handoff 數據。

  - Skewed Data / Hotspots(資料傾斜 / 熱點)

    指數據或訪問負載在叢集中的節點之間分佈極不均勻。某些節點（或數據分割區 Partition/Shard）處理的數據量或請求量遠超其他節點。識別和處理這種不平衡對於維持系統整體效能和穩定性至關重要。

    - 影響：
      - 效能瓶頸: 熱點節點成為效能瓶頸，導致相關請求延遲升高甚至超時。
      - 資源浪費: 其他節點可能處於低負載狀態，資源未被充分利用。
      - 可用性風險: 熱點節點更容易過載甚至崩潰。
    - 原因：
      - 資料特性: 某些鍵本身就是熱點（例如，知名用戶的個人資料、熱門商品的庫存）。
      - 分區策略不當: 使用的雜湊函數或分區鍵導致數據分佈不均。例如，按用戶 ID 的首字母分區，可能導致某些字母對應的節點負載過高。
      - 時間序列數據: 如果按時間戳分區，當前時間段的數據總是寫入同一個節點。
    - 緩解策略：
      - 選擇合適的分區鍵和雜湊函數: 確保數據盡可能均勻分佈。一致性雜湊 (Consistent Hashing) 配合虛擬節點 (Virtual Nodes) 有助於此，但不能完全解決熱點鍵問題。
      - 應用層緩存: 在應用程式或緩存層（如 Redis, Memcached）緩存熱點數據的讀取結果。
      - 寫入分片/聚合: 對於熱點寫入，可能需要在應用層進行分片（如給 key 加後綴）或先聚合再寫入。
      - 動態重新分區/拆分: 監控分區負載，當檢測到熱點時，自動拆分過熱的分區，將其數據和負載分散到更多節點。

  - Tail Latency

    指系統回應時間分佈中，延遲最高的那一部分請求（例如，P99 代表 99% 的請求都比這個延遲快，P99.9 代表 99.9%）。評估系統效能穩定性的重要指標。平均延遲 (Average Latency) 可能很低，但如果尾部延遲很高，表示有一小部分用戶或請求經歷了非常糟糕的效能，這會嚴重影響用戶體驗和系統的可靠性感知。

    在分散式 Key-Value Store 中，高尾部延遲可能由多種因素引起：

    - 節點負載不均 (Hotspots / Skewed Data): 某些節點處理過多請求。
    - 背景活動干擾: 如 LSM Tree 的 Compaction、GC (Garbage Collection)、反熵過程。
    - 網路波動: 節點間通信延遲不穩定。
    - 硬體問題: 磁碟慢、CPU 爭用等。
    - 多副本請求: 讀取操作可能需要聯繫多個副本 (Quorum Read)，最慢的那個副本決定了整體延遲。
    - LSM Tree 讀取放大: 讀取需要檢查多個層級。

## 資料來源：

- [www.educative.io](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-key-value-store)
- [Design a Key-Value Store - System Design Mock Interview (with Microsoft Software Engineer)](https://www.youtube.com/watch?v=6fOoXT1HYxk)
- [Design Key-Value Store](https://www.youtube.com/playlist?list=PL1MM4yIzUdPm2L_Lz8gRa_q6ZElgNoArH)
