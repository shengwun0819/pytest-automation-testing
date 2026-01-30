# 使用指南

本指南將幫助您快速上手使用這個 API 自動化測試框架。

## 📋 前置需求

- Python 3.13 或更高版本
- pip（Python 套件管理器）
- Allure（用於生成測試報告，可選）

## 🚀 快速開始

### 步驟 1: 安裝套件

```bash
# 進入專案目錄
cd ./pytest-automation-testing/

# 安裝 Python 套件
pip install -r requirements.txt
```

### 步驟 2: 安裝 Allure（可選，用於生成測試報告）

**macOS:**
```bash
brew install allure
```

### 步驟 3: 配置環境變數

建立 `.env` 檔案（如果還沒有）：

```bash
# 複製範例配置（如果有的話）
# cp .env.sample .env

# 或直接建立 .env 檔案
touch .env
```

編輯 `.env` 檔案，填入你的 API 測試環境配置：

```env
# ============================================
# 環境設定
# ============================================
ENV=dev
VERSION=/v1

# ============================================
# Service A 配置
# ============================================
SERVICE_A_BASE_URL=https://api.example.com
SERVICE_A_ACCOUNT=your_username
SERVICE_A_PASSWORD=your_password

# ============================================
# 測試資料設定
# ============================================
TEST_DATA_FOLDER=./test_data
```

**使用 Mock 環境（可選）**：若要以專案內建的 Mock Server 執行測試（無需真實 API），請將 `SERVICE_A_BASE_URL` 設為 `http://127.0.0.1:5050`，並在執行測試前於另一終端啟動 Mock Server（`python -m mock_server.app`）與可選的 Mock DB（`python -m mock_server.init_mock_db`）。詳見 [mock_server/README.md](mock_server/README.md)。

### 步驟 4: 調整 API 認證方法

根據你的實際 API 認證方式，修改 `api/example/oauth2.py`：

```python
def post_oauth2(self, account: str, credential: str, service: str = 'service_a'):
    """
    執行 OAuth2 登入
    
    根據你的實際 API 調整登入端點和請求格式
    """
    # 修改這裡的登入邏輯以符合你的 API
    login_path = '/auth/login'  # 根據實際 API 調整
    login_body = {
        'account': account,
        'password': credential
    }
    # ... 其他邏輯
```

### 步驟 5: 準備測試資料

#### 5.1 建立 CSV 測試資料

在 `test_data/dev/{模組名稱}/` 目錄下建立 CSV 檔案，例如 `get_users.csv`：

```csv
case_id,case_description,is_run,tags,status_code,query_string,cookie
TC001,Get all users successfully,1,regression,200,?page=1&limit=10,auth
TC002,Get users with invalid page,1,regression,400,?page=-1,auth
TC003,Get users without authentication,1,regression,401,,no-auth
```

**CSV 欄位說明：**
- `case_id`: 測試案例 ID
- `case_description`: 測試案例描述
- `is_run`: 是否執行（1=執行, 0=跳過）
- `tags`: 測試標籤（用逗號分隔，例如：regression,smoke）
- `status_code`: 預期的 HTTP 狀態碼
- `query_string`: API 查詢參數（例如：?page=1&limit=10）
- `cookie`: 認證類型（auth=正常認證, no-auth=無認證）

#### 5.2 建立預期結果 JSON

在 `test_data/dev/{模組名稱}/expected_result/{api名稱}/` 目錄下建立 JSON 檔案，例如 `TC001.json`：

```json
{
  "data": [
    {
      "id": 1,
      "username": "test_user_1",
      "email": "test1@example.com",
      "is_active": true
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1
  }
}
```

### 步驟 6: 執行測試

#### 6.1 執行所有測試

```bash
pytest tests/ --alluredir=allure-results
```

#### 6.2 執行特定模組的測試

```bash
# 只執行 users 相關測試
pytest tests/users/ --alluredir=allure-results

# 只執行 customers 相關測試
pytest tests/customers/ --alluredir=allure-results
```

#### 6.3 執行特定標籤的測試

```bash
# 只執行標籤為 regression 的測試
pytest tests/ --tags=regression --alluredir=allure-results

# 執行多個標籤（用逗號分隔）
pytest tests/ --tags=regression,smoke --alluredir=allure-results
```

#### 6.4 執行特定測試檔案

```bash
pytest tests/users/test_get_users.py --alluredir=allure-results
```

#### 6.5 執行特定測試案例

```bash
pytest tests/users/test_get_users.py::TestGetUsers::test_get_users --alluredir=allure-results
```

#### 6.6 其他有用的 pytest 選項

```bash
# 顯示詳細輸出
pytest tests/ -v --alluredir=allure-results

# 顯示 print 輸出
pytest tests/ -s --alluredir=allure-results

# 顯示詳細輸出和 print
pytest tests/ -v -s --alluredir=allure-results

# 在遇到第一個失敗時停止
pytest tests/ --maxfail=1 --alluredir=allure-results

# 並行執行測試（需要安裝 pytest-xdist）
pytest tests/ -n auto --alluredir=allure-results
```

### 步驟 7: 查看測試報告

#### 7.1 使用 Allure 查看報告

```bash
# 生成並開啟 Allure 報告
allure serve allure-results

# 或先生成報告再開啟
allure generate allure-results --clean -o allure-report
allure open allure-report
```

> **注意**：執行測試時，框架會自動在 `test_report/` 目錄下生成 HTML 報告檔案。此目錄會在首次執行測試時自動建立，無需手動建立。

#### 7.2 查看簡易測試結果

