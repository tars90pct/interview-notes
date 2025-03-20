# Scaling

在許多系統設計問題中，最重要的主題之一是如何處理 scaling。雖然有許多方法可以實現，但面試官必然會希望您了解如何以「Horizontal Scaling」方式擴展系統。Horizontal Scaling 的核心是透過增加更多 machines 來提升系統容量，這與 Vertical Scaling 形成對比——後者是指透過為單一 machine 增加更多資源（如 CPU、記憶體）來提升效能。

- Vertical Scaling vs. Horizontal Scaling

  面試者通常理解：Vertical Scaling 實際帶來的複雜性增量遠低於 Horizontal Scaling。若能預估 workload 並確認在可預見的未來可透過 Vertical Scaling 滿足需求，這通常會是比 Horizontal Scaling 更理想的解決方案。許多系統的 Vertical Scaling 潛力可能超乎預期。

  增加 machines 並非沒有代價。擴容時常迫使您處理 **work distribution、data distribution 與 state management** 等問題，這類議題在系統設計面試中經常成為警示信號，因此值得深入探討。

  ::TIPS
  經驗不足的面試者常犯兩種錯誤：

  (1) 過度傾向使用 Horizontal Scaling 解決所有效能問題（即使非必要）

  (2) 未考慮 Horizontal Scaling 對系統其他部分的影響。

  當遭遇 scaling bottleneck 時，務必確認問題根源並非來自 poor design（而非單純依賴增加 machines 掩蓋問題）。
  ::

若確定需採用 Horizontal Scaling，則需規劃如何分配 work 至多台 machines。現代系統多使用「Consistent Hashing」技術——此方法將 data 與 machines 排列於環狀的 hash ring 空間中，使增減 machines 時僅需 minimal data redistribution，成為處理分散式 work distribution 的常見方案。

