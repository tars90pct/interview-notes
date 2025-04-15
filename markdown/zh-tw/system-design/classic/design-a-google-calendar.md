# Design a Google Calendar

設計一套具備可擴展性(scalable)與高可用性(highly available)的日曆服務系統，功能類似 Google Calendar。該系統需提供使用者建立、管理及共享行程事件的功能，並支援事件邀請機制。服務架構須能承載大量使用者與高頻次事件操作，同時提供跨平台一致性體驗（含網頁端與行動裝置）。

事件資料結構應包含：標題(Title)、描述(Description)、起訖時間(Start Time/End Time)、地點(Location)、參與者列表(Attendees)、提醒設定(Reminders)，以及週期性規則(Recurring Rules)。每位使用者可建立多個獨立日曆(Calendar)，並具備彈性分享權限設定，可針對完整日曆或單一事件進行分享。系統核心功能需內建多時區(Time Zone)自動轉換支援，確保跨區域使用者能準確同步行程資訊。

## Functional Requirements

- Calendar Management
  - 每個使用者可以擁有多個日曆（例如：個人、工作、家庭）。
  - 建立、修改、刪除日曆。
  - 設定日曆的預設屬性（如顏色、時區）。
- Event Management:
  - CRUD 操作: 建立 (Create)、讀取 (Read)、更新 (Update)、刪除 (Delete) 事件。
  - 事件屬性:
    - 標題 (Title)
    - 開始時間 (Start Time) 和結束時間 (End Time) / 全天事件 (All-day event)
    - 時區 (Timezone)
    - 描述 (Description)
    - 地點 (Location)
    - 附件 (Attachments) - (可選，視範圍而定)
    - 顏色標籤 (Color tagging)
- Recurring Events: 支援設定重複規則（每日、每週、每月、每年、自訂規則）以及處理例外的修改或刪除。
- Reminders/Notifications: 使用者可以為事件設定提醒（例如：事件前 10 分鐘、1 小時），透過 Email、Push Notification 或 In-app Alert 等方式發送。
- Attendee Management

  - 邀請其他使用者參加事件。
  - 參與者可以回覆邀請 (RSVP: Yes, No, Maybe)。
  - 事件創建者或有權限者可以看到參與者的回覆狀態。
  - 檢查參與者的空閒/忙碌狀態 (Free/Busy check) 以便安排會議（需考慮隱私）。

- Calendar & Event Sharing

  - 使用者可以將自己的日曆或特定事件分享給其他使用者或群組。
  - 設定分享權限（例如：僅查看空閒/忙碌、查看所有事件詳情、可修改事件、可管理分享設定）。

- Timezone Support: 正確處理和顯示不同時區的事件。

## Non-functional Requirements

- CAP Theorem
  - High Availability: 系統需要接近 100% 的運行時間（例如 99.99%），因為日曆是核心生產力工具。需要設計容錯機制 (Fault Tolerance) 和冗餘 (Redundancy)
  - Consistency:
    - 對於使用者自己的操作（如新增/修改事件），應盡可能提供強一致性 (Strong Consistency) 的體驗，修改後應立即看到結果。
    - 對於涉及多人的操作（如邀請回覆的更新、共享日曆的變更），可以接受最終一致性 (Eventual Consistency) 以換取更高的可用性和效能，但延遲應盡可能短。
- Scalability
  - 系統需要能夠水平擴展 (Horizontally Scalable) 以支援數億使用者和數十億級別的事件。讀取和寫入操作都需要能擴展。
- Performance/Low Latency
  - 讀取日曆事件（例如載入月視圖）應該快速完成（例如 < 200ms）。
  - 建立或更新事件的操作也應該有較低延遲。
  - 搜尋操作的延遲可在可接受範圍內（例如 < 1 秒）。
- Durability: 使用者的日曆和事件資料絕對不能遺失。需要可靠的資料儲存和備份策略。
- Security:
  - 保護使用者資料隱私，防止未經授權的存取。
  - 安全的認證 (Authentication) 和授權 (Authorization) 機制。

