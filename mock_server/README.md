# Mock Server / API / DB 啟動方式

本目錄提供 **Mock API Server**，用來模擬原始專案（sygna-bundle-gate-sit + sygna-test-data）中「測試程式 → 後端 API → 測試資料」的互動情境，無需真實後端與資料庫即可跑完整測試流程。

---

## 一、Mock API Server（建議先從這裡開始）

### 功能

- **POST /v1/auth/login**：回傳 mock token，供測試的 OAuth2 登入使用。
- **GET /v1/users**、**GET /v1/customers**：
  - **有 Mock DB 時**：若已執行 `init_mock_db` 產生 `mock.db`，且 `USE_MOCK_DB=true`（預設），則**從 SQLite 查資料**回傳（僅對應 CSV 中 status 2xx 的成功案例）；回應格式與 expected_result 一致（`data` + `pagination`）。
  - **無 Mock DB 或非成功案例**：改從 `test_data/dev/` 的 CSV 與 `expected_result` JSON 回傳（含 400、401 等）。

### 環境變數（可選）

| 變數 | 說明 | 預設 |
|------|------|------|
| `TEST_DATA_FOLDER` | 測試資料根目錄（建議從專案根目錄啟動，使用 `./test_data`） | `./test_data` |
| `ENV` | 環境（對應 test_data 子目錄） | `dev` |
| `VERSION` | API 版本前綴 | `/v1` |
| `MOCK_SERVER_PORT` | Mock server 監聽埠（預設 5050，避免 macOS AirPlay 佔用 5000） | `5050` |
| `USE_MOCK_DB` | 是否從 Mock DB (SQLite) 取資料（`true`/`false`）；無 `mock.db` 時仍會改從 CSV/JSON | `true` |
| `MOCK_DB_PATH` | Mock DB 檔案路徑（與 init_mock_db 一致） | `mock.db` |

### 啟動方式

**方式 1：直接執行（建議）**

```bash
# 在專案根目錄 /Users/kevin.lee/Python/api-automation-testing 執行
python -m mock_server.app
```

預設在 `http://0.0.0.0:5050` 啟動。

**方式 2：指定埠**

```bash
MOCK_SERVER_PORT=8000 python -m mock_server.app
```

**方式 3：使用 Flask CLI**

```bash
flask --app mock_server.app:app run --port 5050
```

### 對接測試

1. 啟動 Mock Server（如上）。
2. 設定環境變數，讓測試打 Mock 而非真實 API：
   ```bash
   export SERVICE_A_BASE_URL=http://127.0.0.1:5050
   export SERVICE_A_ACCOUNT=any
   export SERVICE_A_PASSWORD=any
   ```
3. 執行測試：
   ```bash
   pytest tests/ --tags=regression --alluredir=allure-results
   ```

測試會對 `/v1/auth/login` 取得 token，再對 `/v1/users`、`/v1/customers` 發請求；Mock Server 會依 **Mock DB 或 CSV/JSON** 回傳，Validator 會比對預期結果。

---

## 二、Mock DB（SQLite）：讓 API 從 DB 取資料

若想模擬「API 背後有一層 DB」的情境，請先建立 Mock DB，Mock API 會**優先從 SQLite 查資料**再回傳。

### 功能

- **init_mock_db**：建立 SQLite（預設 `mock.db`）、建立 `users` / `customers` 表，並從 `test_data` 的 expected_result JSON 匯入範例資料。
- **Mock API**：當 `mock.db` 存在且 `USE_MOCK_DB=true` 時，GET /v1/users、GET /v1/customers 的**成功案例（2xx）**會從 SQLite 查詢並回傳 `{ data, pagination }`；其餘（401、400 等）仍由 CSV/JSON 決定。

### 啟動方式（建議順序）

```bash
# 1. 在專案根目錄建立 mock.db 並初始化範例表與資料
python -m mock_server.init_mock_db

# 2. 啟動 Mock Server（會自動從 mock.db 取資料回傳）
python -m mock_server.app
```

預設會在專案根目錄產生 `mock.db`。可設定環境變數 `MOCK_DB_PATH` 指定路徑。若不想從 DB 取資料，可設 `USE_MOCK_DB=false`。

---

## 三、架構對應關係（與原始專案對照）

| 原始專案 (sygna-bundle-gate-sit + sygna-test-data) | 本專案 Mock 情境 |
|----------------------------------------------------|------------------|
| 真實 Gate/Hub 後端 API                              | Mock API Server (Flask) |
| 真實 MySQL/PostgreSQL + SQL 腳本                    | SQLite Mock DB（init_mock_db + mock_server/db.py） |
| sygna-test-data 的 CSV + expected_result JSON      | test_data 的 CSV/JSON；成功案例改由 Mock DB 查詢回傳 |

測試程式（pytest、Assert、Validator）不需改動，僅需將 `SERVICE_A_BASE_URL` 指到 Mock Server，即可在無真實後端與 DB 的環境下重現「架構保存與例子」的互動情境。
