# Design an API Rate Limiter

請你設計一個API Rate Limiter，用於控制在特定時間範圍內，用戶或應用程式可以向 API 發送的請求數量。

## Details to know:

- How to identify users to rate limit?
- What algorithm do you use for rate limiting?
- How about in a distributed system - how do you scale this in large distributed website?
- How to make your rate limiter fault tolerant?

## Functional Requirements

- 限制請求速率：系統必須能夠根據預先定義的規則 (例如：每個使用者每分鐘最多 100 次請求)，限制來自特定來源 (如 IP 位址、使用者 ID、API 金鑰) 的 API 請求數量。
- 精確計數：系統必須能在指定的時間窗口內 (例如：每秒、每分鐘、每小時) 準確地追蹤和計算來自每個識別來源的請求數量。
- 執行限制：當來自某來源的請求數量在指定時間窗口內超過其設定的限制時，系統必須拒絕後續的請求。
- 返回錯誤訊息： 對於被拒絕的請求，系統必須返回一個明確的 HTTP 狀態碼 (通常是 429 Too Many Requests)，並可選擇性地包含額外資訊，例如：
  - Retry-After 標頭：告知客戶端何時可以安全地重試請求。
  - X-RateLimit-Limit 標頭：顯示當前時間窗口內的總請求限制。
  - X-RateLimit-Remaining 標頭：顯示當前時間窗口內剩餘的請求次數。
  - X-RateLimit-Reset 標頭：顯示限制重置的時間點 (通常是 Unix 時間戳)。
- 允許正常請求：當來自某來源的請求數量未超過限制時，系統必須允許該請求繼續傳遞到後端的 API 服務。
- 規則可配置性：系統管理員必須能夠定義、修改和移除速率限制規則。規則應能基於不同的標準進行配置，例如：
  - 不同的使用者層級 (如：免費、付費、企業級)。
  - 不同的 API 端點或服務。
  - 不同的請求來源標識符 (IP、API Key 等)。
- 不同的演算法支援
  - Fixed Window
  - Sliding Window
  - Token Bucket
  - Leaky Bucket

## Non-functional Requirements

- High Performance
  - Low Latency：速率限制檢查過程對請求處理時間的增加必須非常小 (例如：毫秒級別)，不能成為系統瓶頸。
  - High Throughput：速率限制器本身必須能夠處理極高的請求量，至少要能承受其保護的 API 的峰值流量。
- High Availability：API rate limiter是關鍵基礎設施，其故障可能導致所有 API 無法訪問或失去保護。系統必須設計為高可用，具備容錯能力，單點故障不應導致整體服務中斷。
- Scalability：系統必須能夠水平擴展，以應對未來流量的增長。當請求量增加時，可以透過增加更多實例來分散負載。
- Accuracy & Consistency
  - 在分散式環境下，計數需要盡可能準確。可以接受最終一致性 (Eventual Consistency)，但在短時間內的誤差應在可接受範圍內，避免嚴重超限或錯誤阻止。
  - 跨多個限制器instance的計數需要保持一致性。
- Low Resource Consumption
  - 每個限制器實例的 CPU 和記憶體消耗應盡可能低，以降低營運成本。

~~Capacity Estimation~~

## Core Entities

- Rule / Policy

  定義一個具體的限制策略

  - Properties:
    - Rule ID: 規則的唯一標識符。
    - Limit: 在時間窗口內允許的最大請求數。
    - Time Window: 時間窗口的持續時間（例如 60 秒）。
    - Key Type / Granularity: 限制的依據（例如 IP, UserID, APIKey）。
    - Target: 規則應用的範圍（例如某個特定 API 端點 /users, 或全局 \*）。
    - Window Type: 時間窗口類型（Fixed, Sliding）。