## Capacity Estimation

## Core Entities

- User

  - UserID: 使用者的唯一識別碼。
  - Email: 使用者 Email (通常用於登入和邀請)。
  - Name: 使用者名稱。
  - Preferences: 使用者偏好設定（例如：預設時區 DefaultTimezone, 語言 Language, 通知設定 NotificationPreferences）。
  - AuthenticationInfo: 認證相關資訊（可能由獨立的認證服務管理）。

- Calendar

  - CalendarID: 日曆的唯一識別碼。
  - OwnerUserID: 擁有此日曆的使用者 UserID。
  - Name: 日曆名稱（例如："工作"、"個人"）。
  - Description: 日曆描述。
  - Color: 日曆在 UI 上顯示的顏色。
  - DefaultTimezone: 此日曆事件的預設時區。
  - AccessPermissions: 誰可以存取此日曆以及權限等級。

- Event

  - EventID: 事件的唯一識別碼。
  - CalendarID: 此事件所屬的日曆 CalendarID。
  - CreatorUserID: 建立此事件的使用者 UserID。
  - Title: 事件標題。
  - Description: 事件詳細描述。
  - StartTime: 事件開始時間 (Timestamp with Timezone)。
  - EndTime: 事件結束時間 (Timestamp with Timezone)。
  - IsAllDay: 是否為全天事件 (Boolean)。
  - Timezone: 事件的特定時區（可能不同於日曆預設）。
  - Location: 事件地點。
  - Status: 事件狀態 (例如：CONFIRMED, TENTATIVE, CANCELLED)。
  - RecurrenceRule: 重複規則定義。
  - Reminders: 提醒設定列表 (例如：[{method: 'popup', minutes_before: 10}, {method: 'email', minutes_before: 60}])。
  - Attendees: 參與者列表及狀態。

- EventParticipant / Attendee

  - ParticipationID: 參與記錄的唯一識別碼。
  - EventID: 關聯的事件 EventID。
  - UserID: 參與者的 UserID。
  - RSVPStatus: 回覆狀態 (ENUM: NEEDS_ACTION, ACCEPTED, DECLINED, TENTATIVE)。
  - IsOptional: 是否為可選參與者 (Boolean)。
  - Comment: 參與者的回覆留言 (可選)。

- RecurrenceRule

  - Frequency: 重複頻率 (ENUM: DAILY, WEEKLY, MONTHLY, YEARLY)。
  - Interval: 重複間隔（例如：每 2 週）。
  - Count: 重複次數。
  - UntilDate: 重複截止日期。
  - ByDay: (用於 WEEKLY/MONTHLY) - 例如：星期一、星期三 (['MO', 'WE'])。
  - ByMonthDay: (用於 MONTHLY/YEARLY) - 例如：每月的 15 號。
  - ExclusionDates: 被排除的特定日期列表 (處理例外情況)。
  - ModifiedInstances: (指向被修改過的特定重複事件實例) - 可能需要額外機制處理。

- AccessControlEntry / SharingPermission
  - ACE_ID: 權限條目的唯一識別碼。
  - ResourceID: 被分享資源的 ID (CalendarID 或 EventID)。
  - ResourceType: 資源類型 (ENUM: CALENDAR, EVENT)。
  - GranteeUserID: 被授權者的 UserID (也可以是 GroupID)。
  - PermissionLevel: 權限等級 (ENUM: READER, WRITER, OWNER, FREE_BUSY_READER)。

## API or System Interface

- API 設計考量:
  - 冪等性 (Idempotency): GET, PUT, DELETE 操作應設計為冪等的。
  - 分頁 (Pagination): 對於可能返回大量結果的列表 API（如 /events），應使用分頁參數（例如 pageToken, maxResults）。
  - RESTful API
