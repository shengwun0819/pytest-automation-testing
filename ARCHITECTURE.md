# 架構設計文件

本文檔說明 API 自動化測試框架的架構設計和執行流程。

## 📐 整體架構

```
┌─────────────────────────────────────────────────────────┐
│                    Test Execution Layer                 │
│  (pytest + conftest.py + test files)                    │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Test Data Layer                        │
│  (CSV files + Expected JSON)                            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Business Logic Layer                   │
│  (API Methods + Assertions + Validators)                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Infrastructure Layer                   │
│  (Base API + Config + Utils)                            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  Optional: Mock Layer (mock_server/)                    │
│  Flask Mock API + router (CSV/JSON) + SQLite Mock DB    │
└─────────────────────────────────────────────────────────┘
```

## 🏗️ 核心組件

### 1. 配置管理 (config.py)

**目的：**
- 統一管理環境變數
- 提供多環境支援
- 驗證必需配置項

**執行流程：**
- 使用 `python-dotenv` 載入環境變數
- 提供 `get_env()` 函數統一處理環境變數讀取
- 支援可選配置項（`is_required=False`）

### 2. API 基礎類別 (api/base_api.py)

**目的：**
- 封裝 HTTP 請求邏輯
- 支援多服務切換
- 統一錯誤處理

**執行流程：**
- 使用 `requests` 庫進行 HTTP 請求
- 使用單一服務（Service A）的 base URL
- 預設 timeout 為 20 秒

### 3. 驗證器 (Validator/validate_common.py)

**目的：**
- 驗證 API 回應
- 比較實際結果和預期結果
- 提供詳細的差異報告

**執行流程：**
- 使用 `deepdiff` 進行深度比較
- 支援多種差異類型（值變更、類型變更、新增、刪除）
- 提供友好的錯誤訊息

### 4. 測試資料管理 (common/file_process.py)

**目的：**
- 讀取 CSV 測試資料
- 讀取 JSON 預期結果
- 處理文字檔案

**執行流程：**
- 使用 `pandas` 讀取 CSV
- 支援參數化測試
- 統一的檔案讀取介面

## 🔄 測試執行流程

```
1. pytest 啟動
   ↓
2. conftest.py 初始化
   - 載入配置
   - 設定 fixtures
   ↓
3. 測試類別初始化 (setup_class)
   - 執行認證
   ↓
4. 測試方法執行
   - 讀取 CSV 測試資料
   - 發送 API 請求
   - 驗證回應
   ↓
7. 生成測試報告
   - Allure 報告
   - 可選：上傳到 S3/Slack
```

## 📊 資料驅動測試

### CSV 檔案結構

```csv
case_id,case_description,is_run,tags,status_code,query_string,cookie
TC001,Get all users,1,regression,200,?page=1&limit=10,auth
```

### 預期結果結構

```
test_data/
  dev/
    users/
      expected_result/
        get_users/
          TC001.json
          TC002.json
```

## 🔐 認證機制

框架支援多種認證類型：

- `auth`: 正常認證
- `no-auth`: 無認證（測試未授權場景）
- `auth_invalid`: 無效 token
- `auth_expired`: 過期 token

## 🎯 設計模式

### 1. 模板方法模式

用於測試執行流程：
- `conftest.py` 定義測試的前後處理流程
- 具體測試類別實作測試邏輯

### 2. Factory mode

用於 API 請求：
- `BaseAPI` 作為 Factory，根據 `service` 參數創建不同的 API 請求

## 🔧 API Endpoint Request

### 新增 API Endpoint

1. 在 `api/example/` 中新增方法
2. 繼承 `BaseAPI` 或使用 `APIMethod`

### 新增驗證規則

1. 在 `Validator/` 中建立新的驗證工具
2. 繼承 `Validator` 類別
3. 覆寫 `validate()` 方法

### 新增測試資料類型

1. 在 `common/file_process.py` 中新增讀取方法
2. 在測試中使用 `@pytest.mark.parametrize` 載入資料

## 📈 效能考量

1. **測試並行化**：支援 `pytest-xdist` 進行並行測試
2. **報告生成**：使用 Allure 的單檔案模式加快報告生成

## 🔒 安全性考量

1. **環境變數**：敏感資訊（密碼、API Key）使用環境變數
2. **`.gitignore`**：確保 `.env` 檔案不會被提交
3. **測試資料**：使用假資料，避免洩露真實資訊

### 5. Mock Server (mock_server/)

**目的：**
- 提供與 test_data 一致的 Mock API（登入、GET /users、GET /customers 等）
- 依 CSV/預期 JSON 回傳，或從 SQLite Mock DB 查詢（可選）

**執行流程：**
- 使用 Flask，預設 port 5050
- 未設定真實 API 時，CI 與本機皆可對接 Mock Server 執行測試

## 🚀 未來改進方向

1. ~~**API Mock**~~：已實作 Mock Server（`mock_server/`）與 Mock DB，支援離線與 CI 測試
2. **測試資料生成**：自動生成測試資料
3. **視覺化報告**：增強測試報告的視覺化
4. **CI/CD 整合**：更完善的 CI/CD 整合範例