- Counter / State

  追蹤特定客戶端在特定規則下的當前請求計數。

  - Identifier: 唯一標識一個計數器，通常是 Rule ID 和 Client Identifier 的組合（例如 rule_abc:user_123 或 rule_xyz:192.168.1.100
  - Count: 在當前時間窗口內的已請求次數。
  - Expiry Timestamp / Window Start: 標記當前計數窗口的結束時間或開始時間，用於判斷計數是否應重置或過期。

- Client Identifier:

  代表發出請求的實體，用於區分不同的請求來源。可能是IP 位址字串、使用者 ID、API 金鑰字串。它通常作為 Counter 實體標識符的一部分。

## API or System Interface

- Request Checking Interface

  API Gateway 或後端服務在處理請求前，調用此介面來判斷請求是否應被允許。這通常不是一個公開的 REST API，有可能是一個嵌入在 Gateway/服務中的 函式庫/SDK 調用。或是一個 Gateway/服務對獨立的 Rate Limiter 微服務的內部 RPC/HTTP 調用。

  ```
  function checkRateLimit(
    clientIdentifier: string,  // e.g., "1.2.3.4" or "user_abc"
    ruleContext: object,       // Contextual info like target endpoint
    timestamp: number          // Request timestamp
  ): {
    allowed: boolean,
    limit?: number,            // Current limit for the client
    remaining?: number,        // Remaining requests in window
    resetTime?: number         // Unix timestamp when limit resets
  }
  ```

- Rule Management API

  供系統管理員或自動化腳本管理速率限制規則

  ```
  GET,POST,PUT,DELETE /rules
  ```

~~Optional Data Flow~~

## High Level Design

![image-api-rate-limiter]({{BASEURL}}/markdown/zh-tw/system-design/classic/image-api-rate-limiter.jpg "image-api-rate-limiter")

- Components
  - Rule Engine: 載入並解釋速率限制規則
  - Counter/State Store: 儲存每個客戶端標識符在當前時間窗口內的請求計數或狀態（例如 Token Bucket 的令牌數）。這通常需要一個快速且可共享的存儲（如 Redis）
- Where to put the Rate Limiter ?

  - 嵌入於 API Gateway

    速率限制邏輯作為 API Gateway（例如 Nginx、Kong、Apigee、AWS API Gateway 等）的一個模組或內建功能來執行。

    - Client -> API Gateway (執行速率限制檢查) -> (若允許) Backend Service
    - 適用場景
      - 已使用 API Gateway 的微服務架構。
      - 希望在請求到達後端服務之前就執行限制，以節省後端資源。
      - 標準的速率限制規則（基於 IP、API Key、基本計數）即可滿足需求。
    - Pros:
      - 集中管理： 在單一入口點管理和執行策略。
      - 早期拒絕： 保護後端服務免受過多流量衝擊。
      - 簡化後端： 後端服務無需關心速率限制邏輯。
      - 利用現有設施： 許多 Gateway 產品已內建此功能。
    - Cons:
      - Gateway 依賴： 功能受限於所選 Gateway 產品的能力。複雜或自訂的規則可能難以實現。
      - 潛在瓶頸： Gateway 需要高度可擴展和可用，否則會成為瓶頸或單點故障。
      - 狀態共享： 如果 Gateway 是分散式部署，仍需要外部共享存儲（如 Redis）來同步計數器狀態。

  - Dedicated Rate Limiter Service

    使用一個專門的微服務負責處理速率限制檢查。API Gateway 或後端服務在處理請求時同步調用此服務。

    - Client -> API Gateway -> Rate Limiter Service (檢查) -> API Gateway -> (若允許) Backend Service
    - 適用場景：
      - 需要高度複雜、動態或自訂的速率限制規則。
      - 希望速率限制邏輯與 Gateway 或後端服務完全解耦。
      - 需要獨立擴展速率限制能力。
      - 未使用 API Gateway 或現有 Gateway 不支援所需功能。
    - Pros
      - 高度靈活性： 可以使用任何技術棧實現複雜邏輯。
      - 獨立擴展與部署： 可根據負載獨立擴展，不影響其他服務。
      - 清晰的關注點分離： 職責單一明確。
    - Cons
      - 增加延遲： 引入了一次額外的網絡調用，增加了請求處理延遲。
      - 額外的基礎設施： 需要部署、管理和監控一個新的服務。
      - 關鍵依賴： 成為系統中的另一個關鍵依賴和潛在故障點。

  - Embedded in Application/Service

    速率限制邏輯作為一個函式庫或中間件 (Middleware) 直接嵌入到每個後端服務實例中。

    - Client -> (API Gateway - 可選) -> Backend Service (執行速率限制檢查) -> Service Logic
    - 適用場景：
      - 簡單的單體應用或少數幾個服務。
      - 對檢查延遲極其敏感。
      - 服務本身就是分散式部署，且每個實例可以獨立限制（或使用共享存儲）。
    - Pros
      - 最低延遲： 檢查在本地進行，沒有網絡開銷。
      - 部署簡單： 對於單體應用，無需額外組件。
    - Cons
      - 狀態共享困難： 在分散式環境下，如果沒有外部共享存儲，每個實例的計數是獨立的，無法實現全局限制。
      - 重複實現/管理： 需要在多個服務中引入和管理相同的邏輯。
      - 更新困難： 更新限制邏輯需要重新部署所有相關服務。
      - 違反關注點分離： 業務邏輯與基礎設施邏輯耦合。

