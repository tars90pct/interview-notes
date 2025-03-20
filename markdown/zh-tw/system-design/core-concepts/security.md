# Security

在設計生產環境系統時，安全性應為首要考量。雖然系統設計面試通常不會要求深入測試安全細節，但面試官會期待您在適當環節強調安全措施。這意味著您需準備好討論如何從各層級保障系統安全。以下為常見安全議題與應對策略。

## Authentication / Authorization (身份驗證與授權)

- 核心目標：確保 API 僅允許特定使用者或服務存取。
- 實作方案：
  - API 閘道器整合：將驗證邏輯委託給 API 閘道器（如 Kong、Amazon API Gateway）或專業服務（如 Auth0、Okta）。

標準協議支援：使用 OAuth 2.0、OpenID Connect（OIDC）等協議，避免自建驗證輪子。即便有很多細節，通常只要來上一句：「我的 API 閘道器將處理身份驗證（Authentication）與權限授權（Authorization），例如透過 JWT 令牌驗證使用者角色與存取範圍。」就可以應付大部分情況了。

## Encryption

- Encryption in Transit(傳輸中加密)

  - HTTPS：透過 SSL/TLS 加密所有 Web 流量（強制使用 TLS 1.2+）。
  - gRPC：內建支援 SSL/TLS，適用於服務間安全通訊。

- Encryption at Rest(靜態資料加密)

  - 資料庫層加密：
    - 使用支援透明加密（TDE）的資料庫（如 AWS RDS、Azure SQL）。
    - 加密磁碟儲存（如 AWS EBS 加密卷）。

- 應用層加密：
  - 敏感資料（如用戶個資）在儲存前先以客戶端密鑰加密（如 AES-256）。
  - 用戶自主控管密鑰（BYOK）：讓終端用戶管理加密金鑰（如 AWS KMS 自帶密鑰）。

## Data Protection

- 最小權限原則：僅授予必要存取權限（如 AWS IAM 角色細粒度控制）。
- 敏感資料遮蔽：

  - 日誌中隱藏敏感欄位（如信用卡號、密碼）。
  - 使用遮罩處理（如顯示「-**-\***-1234」）。
  - PII masking

- 防護機制

  - 速率限制（Rate Limiting）：
    - 防止 API 被暴力破解或濫用（如每 IP 每秒最多 100 請求）。
    - 工具：NGINX limit_req 模組、Cloudflare WAF。
  - 請求節流（Request Throttling）：
    - 針對高負載 API 動態調整處理速率（如 AWS API Gateway 的 Usage Plan）。

- 漏洞防範案例
  - 情境：createFriendRequest 端點可能洩露用戶關係圖。
  - 解法：
    - 限制回傳資料欄位（如不顯示完整用戶 ID）。
    - 實作圖靈測試（如 CAPTCHA）阻擋自動化爬蟲。

## Auditing & Monitoring

- 日誌記錄：集中儲存與分析存取日誌（如 ELK Stack 搭配 SIEM 工具）。
- 異常檢測：設定規則警示異常行為（如單一用戶短時間大量下載資料）。
- 滲透測試：定期進行安全測試（漏洞掃描）。

## Monitoring

- Infrastructure Monitoring

  監控底層硬體與雲端資源的健康狀態，預警潛在問題。

  - 常見指標

    - CPU 使用率：持續高負載可能需水平擴容。
    - 記憶體使用量：記憶體洩漏（Memory Leak）的早期徵兆。
    - 磁碟 I/O 與空間：避免儲存空間耗盡導致服務中斷。
    - 網路流量：偵測 DDoS 攻擊或頻寬瓶頸。

  - 常用工具
    - Datadog：整合多雲端平台，提供儀表板與告警。
    - New Relic：基礎設施可觀測性（Observability）與效能分析。
    - Prometheus + Grafana：開源方案，適合自建監控系統。

  ::TIPS
  「我們使用 Prometheus 監控 Kubernetes 集群的節點資源，當磁碟使用率超過 80% 時觸發告警，並自動擴展 Persistent Volume。」
  ::

- Service-Level Monitoring

  確保微服務或 API 的效能與可靠性符合 SLA（服務等級協議）。

  - 常見指標

    - Latency
      - 從收到請求到回覆的時間
      - P99 > 500ms
    - Error Rate
      - HTTP 5xx 或自定義錯誤比例
      - 錯誤率 > 1% (5 分鐘滑動窗口)
    - Throughput
      - 每秒處理請求數（RPS
      - 突增 200% 以上
    - Success Rate - 業務邏輯成功處理的請求比例 - < 99.9%

  - 常用工具
    - AWS CloudWatch：監控 Lambda、API Gateway 等服務。
    - Istio Service Mesh：追蹤分散式服務的延遲與錯誤。
    - Sentry：應用錯誤追蹤與即時告警。

  ::TIPS
  實例分析

  - 延遲飆高：可能因資料庫查詢未索引或快取失效。
  - 錯誤率上升：檢查依賴服務（如支付閘道器）是否異常。
    ::

- Application-Level Monitoring

  追蹤用戶行為與業務關鍵指標，驅動產品決策。

  - 常見指標

    - DAU（日活躍用戶）、MAU（月活躍用戶）。
    - 業務轉換率：註冊轉換、付款成功率、購物車放棄率。
    - 自定義事件：功能使用頻率（如「分享按鈕點擊次數」）。

  - 常用工具
    - Google Analytics：網頁流量與用戶行為分析。
    - Mixpanel：進階用戶旅程追蹤與 A/B 測試。
    - Snowplow：開源資料收集管道，適合客製化分析。

  ::TIPS
  「我們在電商結帳流程埋設 Mixpanel 事件，當用戶於付款頁面離開時，觸發客戶服務主動聯繫，並優化流程降低放棄率。」
  ::