- Calendar APIs

  - GET /users/me/calendars: 取得目前使用者擁有或訂閱的所有日曆列表。
  - POST /calendars: 建立一個新的日曆。
    - Request Body: { name: "...", description: "...", timezone: "..." }
  - GET /calendars/{calendarId}: 取得特定日曆的詳細資訊。
  - PUT /calendars/{calendarId}: 更新特定日曆的屬性（例如名稱、顏色）。
    - Request Body: { name: "...", color: "..." }
  - DELETE /calendars/{calendarId}: 刪除一個日曆（以及其包含的所有事件）。
  - GET /calendars/{calendarId}/events: 取得特定日曆中的事件列表。
  - Query Parameters: startTime, endTime, maxResults, pageToken 等。

- Event APIs
  - POST /calendars/{calendarId}/events: 在指定日曆中建立一個新事件。
    - Request Body: 包含事件的所有屬性（標題、時間、地點、參與者、重複規則等）。
  - GET /events/{eventId}: 取得特定事件的詳細資訊。
    - Query Parameters: timezone (指定以哪個時區顯示時間)。
  - PUT /events/{eventId}: 更新一個現有事件。
    - Request Body: 包含要更新的事件屬性。
    - Query Parameters: updateScope=SINGLE|FUTURE|ALL (針對重複事件)。
  - DELETE /events/{eventId}: 刪除一個事件。
    - Query Parameters: deleteScope=SINGLE|FUTURE|ALL (針對重複事件)。
  - POST /events/{eventId}/move?targetCalendarId={newCalendarId}: 將事件移動到另一個日曆。
  - POST /events/{eventId}/attendees: 為事件新增參與者。
    - Request Body: [{ email: "...", responseStatus: "needsAction" }]
  - PUT /events/{eventId}/attendees/{attendeeEmail}: 更新參與者的狀態 (通常由參與者自己操作)。
    - Request Body: { responseStatus: "accepted" | "declined" | "tentative" } (可以透過 /users/me/events/{eventId}/rsvp 這樣的介面來實現，更符合語意)
  - POST /users/me/events/{eventId}/rsvp: 目前使用者回覆事件邀請。
    - Request Body: { responseStatus: "accepted" | "declined" | "tentative" }
- Sharing & Permissions APIs
  - GET /calendars/{calendarId}/acl: 取得日曆的存取控制列表 (Access Control List)。
  - POST /calendars/{calendarId}/acl: 新增或更新日曆的分享權限。
    - Request Body: { scope: { type: "user" | "group", value: "email@example.com" }, role: "reader" | "writer" | "owner" }
  - DELETE /calendars/{calendarId}/acl/{ruleId}: 移除一條分享規則。

## High Level Design / Data Flow

- Components

  - Clients: 使用者介面（Web 瀏覽器、iOS/Android 應用程式）和第三方應用程式（透過 API）。
  - Load Balancer (LB): 將外部流量分發到多個 API Gateway 實例，實現高可用和負載均衡。
  - API Gateway: 作為所有客戶端請求的統一入口點。處理認證 (Authentication)、授權 (Authorization)、請求路由、速率限制 (Rate Limiting)、API 組成 (Composition) 等。
  - Backend Microservices:
    - Calendar Service: 核心服務，處理日曆、事件、參與者、權限 (ACL) 的 CRUD 操作和核心業務邏輯。
    - User Service: 管理使用者資料、偏好設定和身份驗證（可能與專門的身份驗證服務整合）。
    - Notification Service: 負責處理和發送所有提醒和通知。包含一個排程器 (Scheduler) 來觸發基於時間的提醒，並與外部通知網關（如 APNS, FCM, Email Service）整合。
    - Search Service: 提供事件的全文搜索功能。它會非同步地從 Calendar Service 接收事件更新，並建立/更新搜尋索引 (e.g., Elasticsearch)。
    - Fan-out Service: 處理需要通知多個使用者的更新（例如，事件更新通知所有參與者，共享日曆的變更通知所有訂閱者）。通常使用 Message Queue 進行解耦。
  - Message Queue (e.g., Kafka, RabbitMQ, Google Pub/Sub): 用於後端服務之間的異步通信。提高系統的彈性 (Resilience) 和解耦性 (Decoupling)。例如，Calendar Service 可以在寫入資料庫後，發送一個訊息，由 Notification Service, Search Service, Fan-out Service 等獨立訂閱和處理。
  - Data Stores:
    - Primary Database: 儲存核心資料。由於資料量巨大且需要高可用和可擴展性，通常需要分片 (Sharding)。可能混合使用 SQL (如 PostgreSQL, MySQL with Vitess) 來保證強一致性和事務性 (ACID) - 適用於使用者、日曆、ACL；以及 NoSQL (如 Cassandra, DynamoDB) 來處理大量的事件資料和高寫入負載，提供更好的可用性和擴展性。
    - Cache (e.g., Redis, Memcached): 快取常用資料（如使用者的近期事件、日曆列表、權限）以降低資料庫負載並加速讀取響應。
    - Search Index (e.g., Elasticsearch): 專門用於快速的文本搜索。
    - Blob Store (e.g., S3, GCS): 如果支援事件附件，用於儲存文件等二進制大物件。