- Counter/State Store

  在分散式環境下（多個 Gateway 實例、多個 Rate Limiter 服務實例、或嵌入式但需要全局限制的場景），需要一個共享的、快速的存儲來保存和更新計數器狀態。

  - 常用選擇：
    - Redis: 非常流行，因為它速度快（內存操作）、支持原子操作（如 INCR, SETNX），並且有豐富的資料結構（如 Hashes, Sorted Sets），適合實現各種演算法。
    - Memcached: 速度也很快，但功能相對 Redis 簡單，原子操作支持較弱，通常不直接用於此目的，除非有額外鎖機制。
    - 資料庫: 通常太慢，不適合高頻率的計數器讀寫。

## Deep Dives

- Algorithm

  - Fixed Window Counter

    將時間劃分為固定長度的窗口（例如每分鐘一個窗口：[0:00-0:59], [1:00-1:59]）。在每個窗口內，對來自特定客戶端的請求進行計數。當計數達到閾值時，拒絕該窗口內的後續請求。窗口結束時，計數器重置。

    - 儲存：每個客戶端標識符只需要一個計數器和窗口的起始/結束時間。
    - 適用場景： 對於可以容忍邊界突發流量、要求簡單實現的場景。
    - Pros:
      - 實現簡單，容易理解。
      - 內存效率高（每個鍵只需要一個計數器）。
    - Cons:
      - Burstiness at Boundaries： 在窗口的邊緣，可能允許短時間內超過平均速率兩倍的流量。例如，限制為 100 次/分鐘，用戶在 0:59 發送 100 次，在 1:00 又發送 100 次，相當於在接近 1 秒的時間內發送了 200 次請求，可能壓垮後端。

  - Sliding Window Log

    記錄每個請求的時間戳。當新請求到達時，移除所有早於 (當前時間 - 窗口大小) 的時間戳。然後計算剩餘時間戳的數量。如果數量小於限制，允許請求並記錄其時間戳。

    - 適用場景： 幾乎不用於實際的高流量系統，主要用於理論分析或流量極低的場景。
    - 儲存：需要儲存窗口內所有請求的時間戳列表。
    - Pros:
      - 非常精確，完美解決了固定窗口的邊界問題。
    - Cons:
      - 內存消耗巨大，需要為每個客戶端儲存大量時間戳。
      - 計算成本高，每次請求都需要清理和計數列表。對於高流量場景不切實際。

  - Sliding Window Counter

    這是Fixed Window Counter和Sliding Window Log的折衷。它通常通過維護當前窗口和上一個窗口的計數器來近似計算滑動窗口內的請求數。例如，限制 100 次/分鐘，窗口 60 秒。當請求在 t 時刻到達，它會考慮上一個窗口 (t-60 到 t) 的計數和當前窗口的計數。估算值 = (上一個窗口的計數 \* 上個窗口在當前滑動窗口中的重疊比例) + 當前窗口的計數。

    - 適用場景： 需要較平滑的速率控制，並且能夠接受稍微複雜實現的通用場景。這是很多現代系統採用的方法。
    - 儲存： 通常需要每個鍵儲存當前和上一個窗口的計數以及窗口時間戳。Redis 的 Sorted Sets 也是一種高效的實現方式 (記錄時間戳，計算範圍內的數量)。
    - Pros:
      - 相比固定窗口，顯著平滑了邊界突發流量，更接近真實的速率。
      - 相比滑動日誌，內存和計算效率高得多。
    - Cons:
      - 實現比固定窗口複雜。
      - 仍然是近似值，但通常足夠精確。

  - Token Bucket

    系統維護一個有固定容量 (burst_limit) 的令牌桶。令牌以恆定速率 (rate) 被添加到桶中，直到桶滿為止。每個傳入的請求需要消耗一個令牌才能通過。如果桶中有令牌，則消耗一個並允許請求；如果桶中沒有令牌，則拒絕請求。

    - 適用場景： 希望允許一定程度的突發流量，同時限制長期平均速率的場景。非常常用。
    - 儲存： 每個鍵需要儲存當前令牌數量 (tokens) 和上次令牌補充的時間 (last_refill_timestamp)。
    - Pros:
      - 允許突發流量： 允許客戶端在短時間內以高於平均速率的速度發送請求，直到消耗完桶中的令牌（突發量受桶容量限制）。
      - 控制平均速率： 長期來看，請求速率受令牌生成速率限制。
      - 易於理解和實現。
    - Cons:
      - 需要額外儲存狀態（令牌數和時間戳）。
      - 參數（桶容量和填充速率）需要仔細調整以匹配期望的行為。

  - Leaky Bucket

    請求像水一樣進入一個固定容量的桶中。桶底有一個孔，以恆定的速率 (leak_rate) 處理（漏出）請求。如果請求到達時桶已滿，則該請求被丟棄（溢出）。

    - 適用場景： 需要嚴格保證下游服務接收請求速率恆定的場景，例如處理消息隊列或數據流。
    - 儲存： 可以想像成一個固定大小的先進先出 (FIFO) 隊列。需要儲存隊列大小、當前隊列長度、上次處理時間等。
    - Pros：
      - 平滑輸出速率： 無論輸入請求如何突發，處理請求的速率是恆定的。非常適合保護下游服務，確保其接收流量的速率穩定。
      - 隱含了隊列處理的概念。
    - Cons：
      - 不處理突發流量： 突發請求會被緩存（如果桶未滿）並延遲處理，或者直接丟棄（如果桶滿），而不是像令牌桶那樣允許一定程度的突發通過。
      - 可能增加延遲： 請求需要在隊列中等待處理。

