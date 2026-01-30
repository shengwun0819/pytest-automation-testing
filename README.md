# API Automation Testing Framework

一個完整的 REST API 自動化測試框架範例，展示如何建立可擴展、可維護的 API 測試系統。

## 📋 專案特色

- ✅ **多環境支援**：支援多個測試環境配置
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
├── tests/                 # 測試案例
│   ├── users/            # 使用者相關測試
│   ├── customers/        # 客戶相關測試
│   └── ...
├── test_data/            # 測試資料
│   └── dev/              # 開發環境測試資料
│       ├── *.csv         # 測試案例資料
│       └── expected_result/  # 預期結果
├── mock_server/          # Mock API Server（可選，模擬後端與 test_data 互動）
│   ├── app.py            # Flask Mock API 入口
│   ├── router.py         # 請求對應 CSV/JSON 邏輯
│   ├── init_mock_db.py    # 可選：SQLite Mock DB 初始化
│   └── README.md         # Mock 啟動方式說明
├── test_report/          # 測試報告（執行測試時自動生成）
├── utils/                # 工具類別
│   ├── assert_response.py    # 回應斷言
│   ├── auth.py               # 認證工具
│   └── ...
└── Validator/            # 驗證器
    └── validate_common.py     # 通用驗證器
```

## 🚀 快速開始

> 💡 **詳細使用指南**：請參考 [USAGE.md](USAGE.md) 獲取完整的使用說明和範例。

**前置需求**：Python 3.8+；建議使用 **Python 3.13**（與 GitHub Actions CI 一致，便於除錯）。若系統為「externally managed」環境（如 macOS Homebrew），建議使用虛擬環境（見下方）。

#### 如何使用 venv（虛擬環境）

在專案根目錄執行以下步驟，之後的 `pip`、`pytest`、`python -m mock_server.app` 都會使用虛擬環境內的 Python 與套件。建議使用 Python 3.13 建立 venv（與 CI 一致）：

```bash
# 1. 建立虛擬環境（會產生 .venv 目錄；建議用 python3.13 或系統預設 python3）
python3 -m venv .venv
# 若系統有多個 Python：py -3.13 -m venv .venv（Windows）或 python3.13 -m venv .venv（macOS/Linux）

# 2. 啟動虛擬環境
# macOS / Linux:
source .venv/bin/activate

# 3. 之後在此 shell 中安裝依賴與執行指令
pip3 install -r requirements.txt
# 例如：pytest tests/ ...、python -m mock_server.app
```

關閉虛擬環境：輸入 `deactivate`。下次要跑測試或 Mock 時，先 `source .venv/bin/activate`（或 Windows 對應指令）再執行即可。

### 1. 安裝依賴

```bash
pip3 install -r requirements.txt
```

（若已依上方使用 venv，請先 `source .venv/bin/activate` 再執行。）

若出現 `Cannot import 'setuptools.build_meta'` 或建置 numpy/pandas 失敗，請先執行：
`pip3 install --upgrade pip setuptools wheel`，再重新執行 `pip3 install -r requirements.txt`（Python 3.12+ 的 venv 預設可能未包含 setuptools）。

### 2. 配置環境變數

複製 `.env.sample` 並建立 `.env` 檔案（**必做**，否則執行時會缺少 `SERVICE_A_BASE_URL` 等設定）：

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

# 測試資料路徑
TEST_DATA_FOLDER=./test_data
```

### 3. 準備測試資料

將測試資料放在 `test_data/dev/` 目錄下，包含：
- CSV 檔案：定義測試案例參數
- `expected_result/` 目錄：存放預期回應的 JSON 檔案

### 4. 執行測試

```bash
# 執行所有測試（未加 --tags 時會執行 CSV 中 is_run=1 的案例）
pytest tests/ --alluredir=allure-results

# 執行特定標籤的測試
pytest tests/ --tags=regression --alluredir=allure-results

# 生成 Allure 報告（需先安裝 Allure CLI，可選）
allure serve allure-results
```

> **注意**：測試結束後會自動嘗試產生 Allure HTML 報告；若未安裝 `allure` 指令，該步驟會失敗，但不影響測試結果。

### 5. 使用 Mock 環境（可選）

若不想依賴真實後端與 DB，可使用 **Mock API Server** 模擬 Gate/Hub 與 test_data 的互動情境：

1. **啟動 Mock Server**（在專案根目錄）：
   ```bash
   python -m mock_server.app
   ```
2. **設定環境變數**，讓測試打 Mock：
   ```bash
   export SERVICE_A_BASE_URL=http://127.0.0.1:5050
   export SERVICE_A_ACCOUNT=any
   export SERVICE_A_PASSWORD=any
   ```
3. **執行測試**（在另一終端）：`pytest tests/ --tags=regression --alluredir=allure-results`

亦可先編輯 `.env`，將 `SERVICE_A_BASE_URL` 改為 `http://127.0.0.1:5050`，則不需每次 export。可選：使用 **Mock DB（SQLite）** 初始化範例資料，詳見 [mock_server/README.md](mock_server/README.md)。

**驗證 Mock 與測試流程是否可執行**：依序完成「安裝依賴 → 複製 .env.sample 為 .env 並改為 Mock URL → 終端一執行 `python -m mock_server.app` → 終端二執行 `pytest tests/ --tags=regression --alluredir=allure-results`」。若測試通過且 Mock Server 有收到請求，即表示流程正常。

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
    def test_get_users(self, is_run, case_input):
        allure.dynamic.title(f"{case_input['case_id']} - {case_input['case_description']}")
        
        if not is_run(run=case_input['is_run'], tags=case_input['tags']):
            pytest.skip('Skip')
        
        resp = Assert.request_switch(
            self,
            method='GET',
            cookie_code=case_input['cookie'],
            params_query=case_input['query_string'],
            path=self.path,
            api=self.api,
            cookie=self.auth   # 來自 setup_class 的 OAuth2 登入結果
        )
        
        Assert.validate_status(resp.status_code, case_input)
        # 驗證回應內容（如使用 Validator 比對 expected_result JSON）...
```

## 🔧 核心組件說明

### 1. BaseAPI

所有 API 請求的基礎類別，封裝了 HTTP 請求邏輯。

### 2. Config

統一管理環境變數和配置，支援多環境切換。

### 3. FileProcess

提供讀取 CSV、JSON 等測試資料檔案的方法。

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

> **注意**：執行測試時，框架會自動在 `test_report/` 目錄下生成 HTML 報告檔案。此目錄會在首次執行測試時自動建立，無需手動建立。

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
5. **環境隔離**：使用不同的環境配置進行測試，避免影響生產環境

## 🔄 CI/CD

本專案包含 GitHub Actions 工作流程，支援自動化測試：

- **自動測試**：Push 或 PR 時自動執行測試
- **多版本測試**：支援多個 Python 版本測試
- **測試報告**：自動生成並上傳 Allure 測試報告
- **報告發布**：可選的 GitHub Pages 報告發布

詳細說明請參考 [.github/workflows/README.md](.github/workflows/README.md)

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License

## 🙏 致謝

本專案改寫自實際的企業級 API 自動化測試框架，保留了核心架構和設計模式，移除了公司特定的業務邏輯和機密資訊，作為學習和參考的範例。