- Create Event Flow

  1. 使用者 (User): 在客戶端 (Client - Web/Mobile App) 輸入事件詳情（標題、時間、參與者等）並點擊儲存。
  2. 客戶端 (Client): 發送一個 POST /calendars/{calendarId}/events HTTP 請求，包含事件資料和認證 Token，到 API Gateway。
  3. API Gateway:

  - 驗證 Token (Authentication)。
  - 執行速率限制 (Rate Limiting)。
  - 將請求路由 (Route) 到後端的 Calendar Service。

  4. Calendar Service (Write Path):

  - 接收請求並驗證資料。
  - 產生唯一的 EventID。
  - 將事件核心資料寫入 主資料庫 (Primary Database) (例如：Events 表)。
  - 將參與者資訊寫入 EventParticipant 表，狀態設為 NEEDS_ACTION。
  - 如果事件是重複的，儲存 RecurrenceRule。
  - 異步處理 (Asynchronous Tasks): 發送訊息到 訊息佇列 (Message Queue) 以觸發後續任務：
    - 通知任務 (Notification Task): 通知 Notification Service 設定未來事件的提醒。
    - 粉絲散播任務 (Fan-out Task): 通知 Fan-out Service 將新事件邀請推送給參與者（更新他們的日曆視圖、發送 Push Notification 等）。
  - 索引任務 (Indexing Task): 通知 Search Service 更新搜尋索引。5.主資料庫 (Primary Database): 持久化儲存事件、參與者等相關資料。

  5. Calendar Service: 向 API Gateway 返回成功回應 (例如 201 Created)。
  6. API Gateway: 將回應傳回 客戶端 (Client)。
  7. 客戶端 (Client): 更新 UI，顯示新建立的事件。

- View Calendar/Events Flow

  1. 使用者 (User): 在客戶端選擇查看某個時間範圍（例如月視圖）。
  2. 客戶端 (Client): 發送 GET /events?startTime=...&endTime=... 或 GET /calendars/{calendarId}/events?... 請求到 API Gateway。
  3. API Gateway: 驗證、限速、路由請求到 Calendar Service。
  4. Calendar Service (Read Path):

  - 接收請求並驗證參數。
  - 確定使用者有權限查看的日曆 (CalendarID 列表)。
  - 查詢快取 (Cache Query): 檢查 快取 (Cache - 如 Redis/Memcached) 中是否有該使用者/時間範圍的快取資料。如果命中 (Cache Hit)，直接返回快取資料。
  - 資料庫查詢 (Database Query - Cache Miss):
  - 產生資料庫查詢語句，涵蓋使用者有權限的日曆和指定時間範圍。
  - 處理重複事件：可能需要即時展開 (Expand) 重複規則以找出在時間範圍內的實例，或者查詢預先展開 (Pre-computed) 的實例表。
  - 從 主資料庫 (Primary Database) 的相關分片 (Shards) 讀取事件資料。
  - 聚合 (Aggregate) 查詢結果。
  - 更新快取 (Cache Update): 將查詢結果存入快取，供後續請求使用。

  5. Calendar Service: 向 API Gateway 返回事件列表。
  6. API Gateway: 將回應傳回 客戶端 (Client)。
  7. 客戶端 (Client): 在 UI 上渲染日曆和事件。

