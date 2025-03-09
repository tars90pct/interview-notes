# CAP Theorem

CAP 定理是分散式系統的基礎理論，主張系統最多只能同時滿足以下三項特性中的兩項：Consistency（一致性）、Availability（可用性） 與 Partition Tolerance（分區容忍性）。實務上，由於網路分區（Network Partition）不可避免，通常需在 Consistency 與 Availability 之間做出取捨。

- 選擇 Consistency：
  系統所有節點隨時保持資料一致性。寫入操作後，所有後續讀取（無論從哪個節點）都會返回最新值。然而，在網路分區期間，為維持一致性，部分節點可能暫時不可用。

- 選擇 Availability：
  所有請求皆能獲得回應（即使發生網路分區），但不同節點可能短暫存在資料不一致。系統最終會收斂至一致狀態（Eventual Consistency），但無法保證收斂時間。

在系統設計面試中，Availability 應作為預設選擇，僅在「讀取過時資料不可接受」的場景才需強一致性（Strong Consistency）。需要強一致性的系統範例：

- 庫存管理系統：需精確追蹤庫存以避免超賣。
- 限量資源預訂系統（如機位、活動票券、飯店房間），需防止重複預訂。
- 銀行系統：帳戶餘額需跨節點一致，防止金融詐欺。

此類系統的共同特徵是任何不一致（即使短暫）都可能導致嚴重業務或技術問題。

::TIPS
無需強制整個系統採用單一的一致性模型。不同功能通常有不同需求——例如在電商系統中，商品描述可採用最終一致性（Eventually Consistent），而庫存數量與訂單處理則需強一致性（Strong Consistency）以預防超賣問題。

根據業務邏輯劃分一致性需求，而非技術限制。
::

CAP模式

- CP 系統(犧牲 Availability)：
  - PostgreSQL Streaming Replication: 主節點（Primary）同步資料至備用節點（Standby），寫操作需等待多數節點確認。若主節點與備用節點發生分區，系統可能拒絕寫入以維持一致性，導致短暫不可用。
  - MongoDB(Stream replica-set limitation): 寫操作需由多數派（Majority）節點確認才算成功。若主節點（Primary）與多數派節點分離，剩餘節點無法選出新主節點，寫入操作暫停（犧牲 Availability）。讀取可設定從次節點（Secondary）回應，但可能讀到舊資料（需明確設定讀偏好）。
- AP 系統(犧牲 Consistency)：

  - 核心特性：在網路分區發生時，犧牲一致性（Consistency），優先保證可用性（Availability）與分區容忍性（Partition Tolerance），允許資料短暫不一致（最終一致性）。
  - Cassandra
    - 分散式架構：無主節點（Masterless），所有節點平等，資料按一致性雜湊（Consistent Hashing）分布。
    - 可設定寫入成功的最低節點數（如 QUORUM），但即使部分節點不可用，仍允許寫入其他節點（犧牲即時一致性）。
    - 資料衝突透過「最後寫入勝出」（Last Write Wins, LWW）或手動解決。
  - Dynamo DB
    - Serverless 設計：自動分區與擴容，預設為最終一致性（Eventual Consistency）。
    - 可設定讀取時要求強一致性，但可能增加延遲或降低可用性（與 AP 預設行為矛盾）。
    - 分區發生時，各分區繼續服務請求，但跨分區資料同步延遲，導致暫時不一致。

- CA 系統(僅在單一節點成立)：單體資料庫（如 MySQL 單節點）