- 針對Counter/State Store的Data Partitioning / Sharding

  - Partition Key: 通常使用速率限制所針對的客戶端標識符（如 user_id, api_key, ip_address）作為分區鍵。
  - Partitioning Strategy:
    - Consistent Hashing/Hash Partitioning
      - 對Partition Key進行hash，然後根據hash value將其映射到一個特定的分區（Shard/節點）。這是最常用的方法。
      - 當增加或移除Partition node時，它能最小化需要重新映射（遷移）的鍵的數量，提高了系統在擴縮容時的穩定性。
    - Range Partitioning
      - 將鍵按範圍分配到不同分區（例如，用戶 ID 1-10000 在分區 1，10001-20000 在分區 2）。實現簡單，但如果鍵分佈不均勻，容易導致熱點分區。對於速率限制的鍵（如 IP 或隨機 API Key）通常不適用。

- Fault Tolerance

  - Limiter Instance Level
    - Redundancy & Load Balancing: 部署多個limiter instance（無論是 Gateway 節點還是獨立服務實例），並在其前端使用負載均衡器。單個實例故障時，流量會自動切換到健康的實例。
    - Stateless Design: 限制器實例本身最好設計成無狀態的，所有必要的狀態（計數器、令牌數）都存儲在外部共享存儲中。這樣，實例故障後，新接管的實例可以立即從共享存儲中讀取狀態。
  - Counter Store Level

    - Primary-Replica Replication
      - 使用 Redis Sentinel 實現。寫操作發送到主節點，異步或同步複製到一個或多個從節點。當主節點故障時，Sentinel 會自動將一個從節點提升為新的主節點 (Failover)。
      - 異步複製可能在故障切換瞬間丟失少量最新寫入的數據（計數可能略微不准）。同步複製則會增加寫延遲。
    - Clustering
      - 使用例如 Redis Cluster，它將數據分片到多個主節點上，每個主節點可以有自己的從節點。單個主節點故障只會影響其負責的分片，並且其從節點可以接管，提供了更高的可用性和擴展性。
    - Degradation Strategy on Total Store Failure (如果整個存儲集群不可用)

      - Fail Open: 允許所有請求通過，適用於速率限制非絕對核心、且後端能短時承受超額負載的場景。
        - Pros：服務不會完全中斷。
        - Cons：可能瞬間壓垮後端服務。
      - Fail Close: 拒絕所有需要檢查的請求。適用於保護極其敏感或昂貴的後端資源。
        - Pros：保護了後端服務。
        - Cons：導致客戶端服務中斷。
      - Caching & Grace:

        在限制器實例本地緩存最近的計數狀態。當無法連接到主存儲時，在短時間內（例如幾秒或一分鐘）基於這個可能過期的緩存數據做決策，或者應用一個非常保守的默認限制。這是一種更優雅的降級方式。