- Horizontal Scaling 實務範例(low level design)：

  - Kubernetes (k8s) 實現 Horizontal Scaling

    在 Kubernetes 中，Horizontal Scaling 主要透過兩種機制實現：

    - HPA (Horizontal Pod Autoscaler)
      根據 CPU、Memory 或自定義指標（Custom Metrics），自動調整 Pod 的數量。

      1. 定義 Deployment 或 StatefulSet 的資源請求（如 requests.cpu）。
      2. 建立 HPA 規則
      3. 當超過HPA 規則時，自動增加 Pod 數量。詳見[horizontal-pod-autoscale](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

    - Cluster Autoscaler

      當節點（Node）資源不足時，自動擴展 Kubernetes 集群的節點數量（例如 AWS 的 Auto Scaling Group）。

  - AWS EC2 實現 Horizontal Scaling
    在 EC2 架構中，透過 Auto Scaling Groups (ASG) 實現：

    - 定義 Launch Template（指定 AMI、Instance Type 等）。
    - 設定 Scaling Policy（例如基於 CPU 使用率或 Network In/Out）。
    - 操作範例：
      1. 建立 Auto Scaling Group，設定最小/最大實例數（如 min=2, max=10）。
      2. 綁定 CloudWatch Alarm，當 CPU > 70% 觸發擴展（Scale-out）。
      3. 新增實例時，自動註冊到 Load Balancer（如 ALB/NLB）。
      4. 進階策略有 Predictive Scaling(基於歷史流量預測擴展)，Mixed Instances Policy(混合不同 Instance 類型降低成本)

  - AWS Lambda 實現自動擴展

    適用場景為短時間高流量的 Event-Driven 任務（如 API 請求、檔案處理）。

    - Lambda 是 Serverless 服務，天然支援 Horizontal Scaling，Lambda 根據請求量自動並行啟動多個執行個體（Instances）。
    - 預設帳戶層級並行限制（Concurrent Executions）為 1,000，可申請提高。
    - 透過 Reserved Concurrency 控制單一函數的最大並行量。

- 通用設計原則

  - Stateless 設計：確保服務無狀態，避免擴展時產生資料不一致問題。
  - 搭配 Load Balancer：均勻分配流量至新擴展的實例（如 ALB、Nginx）。
  - 監控與回退機制：

    - 監控指標（如 Latency、Error Rate）防止過度擴展。
    - 設定冷卻時間（Cooldown Period）避免震盪（Thrashing）。

- 常見陷阱

  - 冷啟動（Cold Start）：Lambda 或 Kubernetes 新 Pod 啟動可能增加延遲。
  - 資料一致性：擴展時需處理 Shared State（建議用 Redis/DynamoDB 等外部儲存）。
  - 成本控制：自動擴展可能導致意外費用，需設定預算警報（如 AWS Budgets）。

- Work Distribution

  Horizontal Scaling的第一個挑戰在於如何將工作正確分配至特定機器。實務上通常透過 Load Balancer（負載平衡器）實現，由它決定將傳入的請求分配至集群中的哪個節點。儘管 Load Balancer 支援多種分配策略（例如 least connections（最少連線）、utilization-based（基於使用率）等，但簡單的 round-robin通常已足夠。對於非同步任務型工作（asynchronous jobs），則常透過 Queueing System（佇列系統）處理。

  - Round-Robin：輪流分配請求，適合無狀態服務。
  - Least Connections：優先分配至當前連線數最少的節點。
  - Hash-Based：基於請求特徵（如用戶 IP、Session ID）固定分配至特定節點。

  工作分配需**盡可能保持系統負載均衡**。例如，若使用 hash map 將工作分配至多個節點，可能會因請求分布特性導致某個節點承受不成比例的工作量。系統的可擴容性最終取決於能否有效緩解此問題——若某個節點處於 90% 忙碌狀態，而其餘節點僅 10% 忙碌，則 Horizontal Scaling 的效益將大打折扣。「平均負載」可能掩蓋個別節點的極端值，需同步觀察「尾部延遲」（Tail Latency）

  - Load Balancer 定期收集節點負載指標（如 CPU、記憶體），動態調整分配權重。
  - Consistent Hashing： 減少節點增減時的資料搬移量，同時平衡負載分布。
  - Sharding：將資料或任務按規則Sharding（如按用戶 ID 範圍），確保各節點處理量均衡。

- Data Distribution

  在Horizontal Scaling系統中，還需考量如何將資料分布至各節點。對於某些系統，這可能意味著將資料保留在處理請求的節點記憶體中；更常見的做法是將資料儲存在所有節點共享的資料庫中。設計時應尋找資料分區（Partitioning）方法，使單一節點能直接存取所需資料，無需與其他節點通訊。若必須跨節點協調（此概念稱為fan-out），**應盡量減少協調次數**。常見的反模式是讓請求fan-out至多個節點，再將結果彙整（即「Scatter-Gather」模式）。此模式可能導致以下問題：

  - 網路流量激增：大量跨節點通訊增加延遲與頻寬成本。
  - 容錯性脆弱：任一節點失敗可能導致整體請求失敗。
  - 尾部延遲（Tail Latency）：最終結果需等待所有節點回應，最慢節點決定整體延遲。

  ::TIPS
  若系統設計涉及地理分布，通常可透過 地理分區（如 REGION_ID） 實現擴容。例如，美國用戶僅需存取當地資料，與歐洲資料無關，此分區策略能有效降低跨區域資料同步需求。
  ::

  Horizontal Scaling本質上會引入資料同步問題：

  - 共享資料庫：讀寫需透過網路傳輸（理想延遲約 1-10ms）。
  - 多副本冗余：各節點維護資料副本，需解決Race Conditions與Consistency問題。

  多數資料庫系統內建機制（Transactions）可部分解決此類問題。其他情況下，可能需使用 分散式鎖（Distributed Lock）。無論採用何種方案，需明確說明如何維持**資料一致性**。常見的同步機制有分散式鎖（如 Redis Redlock），可以協調跨節點資源存取。或是採用2 phase commit，確保跨節點操作原子性。

  Partitioning：

  - Range Partitioning：按資料鍵值範圍分配（如時間戳、ID區間）。
  - Hash Partitioning：透過hash function均勻分布資料。
  - Geographical Partitioning：按用戶位置就近儲存資料。

  Consistency：

  - Strong Consistency：確保所有節點即時同步，適用金融交易等場景。
  - Eventual Consistency：允許短暫不一致，適用高吞吐量系統（如社交媒體）。
