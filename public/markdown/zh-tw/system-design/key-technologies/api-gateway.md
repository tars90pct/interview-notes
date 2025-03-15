# API Gateway

API Gateway是系統架構的前置調度中樞，特別在微服務架構（microservice architecture）中扮演關鍵角色。其主要功能包含：

- 請求路由：根據路徑（如 /users）、HTTP 方法（GET/POST）或標頭（Header）將請求導向特定微服務。
- 身份驗證與授權：驗證 API 金鑰、JWT，並檢查存取權限。
- 速率限制（Rate Limiting）：防止 API 被濫用（如單一 IP 每秒最多 100 次請求）。
- 日誌與監控：集中記錄請求指標（如延遲、錯誤率）供後續分析。
- 轉換與聚合：將多個微服務回應組合成單一客戶端回應（如 BFF 模式）。

在產品設計類系統設計面試中，建議將API閘道器作為客戶端首要接觸點納入架構圖。面試官通常關注其戰略性定位而非實作細節，但需注意面試重點仍以題目情境為主）。

## 適用場景

- 微服務架構：簡化客戶端與分散式服務的互動。
- 統一安全管理：集中處理驗證、SSL 終止（SSL Termination）。
- 邊界服務（Edge Service）：作為系統與外部網路的第一道防線。
- 範例:
  - Client 發送 GET /products/123 request
  - API Gateway:
    - 檢查JWT有效性
    - 檢查rate limit（如每用戶每秒 10 次請求）。
    - 路由至Product Service。
  - Product Service查詢資料庫並回傳商品詳情。
  - API Gateway 記錄日誌（如請求耗時 150ms）並回傳結果。

## 進階模式

- BFF（Backend for Frontend）：為不同客戶端（Web、Mobile）提供專屬閘道器，客製化回應格式。
- Service Mesh 整合：結合 Istio 等服務網格，實現細粒度流量管理（如 A/B 測試、金絲雀部署）。
- 混合雲路由：將部分請求導向公有雲，部分導向本地資料中心（如合規要求）。

## 優勢

- 簡化客戶端：客戶端只需與單一端點互動，無需知曉後端服務細節。
- 集中管理：統一實施安全策略、監控與版本控制（如 /v1/users 與 /v2/users）。
- 效能：快取常見回應（如商品目錄）、壓縮傳輸資料（如 GZIP）。

## 潛在問題

- 單點故障：需搭配負載平衡器與多區域部署確保高可用性。
- 效能瓶頸：複雜路由邏輯或過度聚合可能增加延遲。
- 過度設計：小型單體系統引入 API Gateway反而增加複雜度。

## 主流技術方案

- 雲端託管服務：AWS API Gateway、Google Apigee
- 開源解決方案：Kong（基於Nginx）、Tyk
- 基礎伺服器改造：早期Amazon曾大規模採用Apache伺服器群集實現閘道器功能，現今亦可透過Nginx反向代理配置實現基礎路由