- Redis 如何確保Counter Update這樣的操作具有原子性 (Atomicity)

  - 核心原理：Redis 的單線程命令執行模型，它主要使用單個主線程來處理所有客戶端命令。
    - 命令隊列 (Command Queue): 當多個客戶端（例如，來自不同速率限制器服務實例的請求）同時向 Redis 發送命令時（例如 INCR my_counter），這些命令會被放入一個先進先出 (FIFO) 的隊列中。
    - 單線程處理 (Single-Threaded Execution): Redis 的主事件循環 (Event Loop) 從隊列中一次取出一個命令，並在單個線程中執行它。
    - 阻塞執行 (Blocking Execution - 相對於其他命令): 最關鍵的一點是，當這個單線程正在執行某個命令時（例如 INCR），它不會被中斷去執行另一個客戶端發來的命令。它會完整地執行完當前命令的所有內部步驟（讀取舊值、計算新值、寫入新值）後，才會去處理隊列中的下一個命令。
    - 原子性保證: 正是因為這種串行化的命令執行方式，任何單個 Redis 命令（如 INCR, DECR, SET, GETSET, HINCRBY 等）本質上都是原子的。從外部來看，一個 INCR my_counter 不可能存在一個命令執行到一半（例如剛讀完舊值）時，被另一個修改同一個鍵的命令插入並干擾。
  - 處理更複雜的原子操作：Redis Lua Script

    很多速率限制演算法（例如滑動窗口、令牌桶）需要的邏輯比單純的 INCR 更複雜，可能涉及「讀取當前值 -> 檢查是否超限 -> 如果未超限則增加計數 -> 設置/更新過期時間」等多個步驟。如果將這些步驟作為多個獨立的命令從客戶端發送給 Redis，那麼在這些命令之間就可能被其他客戶端的命令插入，從而破壞原子性。

    - Redis 執行整個 Lua 腳本的過程與執行單個內建命令一樣，也是原子性的。Redis 主線程會完整地執行完腳本中的所有 Redis 命令，期間不會處理任何其他客戶端命令。
    - 開發者可以將速率限制演算法的核心邏輯（讀-判斷-寫）封裝在一個 Lua 腳本中。例如，一個腳本可以接收 key, limit, window_size 等參數，在腳本內部執行 GET, 條件判斷, INCR (如果需要), EXPIRE 等操作，並返回結果（例如是否允許請求）。
    - 保證複雜邏輯的原子性： 將多個操作捆綁成一個不可分割的單元。
    - 減少網絡往返，將多個命令的邏輯放在伺服器端一次執行，減少了客戶端與伺服器之間的通信次數。