- RSVP Flow (回覆事件邀請)

  1. 使用者 (User): 在客戶端對收到的邀請點擊 "接受" (Accept)。
  2. 客戶端 (Client): 發送 POST /users/me/events/{eventId}/rsvp 請求，Body 中包含 { responseStatus: "accepted" }。
  3. API Gateway: 驗證、限速、路由到 Calendar Service。
  4. Calendar Service:

  - 驗證使用者是否有權限回覆此事件。
  - 更新 主資料庫 中對應的 EventParticipant 記錄的 RSVPStatus。
  - 異步處理: 發送訊息到 訊息佇列，觸發 Fan-out Service 通知事件的組織者和其他參與者該使用者的回覆狀態已更新。

  5. Calendar Service: 返回成功回應。
  6. API Gateway & Client: 更新 UI。

- ## Typical Workflow

  假設使用者 A 更新了一個有 50 個參與者（包括使用者 B）的會議時間：

  - Trigger: 使用者 A 在客戶端操作，Calendar Service 接收到更新請求。
  - 寫入與發布 (Write & Publish): Calendar Service 成功將事件的新時間寫入主資料庫。它構建一個包含 EventID、UpdateType: TIME_CHANGED、UpdaterUserID: UserA 等資訊的訊息。
  - 訊息入隊 (Enqueue): Calendar Service 將此訊息發布到 Message Queue 的特定主題 (Topic) 上（例如 event-updates）。Calendar Service 的任務到此基本完成，可以回應使用者 A 更新成功。
  - 訊息消費 (Consume): Fan-out Service 的一個或多個實例監聽 event-updates 主題，並接收到這個訊息。
  - 查找收件人 (Lookup Recipients): Fan-out Service 使用訊息中的 EventID 去查詢 主資料庫，獲取了 50 個參與者的 UserID 列表。
  - 確定操作 (Determine Actions): 對於列表中的每個 UserID（例如 使用者 B），Fan-out Service 決定需要做什麼：
    - 查詢 User Service 或相關資料庫，得知使用者 B 啟用了 Push Notification 並獲取其 Device Token。
    - 決定需要讓使用者 B 的日曆視圖快取失效。
  - 執行操作 (Execute Actions): Fan-out Service 並行地執行這些操作：
    - 向 Notification Service 發送請求，要求給使用者 B 的 Device Token 發送一個內容為「會議時間已更改」的 Push Notification。
    - 向 Cache (如 Redis) 發送命令，刪除或標記使用者 B 對於該 EventID 的快取條目為失效。
    - (對其他 49 個參與者執行類似操作...)
  - 處理結果 (Handle Results): 記錄操作成功或失敗。如果對使用者 B 的 Push Notification 發送暫時失敗，可能會在稍後重試。

## Deep Dives

