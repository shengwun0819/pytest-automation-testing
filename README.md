# API Automation Testing Framework

一個完整的 REST API 自動化測試框架範例，展示如何建立可擴展、可維護的 API 測試系統。

## 📋 專案特色

- ✅ **多環境支援**：支援多個測試環境配置
- ✅ **多資料庫支援**：支援 PostgreSQL 和 MySQL
- ✅ **資料驅動測試**：使用 CSV 檔案進行參數化測試
- ✅ **完整的驗證系統**：自動驗證 API 回應結構和內容
- ✅ **測試報告**：使用 Allure 生成美觀的測試報告
- ✅ **CI/CD 整合**：支援自動化測試和報告上傳
- ✅ **模組化設計**：清晰的架構，易於擴展和維護

## 📁 專案結構

```
.
├── api/                    # API 請求封裝
│   ├── base_api.py        # API 基礎類別
│   └── example/           # 範例 API 方法
│       └── api_method.py
├── common/                # 共用工具
│   ├── constants.py       # 常數定義
│   └── file_process.py    # 檔案處理工具
├── config.py              # 配置管理
├── conftest.py            # pytest 配置和 fixtures
├── database/              # 資料庫操作
│   └── db_sqlalchemy.py   # SQLAlchemy 封裝
├── tests/                 # 測試案例
│   ├── users/            # 使用者相關測試
│   ├── customers/        # 客戶相關測試
│   └── ...
├── test_data/            # 測試資料
│   └── dev/              # 開發環境測試資料
│       ├── *.csv         # 測試案例資料
│       └── expected_result/  # 預期結果
├── utils/                # 工具類別
│   ├── assert_response.py    # 回應斷言
│   ├── auth.py               # 認證工具
│   └── ...
└── Validator/            # 驗證器
    └── validate_common.py     # 通用驗證器
```

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 配置環境變數

複製 `.env.sample` 並建立 `.env` 檔案：

```bash
cp .env.sample .env
```

編輯 `.env` 檔案，填入你的測試環境配置：

```env
# 環境設定
ENV=dev
VERSION=/v1

# Service A 配置（對應原始專案中的 ORI）
SERVICE_A_BASE_URL=https://api.example.com
SERVICE_A_ACCOUNT=test_user
SERVICE_A_PASSWORD=test_password
SERVICE_A_DB_HOST=localhost
SERVICE_A_DB_PORT=5432
SERVICE_A_DB_NAME=test_db
SERVICE_A_DB_USER=test_user
SERVICE_A_DB_PASSWORD=test_password

# Service B 配置（對應原始專案中的 BEN）
SERVICE_B_BASE_URL=https://api.example.com
SERVICE_B_ACCOUNT=test_user
SERVICE_B_PASSWORD=test_password
SERVICE_B_DB_HOST=localhost
SERVICE_B_DB_PORT=5432
SERVICE_B_DB_NAME=test_db
SERVICE_B_DB_USER=test_user
SERVICE_B_DB_PASSWORD=test_password

# 測試資料路徑
TEST_DATA_FOLDER=./test_data
```

### 3. 準備測試資料

將測試資料放在 `test_data/dev/` 目錄下，包含：
- CSV 檔案：定義測試案例參數
- `expected_result/` 目錄：存放預期回應的 JSON 檔案

### 4. 執行測試

```bash
# 執行所有測試
pytest tests/ --alluredir=allure-results

# 執行特定標籤的測試
pytest tests/ --tag=regression --alluredir=allure-results

# 指定資料庫類型
pytest tests/ --db_type=postgres --alluredir=allure-results

# 生成 Allure 報告
allure serve allure-results
```

## 📝 測試案例範例

### CSV 驅動測試

在 `test_data/dev/users/get_users.csv` 中定義測試案例：

```csv
case_id,case_description,is_run,tags,status_code,query_string,cookie
TC001,Get all users successfully,1,regression,200,?page=1&limit=10,auth
TC002,Get users with invalid page,1,regression,400,?page=-1,auth
```

### 測試程式碼

```python
import allure
import pytest
from api.example.api_method import APIMethod
from common.file_process import FileProcess
from utils.assert_response import Assert

@allure.epic("Users")
@allure.feature("Get Users")
class TestGetUsers:
    api = APIMethod()
    path = '/users'

    @allure.story("Positive Test Cases")
    @pytest.mark.parametrize('case_input', FileProcess.read_csv_data('get_users', 'users'))
    def test_get_users(self, db_type, is_run, case_input):
        allure.dynamic.title(f"{case_input['case_id']} - {case_input['case_description']}")
        
        if not is_run(run=case_input['is_run'], tags=case_input['tags']):
            pytest.skip('Skip')
        
        resp = Assert.request_switch(
            self,
            method='GET',
            cookie_code=case_input['cookie'],
            params_query=case_input['query_string'],
            path=self.path,
            api=self.api
        )
        
        Assert.validate_status(resp.status_code, case_input)
        # 驗證回應內容...
```

## 🔧 核心組件說明

### 1. BaseAPI

所有 API 請求的基礎類別，封裝了 HTTP 請求邏輯。

### 2. Config

統一管理環境變數和配置，支援多環境切換。

### 3. Database

使用 SQLAlchemy 封裝資料庫操作，支援 PostgreSQL 和 MySQL。

### 4. Validator

自動驗證 API 回應，支援深度比較和自訂驗證規則。

### 5. Assert

提供統一的斷言方法，簡化測試程式碼。

## 📊 測試報告

使用 Allure 生成測試報告：

```bash
# 生成報告
allure generate allure-results --clean -o allure-report

# 開啟報告
allure open allure-report
```

## 🛠️ 自訂擴展

### 新增 API 端點

1. 在 `api/example/api_method.py` 中新增方法
2. 繼承 `BaseAPI` 類別
3. 使用 `request()` 方法發送請求

### 新增驗證器

1. 在 `Validator/` 目錄下建立新的驗證器
2. 繼承 `Validator` 類別
3. 實作自訂驗證邏輯

### 新增測試案例

1. 在 `tests/` 目錄下建立測試檔案
2. 使用 CSV 檔案定義測試參數
3. 在 `expected_result/` 中放置預期結果

## 📚 最佳實踐

1. **測試資料管理**：使用 CSV 檔案管理測試參數，易於維護
2. **預期結果驗證**：使用 JSON 檔案儲存預期結果，確保一致性
3. **標籤管理**：使用標籤分類測試案例，方便選擇性執行
4. **錯誤處理**：完善的錯誤處理和日誌記錄
5. **資料庫清理**：測試前後自動清理測試資料

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License

## 🙏 致謝

本專案改寫自實際的企業級 API 自動化測試框架，保留了核心架構和設計模式，移除了公司特定的業務邏輯和機密資訊，作為學習和參考的範例。