- 使用 Redis 在分散式系統中實作 Fixed Window Counter
  - 使用 Redis 的 String 資料類型和其原子性的 INCR 指令。
  - Key 設計: Key 需要包含用戶標識符（如 User ID、API Key 或 IP 地址），以及當前時間窗口的標識符。
    - 對於每分鐘限制，Key 可以是 ratelimit:`<user_id>:<api_endpoint>:<timestamp_of_window_start>`。更常見的做法是直接計算出當前窗口的開始時間戳（例如，取整到分鐘 `current_timestamp // 60`）
    - 或是簡化設計：ratelimit:<user_id>:<rounded_timestamp> (例如 ratelimit:user123:1678886400 代表 2023-03-15 10:00:00 UTC 這個窗口)。
  - 計算細節：
    - 當收到請求時，計算當前時間窗口對應的 Key。
    - 使用 INCR key_name 指令對該 Key 的值進行原子遞增。這個指令會回傳遞增後的值。
    - 檢查回傳的值是否超過了設定的限制 (limit)。
      - 如果超過限制，則拒絕請求。
      - 如果未超過限制，則允許請求。
    - 設定過期時間 (TTL): 為了自動清除過期資料，當第一次對某個 Key 執行 INCR 時（即 INCR 回傳值為 1），需要為該 Key 設定一個過期時間 (EXPIRE 或 PEXPIRE)。過期時間應等於窗口的長度。例如，如果窗口是 60 秒，則設定 EXPIRE key_name 60。這樣，窗口結束後，Redis 會自動刪除這個 Key。
    - 原子性: INCR 是原子操作，這在分散式環境下至關重要，可以避免多個伺服器同時讀取、修改、寫入同一個 Key 時的競爭條件 (Race Condition)。設定 TTL 的步驟最好也與 INCR 一起在一個原子操作中完成（例如，使用 Lua Script），或者在 INCR 之後立即設置，雖然存在極小的可能在 INCR 成功和 EXPIRE 設置之間服務器崩潰導致 Key 永不過期，但在大多數情況下是可接受的。
