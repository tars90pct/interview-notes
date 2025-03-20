# Communication Protocols

通訊協定是軟體工程的重要組成部分，但多數系統設計面試不會深入探討完整的**OSI 模型**，而是聚焦於系統建構時選擇的**協定類型**。通訊協定可分為兩大類：內部協定(Internal Protocols)與外部協定(External Protocols)。

## 內部協定 (Internal Protocols)

適用於微服務架構（涵蓋 90% 以上的系統設計問題），常見選擇：

- HTTP(S)：

  - 優勢：簡單易用、工具生態成熟（如 RESTful API、Swagger）。
  - 場景：低頻率、非即時的服務間通訊（如訂單服務呼叫支付服務）。

- gRPC：

  - 優勢：基於 HTTP/2 與 Protocol Buffers，高效二進位傳輸，支援雙向串流。
  - 場景：高吞吐、低延遲的內部服務通訊（如即時分析、微服務叢集）。

設計原則：避免過度複雜化，上述兩種協定足以應付多數場景。

## 外部協定 (External Protocols)

需考量客戶端如何與系統互動，包含：

- 通訊發起方（客戶端或伺服器端）
- 延遲要求（即時性 vs 非即時性）
- 資料傳輸量（小量參數 vs 大檔案串流）
- HTTP(S)、SSE、WebSocket 已被主流環境原生支援，無需自訂協定。
- 高自訂協定（如 QUIC、MQTT）適用 IoT 或極端效能需求，但增加實作與維護成本。

多數面試情境建議使用標準方案，除非題目明確要求優化傳輸層。

```
是否需要即時雙向通訊？
├─ 是 → WebSocket
└─ 否 → 是否需要伺服器主動推送？
         ├─ 是 → SSE 或 長輪詢（依客戶端相容性）
         └─ 否 → HTTP(S)
```

常見選擇有：

- HTTP(S)

  - 無狀態（Stateless）：每個請求獨立，不依賴前後文。
  - 透過負載平衡器（Load Balancer）輕鬆擴展 API 伺服器。
  - 避免狀態依賴，服務不應假設客戶端狀態（例如會話 Session），需將狀態儲存於外部（如 Redis 或資料庫）。
  - 應用場景: 網頁表單提交、API 呼叫、靜態資源傳輸（如圖片、CSS/JS 檔案）

  ```
  [客戶端] → [負載平衡器] → [API 伺服器叢集] → [資料庫/快取]
  ```

- SSE (Server-Sent Events)

  - 特性
    - 伺服器單向推送更新（基於 HTTP)
    - 使用單一長連線，伺服器主動推送資料
    - Client瀏覽端透過 EventSource 物件監聽
  - 應用場景: 即時通知（如股價變動、新聞推播）

- Long Polling

  - 運作機制
    - 客戶端發起 HTTP 請求。
    - 伺服器**保持連線開啟**，直到有新資料或逾時。
    - 傳送資料後，客戶端立即發起新請求，循環往復。
  - 特性
    - 模擬即時更新，客戶端定期拉取
    - 相容性高：使用標準 HTTP 協定，無需特殊防火牆設定。
    - 相較短輪詢（Short Polling），減少無效請求次數。
  - 應用場景: 舊版瀏覽器相容的即時聊天室

  ```
  [客戶端] ←HTTP長輪詢→ [伺服器]
                ↑
                └─ 監聽資料變更（如資料庫觸發器、訊息佇列）
  ```

- WebSocket
  - 特性:
    - 全雙工通訊，低延遲持久連線
    - 需長時間保持客戶端與伺服器的 TCP 連線
    - 負載平衡器需支援 WebSocket（如 NGINX 的 proxy_set_header Upgrade 設定）
    - 分散式環境需同步連線狀態（如使用 Redis Pub/Sub 跨節點傳遞訊息）
  - 應用場景: 線上遊戲、協作編輯工具、即時交易系統
  ```
  [客戶端] ↔ [WebSocket 閘道器] ↔ [訊息佇列（如 Kafka、RabbitMQ）] ↔ [後端服務]
  ```

![commuication-protocols]({{BASEURL}}/markdown/zh-tw/system-design/core-concepts/communication-protocols-1.png "commuication-protocols")

## 常見問題

- 為何選擇 gRPC 而非 REST？

  - 強調**效能需求**（如 Protobuf 二進位編碼減少頻寬）、支援串流處理

- WebSocket 與 SSE 的差異？

  - WebSocket 為雙向通訊，SSE 僅伺服器推送；SSE 基於 HTTP 更易穿透防火牆。

- 如何處理即時資料同步？

  - 策略組合：WebSocket 處理即時更新 + HTTP 補償查詢（Fallback）
