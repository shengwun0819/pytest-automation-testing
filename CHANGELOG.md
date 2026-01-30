# 更新日誌

所有重要的變更都會記錄在此文件中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
版本號遵循 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

## [Unreleased]

### 變更
- 移除 PostgreSQL/MySQL 相關邏輯：`utils/assert_response.py` 僅使用 `status_code` 驗證狀態碼；`mock_server/README.md` 表格改為「真實關聯式資料庫」描述。
- GitHub Actions：修正 artifact 檔名含冒號導致上傳失敗（報告路徑與時間格式不含 `:`）、Allure 目錄與權限處理、NumPy 版本相容 Python 3.13 等。

## [1.0.0] - 2026-01-30

### 新增
- 初始版本發布
- 完整的 API 自動化測試框架
- Mock Server（Flask + SQLite），無需 PostgreSQL/MySQL 即可執行測試
- CSV 驅動的參數化測試
- Allure 測試報告
- 完整的驗證器系統
- 範例測試案例和測試資料
- 完整的文檔（README、架構文件、貢獻指南）
- GitHub Actions CI：測試、Allure 報告、test_report HTML 上傳

### 核心功能
- BaseAPI：統一的 API 請求封裝
- Mock Server：Flask + SQLite 模擬後端與資料庫
- Validator：API 回應驗證
- FileProcess：測試資料讀取
- Assert：統一的斷言方法

### 測試功能
- 支援多環境配置
- 支援測試標籤過濾（`--tags=regression`）
- 支援測試資料驅動
- 支援預期結果驗證
- 支援測試報告生成（Allure、HTML）