- Recurring Events

  重複事件的處理是日曆系統中的一個複雜點，主要挑戰在於如何在儲存效率、查詢效能和通知準確性之間取得平衡。以下是一種常見的處理方式，符合先前描述的高階設計：

  - 重複事件的產生 (Generating Recurring Event Occurrences)
    - 核心概念: 不會儲存無限的未來事件實例。通常採用 預先計算/具現化 (Pre-computation / Materialization) 結合 規則儲存 的方式。當使用者建立一個重複事件時，Calendar Service 會儲存：
    - 一個「主事件」記錄 (Master Event Record)，包含事件的基本資訊（標題、描述、地點等）以及完整的 RecurrenceRule（重複規則，如每週一、每月第一個星期五）。
    - 這個主事件本身通常不直接顯示在日曆上，它更像是一個模板。
  - Instance Generation
    - 異步流程: 當主事件被建立或其重複規則被修改時，Calendar Service 會發送一個訊息到 Message Queue。
    - 處理器 (Generator): 一個背景處理器（可以是 Calendar Service 的一部分，或是一個獨立的 Recurring Event Service）會接收此訊息。
    - 計算與儲存: 此處理器根據 RecurrenceRule 計算出未來一段時間內（例如未來 1-2 年，這個窗口 window 是可配置的）所有具體的事件「實例 (Instances)」。
    - 對於計算出的每一個實例：
      - 在 主資料庫 (Primary Database) 中創建一個獨立的 Event 記錄。
      - 這個實例記錄會包含具體的 StartTime 和 EndTime。
      - 它會標示自己是一個重複事件的實例 (EventType = RECURRING_INSTANCE)。
      - 它會包含一個指向「主事件」記錄的引用 (MasterEventID)。
    - 持續產生: 這個產生器需要定期運行，以確保隨著時間推移，總是有未來一段時間內的事件實例被預先計算好。
  - 查詢/查看:
    - 當使用者查看日曆時 (GET /events?startTime=...&endTime=...)，Calendar Service 主要查詢的是資料庫中那些已經被具現化的、落在請求時間範圍內的 Event 實例記錄。
    - 因為實例已經是具體的事件記錄，查詢效能會很好，就像查詢普通事件一樣。
  - 處理例外 (Handling Exceptions):
    - 修改單一實例: 使用者修改某一個日期的重複事件（例如更改時間或標題），可以直接更新對應的那個具現化 Event 實例記錄。同時可能需要在主事件的規則中（或一個獨立的例外表）記錄這個日期的例外情況。
  - 修改未來事件: 這通常會被處理為：
    - 結束舊的重複規則（例如，設定舊規則的 UntilDate 到修改日的前一天）。
    - 創建一個新的「主事件」記錄，包含新的規則，起始於修改日。
    - 觸發新規則的實例產生流程。
  - Notifying Users for Recurring Events
    通知的挑戰在於如何為可能非常多且分散在未來的事件實例安排提醒。

    - 提醒設定: 提醒的規則（例如提前 10 分鐘彈窗提醒）儲存在「主事件」記錄中，並被所有產生的實例繼承。
    - 通知觸發機制: 採用 Notification Service 配合 定期查詢 (Periodic Querying) 的方式通常更具擴展性。
    - Notification Service Scheduler: Notification Service 內部有一個高效率的排程器 (Scheduler)。這個排程器**不會**為未來幾年的每個提醒都創建一個單獨的計時器。
    - 定期檢查: 排程器會非常頻繁地運行（例如每分鐘或每幾分鐘）。
    - 查詢即將發生的事件: 每次運行時，它會查詢 主資料庫（或為此優化的快取/視圖），找出 即將 發生並且需要發送提醒的事件。查詢條件類似：「找出所有 StartTime 在接下來 N 分鐘內，且設定了需要在 M 分鐘前提醒的 Event 實例」。這個查詢會自然地包含那些即將到期的、預先計算好的重複事件實例。
    - 觸發通知: 一旦查詢到符合條件的事件實例及其提醒設定，Notification Service 就會執行實際的通知動作：
      - 調用 APNS, FCM 發送 Push Notification。
      - 調用 Email Service 發送郵件提醒。
      - 對於 Web Client 可能通過 WebSocket 或類似機制發送即時提醒。