```bash
# pytest 會自動顯示測試結果摘要
pytest tests/ -v -s
```
- `-v`：verbose，顯示每個測試案例的名稱與通過/失敗狀態。
- `-s`：不擷取 stdout，測試中的 `print()` 與標準輸出會直接顯示在終端機。

#### 7.3 測試報告存放位置

- **Allure 結果**：`allure-results/` 目錄（原始測試結果）
- **HTML 報告**：`test_report/` 目錄（生成的 HTML 報告檔案）
  - 報告檔案命名格式：`report_{commit_sha}_{result}_{timestamp}.html`
  - 此目錄已被 `.gitignore` 忽略，不會提交到版本控制

## 📝 實際使用範例

### 範例 1: 測試 GET /users API

1. **建立 CSV 測試資料** (`test_data/dev/users/get_users.csv`):

```csv
case_id,case_description,is_run,tags,status_code,query_string,cookie
TC001,Get all users successfully,1,regression,200,?page=1&limit=10,auth
TC002,Get users with invalid page,1,regression,400,?page=-1,auth
```

2. **建立預期結果** (`test_data/dev/users/expected_result/get_users/TC001.json`):

```json
{
  "data": [
    {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1
  }
}
```

3. **執行測試**:

```bash
pytest tests/users/test_get_users.py -v --alluredir=allure-results
```

### 範例 2: 新增新的 API 測試

1. **在 `api/example/api_method.py` 中新增方法**:

```python
def get_products(self, cookie: str, params_query: str = '', service: str = 'service_a'):
    """取得產品列表"""
    return self.method_switch(
        method='GET',
        path='/products',
        cookie=cookie,
        cookie_code='auth',
        params_query=params_query,
        service=service
    )
```

2. **建立測試檔案** (`tests/products/test_get_products.py`):

```python
import allure
import config
import pytest
from api.example.api_method import APIMethod
from api.example.oauth2 import OAuth2
from common.file_process import FileProcess
from utils.assert_response import Assert
from Validator.validate_common import Validator

testdata_folder = config.TEST_DATA_FOLDER
env = config.ENV

@allure.epic("Products")
@allure.feature("Get Products")
class TestGetProducts:
    oauth2 = OAuth2()
    api = APIMethod()
    path = '/products'
    
    def setup_class(self):
        self.auth = self.oauth2.post_oauth2(
            account=config.SERVICE_A_ACCOUNT,
            credential=config.SERVICE_A_PASSWORD,
            service='service_a'
        )
    
    @allure.story("Positive Test Cases")
    @pytest.mark.parametrize(
        'case_input',
        FileProcess.read_csv_data(file_name='get_products', path='products')
    )
    def test_get_products(self, is_run, case_input):
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
            cookie=self.auth
        )
        
        resp_json = resp.json()
        
        Assert.validate_status(
            self,
            status_code=resp.status_code,
            case_input=case_input
        )
        
        validator = Validator(
            resp_json=resp_json,
            expected_path=(
                f"./{testdata_folder}/{env}/products/expected_result/"
                f"get_products/{case_input['case_id']}.json"
            ),
            api_tag='get_products'
        )
        validator.validate()
```

3. **建立測試資料和預期結果**（參考範例 1）

## 🔧 常見問題

### Q1: 如何跳過某些測試案例？

在 CSV 檔案中將 `is_run` 設為 `0`：

```csv
case_id,case_description,is_run,tags,status_code,query_string,cookie
TC001,Test case,0,regression,200,,auth
```

### Q2: 如何只執行特定標籤的測試？

```bash
pytest tests/ --tags=regression --alluredir=allure-results
```

### Q3: 測試失敗時如何除錯？

1. 使用 `-v -s` 查看詳細輸出：
```bash
pytest tests/ -v -s --alluredir=allure-results
```

2. 查看 Allure 報告中的詳細錯誤資訊

3. 檢查預期結果 JSON 是否正確

### Q4: 如何處理動態資料（如時間戳記、ID）？

在驗證器中可以實作自訂驗證邏輯，忽略動態欄位。參考 `Validator/validate_common.py`。

### Q5: 如何測試需要不同認證的 API？

在 CSV 的 `cookie` 欄位中使用不同的認證類型：
- `auth`: 正常認證
- `no-auth`: 無認證
- `auth_invalid`: 無效認證（需要在 `utils/auth.py` 中實作）

## 🔄 CI/CD 整合

本專案包含 GitHub Actions 設定，支援自動化測試：

### 設定 GitHub Secrets

在 GitHub Repository Settings → Secrets and variables → Actions 中設定：

- `SERVICE_A_BASE_URL` - Service A 的 API URL
- `SERVICE_A_ACCOUNT` - Service A 的帳號
- `SERVICE_A_PASSWORD` - Service A 的密碼

### 查看測試結果

1. 前往 GitHub Repository → **Actions** 標籤
2. 選擇對應的 workflow 執行
3. 下載 **Artifacts** 中的測試報告

詳細說明請參考 [.github/workflows/README.md](.github/workflows/README.md)

## 📚 下一步

- 閱讀 [ARCHITECTURE.md](ARCHITECTURE.md) 了解架構設計
- 閱讀 [README.md](README.md) 了解專案特色
- 閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何貢獻
- 閱讀 [.github/workflows/README.md](.github/workflows/README.md) 了解 CI/CD 設定

## 💡 提示

1. **測試資料管理**：將測試資料放在 `test_data/{env}/` 目錄下，方便管理不同環境的測試資料
2. **標籤使用**：善用標籤分類測試（如：regression, smoke, critical），方便選擇性執行
3. **預期結果**：保持預期結果 JSON 與實際 API 回應一致，避免誤報
4. **版本控制**：不要將 `.env` 檔案提交到版本控制系統（已在 `.gitignore` 中）
