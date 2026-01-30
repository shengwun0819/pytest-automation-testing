# GitHub Actions Workflows

本目錄包含專案的 CI/CD 工作流程設定。

## 📋 可用的 Workflows

### 1. `test.yml` - 完整測試流程（多 Python 版本）

**觸發條件：**
- Push 到 `main` 分支
- Pull Request 到 `main` 分支
- 手動觸發（workflow_dispatch）

**功能：**
- 在 **Python 3.13** 上執行測試（與建議的本地 venv 一致）
- 未設定 `SERVICE_A_BASE_URL` 時自動啟動 Mock Server 與 Mock DB，無需真實 API 即可通過測試
- 支援指定測試標籤（`--tags=regression`）
- 生成 Allure 報告並上傳為 Artifacts

**使用方式：**
```bash
# 在 GitHub Actions 頁面手動觸發
# 可以指定要執行的測試標籤（例如：regression,smoke）
```

### 2. `publish-report.yml` - 發布測試報告到 GitHub Pages

**觸發條件：**
- `test.yml`（API Tests）完成後自動觸發

**功能：**
- 下載 Allure 報告
- 發布到 GitHub Pages（僅 main 分支）

## 🔧 配置 GitHub Secrets

為了讓 GitHub Actions 能夠正常執行，需要在 GitHub Repository Settings 中配置以下 Secrets：

### 可選的 Secrets

若**不設定** `SERVICE_A_BASE_URL`，CI 會自動啟動專案內建的 Mock Server（port 5050）與 Mock DB，測試可正常通過。若需對接真實 API，請設定：

- `SERVICE_A_BASE_URL` - Service A 的 API 基礎 URL（例如 `https://api.example.com`）
- `SERVICE_A_ACCOUNT` - Service A 的帳號
- `SERVICE_A_PASSWORD` - Service A 的密碼

### 如何設定 Secrets

1. 前往 GitHub Repository
2. 點擊 **Settings** → **Secrets and variables** → **Actions**
3. 點擊 **New repository secret**
4. 輸入 Secret 名稱和值
5. 點擊 **Add secret**

## 📊 查看測試結果

### 在 GitHub Actions 中查看

1. 前往 GitHub Repository
2. 點擊 **Actions** 標籤
3. 選擇對應的 workflow
4. 查看執行結果

### 下載測試報告

1. 在 workflow 執行完成後
2. 在 workflow 執行頁面底部找到 **Artifacts**
3. 下載 `allure-report` 或 `test-report` artifact
4. 解壓縮後開啟 `index.html` 查看報告

### 在 GitHub Pages 中查看（如果啟用）

如果啟用了 `publish-report.yml`，報告會發布到：
```
https://{username}.github.io/{repository}/test-report/
```

## 🛠️ 自訂 Workflow

### 修改測試標籤

在 `test.yml` 中修改：

```yaml
pytest tests/ \
  --tags=regression,smoke \  # 修改這裡的標籤
  --alluredir=allure-results
```

### 修改 Python 版本

在 `test.yml` 中修改 `strategy.matrix.python-version`（目前僅 3.13）：

```yaml
strategy:
  matrix:
    python-version: ["3.13"]  # 可改為 ["3.12", "3.13"] 等
```

### 新增 Slack 通知（可選）

如果需要 Slack 通知，可以在 workflow 中新增：

```yaml
- name: Send Slack Notification
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Test completed'
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## 📝 注意事項

1. **測試環境**：GitHub Actions 使用 Ubuntu 環境，確保測試可以在 Linux 環境下執行
2. **API 連線**：確保測試的 API 可以從 GitHub Actions 環境中存取
3. **Secrets 安全**：不要將敏感資訊直接寫在 workflow 檔案中，使用 Secrets
4. **Artifacts 保留**：預設保留 7-30 天，可以根據需求調整
5. **並行執行**：多個 workflow 可能會並行執行，注意資源使用

## 🔧 疑難排解

### 「Could not find allure-results directory」

- **原因**：產生 Allure 報告的 job 在**另一個 job** 執行，且沒有先下載 `test` job 產生的 `allure-results` artifact。
- **作法**：本專案已在**同一個** `test` job 內產生報告並上傳；若你拆成兩個 job，請在報告 job 開頭加上「Download artifact」步驟，下載 `allure-results-${{ matrix.python-version }}`（或你上傳的 artifact 名稱），再執行 `allure generate`。

### 「ModuleNotFoundError: No module named 'numpy.rec'」（Python 3.13）

- **原因**：NumPy 2.0 移除了 `numpy.rec`，而 pandas 在讀 CSV 時會用到，導致 Mock Server 在 Python 3.13 上失敗。
- **作法**：`requirements.txt` 已限定 `numpy>=1.23.3,<2`；CI 的 Python 矩陣目前僅使用 **3.8–3.11**，未納入 3.12/3.13。若你在 fork 中加入 3.13，請先移除以通過 CI，或等 pandas/numpy 完全支援 3.13 再啟用。

### 「Job was cancelled」

- **原因**：多為手動取消、或並行/排程觸發的 cancel 政策，少數為 runner 逾時。
- **作法**：確認同一 branch 沒有重複觸發；若測試與報告都通過但 job 仍顯示 cancelled，可再跑一次或檢查 repo 的 Actions 設定（concurrency、timeout）。

## 🔗 相關資源

- [GitHub Actions 文件](https://docs.github.com/en/actions)
- [pytest 文件](https://docs.pytest.org/)
- [Allure 文件](https://docs.qameta.io/allure/)