- Fan-out Service

  Fan-out 在這裡指的是將一個信息或一個更新，從單一來源「散播」或「分發」給大量（多個）目標接收者的過程。在 Google Calendar 的情境下，當一個共享資源（如一個事件或一個日曆）發生變更時，需要通知所有相關的使用者。

  - 為什麼需要 Fan-out Service？如果讓原始服務（例如 Calendar Service）在處理一個更新請求時，同步地去通知所有相關人員（例如一個有 100 個參與者的事件更新），會遇到以下問題：
    - 高延遲 (High Latency): 更新操作會變得很慢，因為服務需要等待所有通知/更新完成後才能回應原始請求者。使用者體驗會很差。
    - 緊密耦合 (Tight Coupling): Calendar Service 需要知道如何找到每個參與者的通知偏好（Push? Email?）、設備標識 (Device Token)、甚至可能需要更新他們各自的快取。這使得 Calendar Service 過於複雜且與其他服務耦合過緊。
    - 可靠性問題 (Reliability Issues): 如果通知其中一個使用者失敗了，整個更新操作是否要回滾？如何有效地重試失敗的通知？同步處理會讓錯誤處理變得非常複雜和脆弱。
    - 擴展性瓶頸 (Scalability Bottleneck): 當參與者/訂閱者數量非常多時，Calendar Service 在處理更新時會承受巨大壓力，成為系統瓶頸。
  - Fan-out Service 的角色和職責 (Role & Responsibilities):
    - 解耦 (Decoupling): 將「觸發更新」的服務（如 Calendar Service）與「接收更新」的眾多使用者或系統元件（如快取、通知渠道）分離開來。
    - 異步處理 (Asynchronous Processing): 它是透過 Message Queue 來驅動的。Calendar Service 只需快速地將一個「更新事件」訊息發布到佇列，然後就可以立即回應使用者。Fan-out Service 會在稍後異步地處理這個訊息。
    - 收件人確定 (Recipient Determination): 根據收到的訊息內容（例如 EventID 和更新類型），查詢 主資料庫 (Primary Database) 或相關資料源，找出所有需要被通知的 UserID（例如事件的所有參與者、共享日曆的所有訂閱者）。
  - 分發邏輯 (Distribution Logic): 決定對於每個 UserID，需要執行哪些操作。這可能包括：
    - 觸發 Push Notification (需要查找 Device Token)。
    - 觸發 Email Notification (需要查找 Email 地址和使用者偏好)。
    - 使相關使用者的 快取 (Cache) 失效（例如，他們查看該事件的快取）。
    - 透過 WebSocket/Server-Sent Events (SSE) 等實時通道推送更新給已連接的客戶端。
    - 將更新標記寫入使用者特定的「收件匣」或「動態饋送 (Feed)」數據結構中。
  - 高吞吐量與並行處理 (High Throughput & Parallelism): 設計上需要能高效處理大量收件人，通常會並行處理對不同使用者的操作。
  - 可靠性與重試 (Reliability & Retries): 負責處理通知或更新個別使用者時可能發生的暫時性失敗，執行重試邏輯。對於持續失敗的情況，可能將訊息移至「死信佇列 (Dead-Letter Queue)」以便後續分析處理。

- Time Range Queries - 如何快速獲取特定時間範圍內的所有事件 (例如：顯示某一周的日曆)？

  - 資料庫設計: 如使用 Cassandra/Bigtable，以 CalendarID 為分區鍵，StartTime 為聚類鍵，可以高效執行範圍掃描。如使用 Sharded SQL，需要在 (CalendarID, StartTime) 或 (CalendarID, StartTime, EndTime) 上建立索引。
  - 查詢邏輯: 查詢需要處理跨越查詢邊界的事件（例如，一個從週日持續到週二的事件，在查詢週一時也應顯示）。
  - 預計算/快取: 對於常用視圖（如“本週”），可以預先計算結果並快取。

- Notification System
  - 事件創建/更新時，計算提醒時間。
  - 將提醒任務（包含 UserID, EventID, NotificationTime, Type）放入訊息佇列 (Message Queue) 或一個按 NotificationTime 索引的延遲任務資料庫 (Scheduled Task Database)。
  - 設計一個通知工作者服務 (Notification Worker Service) 池，這些服務從佇列或資料庫中提取即將到期的提醒任務。
  - 工作者獲取事件和使用者詳細信息，透過推送通知服務 (Push Notification Service - APNS/FCM) 或 郵件閘道器 (Email Gateway) 發送通知。
  - 需要實現重試機制、錯誤處理和冪等性（確保同一提醒不被發送多次）。
