# Key Technologies

> 系統設計的核心在於**組合最有效的建構模組**來解決問題，因此深入理解常用模組至關重要。多數面試官並不在意您是否熟悉「特定工具」（例如某款佇列方案），只要您能提出可行的解決方案即可。然而，若對某類技術毫無概念（如佇列系統），設計相關系統時將面臨巨大挑戰！

::TIPS
從面試分級的角度，面試官對技術深度的探詢程度與應徵職級成正比：

中階候選人：能粗略描述 ElasticSearch 是「搜尋索引」即可過關。

高階候選人：若無法解釋Inverted Index或討論其擴容機制，可能被視為警示信號。

無論職級，優先**廣度再求深度**！
::

- Core Database

  - Relational Databases

    基於表格結構與 SQL 查詢，支援 ACID 交易（如 PostgreSQL、MySQL）

  - NoSQL Databases

    非結構化資料儲存，強調水平擴展與高可用性（如 MongoDB、Cassandra）

  - Blob Storage

    專用於儲存圖片、影片等非結構化檔案（如 AWS S3、Azure Blob Storage）

  - Search Optimized Database

    針對全文搜索與複雜查詢設計（如 Elasticsearch）

- API Gateway

  作為系統單一入口，處理路由、認證、限流、監控等（如 Kong、Amazon API Gateway）

- Load Balancer

  分配流量至多台伺服器，提升可用性與吞吐量（如 NGINX、AWS ALB）

- Queue

  解耦生產者與消費者，實現非同步處理（如 RabbitMQ、Kafka）

- Streams / Event Sourcing

  以事件序列記錄狀態變更，支援回溯與即時處理（如 Kafka Streams、AWS Kinesis）

- Distributed Lock

  跨多節點的資源互斥存取機制，如 Redis Redlock（基於租約）、ZooKeeper（強一致性）

- Distributed Cache

  跨節點共享熱點資料，降低資料庫負載（如 Redis Cluster、Memcached）

- CDN

  透過邊緣節點快取靜態資源，降低延遲（如 Cloudflare、Akamai）