- 使用 Redis 在分散式系統中實作 Sliding Window Log

  滑動窗口記錄了每個請求的時間戳。當有新請求進來時，會移除窗口時間範圍之外的舊時間戳，然後計算窗口內剩餘的時間戳數量，以判斷是否超過限制。窗口是持續滑動的，例如“過去 60 秒”。

  - 資料結構: 使用 Redis 的 Sorted Set (ZSET)。
  - Key 設計: Key 通常包含用戶標識符和限制的資源。ratelimit:log:<user_id>:<api_endpoint>。
  - Sorted Set 內容:
    - Score: 儲存請求的精確時間戳（例如，毫秒級 Unix 時間戳）。
    - Member: 儲存一個唯一值來代表該請求。為了確保唯一性，通常也使用時間戳，或者時間戳加上一個隨機值 (timestamp:random_value)。由於 Sorted Set 的 Member 必須唯一，如果同一毫秒有多個請求，只用時間戳做 Member 會導致舊請求被覆蓋。使用 timestamp:random 或 timestamp:uuid 可以避免此問題。
  - 計算細節(Lua Script)：

    - 當收到請求時：

      1. 獲取當前時間戳 current_time（毫秒）。
      2. 計算窗口的起始時間 window_start_time = current_time - window_size (例如 window_size = 60000 毫秒)。
      3. 移除過期成員: 使用 ZREMRANGEBYSCORE key_name 0 window_start_time。移除所有 Score（時間戳）小於窗口起始時間的成員。這一步確保了 Sorted Set 只包含當前滑動窗口內的請求記錄。
      4. 獲取當前計數: 使用 ZCARD key_name 獲取 Sorted Set 中目前的成員數量。
      5. 檢查限制: 比較 ZCARD 的結果和設定的限制 (limit)。

         - 如果數量 >= limit，則拒絕請求。
         - 如果數量 < limit：
           1. 添加新請求記錄: 使用 ZADD key_name current_time member_value 將當前請求的時間戳和唯一標識符加入 Sorted Set。member_value 建議使用 current_time:random_element。
           2. 設定 Key 的過期時間 (推薦): 為了清理長時間不活躍用戶的 Sorted Set，可以為整個 ZSET Key 設定一個過期時間，例如 EXPIRE key_name window_size。每次成功添加記錄後更新 TTL。這樣，如果用戶在一個窗口時間內沒有任何請求，整個 Key 會被自動刪除。
           3. 允許請求。

  - Pros
    - 非常精確，完美解決了固定窗口的邊界突發流量問題。
    - 限流效果平滑。
  - Cons
    - 儲存成本較高，因為需要儲存每個請求的時間戳。如果請求量很大，Sorted Set 可能會佔用較多內存。
    - 操作相對複雜，需要使用 Lua Script 保證原子性。

- 使用 Redis 在分散式系統中實作 Sliding Window Log

  這是固定窗口和滑動窗口日誌的一種折衷。它仍然使用固定窗口，但窗口的粒度更細（例如，每秒一個計數器），並且在計算當前速率時，會匯總覆蓋當前滑動窗口時間範圍內的多個小窗口的計數。

  - 資料結構:
    - (Method1) 使用 Redis Hash。Key 是用戶標識符。Hash 的 Field 是細粒度窗口的時間戳（例如，取整到秒），Value 是該秒內的請求計數。
    - (Method2) 使用多個 Redis String Key。類似固定窗口，但 Key 包含更細粒度的時間戳。例如 ratelimit:counter:<user_id>:<timestamp_rounded_to_second>。
  - 計算細節(Lua Script)：
    - 假設滑動窗口為 60 秒，限制 100 次。
    - 當收到請求時，獲取當前時間戳 current_second。
    - 獲取相關計數: 確定過去 60 秒內涉及的所有秒級 Key (例如，從 current_second - 59 到 current_second 對應的 Key)。使用 MGET 一次性獲取這些 Key 的值。
    - 計算總和: 將 MGET 獲取到的所有有效計數（忽略不存在或已過期的 Key）加總。
    - 檢查限制:
      - 如果總和 >= limit，拒絕請求。
      - 如果總和 < limit：
        1. 遞增當前秒的計數: 使用 INCR current_second_key。
        2. 設定過期: 如果是第一次 INCR（返回 1），則設定 EXPIRE current_second_key 60 （或者略大於 60 秒，例如 65 秒，確保在計算總和時它不會過早消失）。
        3. 允許請求。
    - Pros:
      - 相比 Sorted Set，內存佔用通常較少（特別是請求分佈不均勻時）。
      - 比固定窗口更平滑，部分緩解了邊界突發問題（但不如 Sorted Set 精確）。
    - Cons:
      - 仍然不是完全平滑的滑動窗口，在細粒度窗口的邊界可能仍有小的突發。
      - 實作比固定窗口複雜，需要處理多個 Key 或 Hash Field。
      - 如果窗口很大且粒度很細，MGET 或 HGETALL 可能涉及較多 Key/Field，影響性能。
