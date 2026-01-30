# 更新日誌

所有重要的變更都會記錄在此文件中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
版本號遵循 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

## [1.0.0] - 2025-01-XX

### 新增
- 初始版本發布
- 完整的 API 自動化測試框架
- 支援 PostgreSQL 和 MySQL
- CSV 驅動的參數化測試
- Allure 測試報告
- 完整的驗證器系統
- 範例測試案例和測試資料
- 完整的文檔（README、架構文件、貢獻指南）

### 核心功能
- BaseAPI：統一的 API 請求封裝
- DBSqlalchemy：跨資料庫的資料庫操作
- Validator：API 回應驗證
- FileProcess：測試資料讀取
- Assert：統一的斷言方法

### 測試功能
- 支援多環境配置
- 支援測試標籤過濾
- 支援測試資料驅動
- 支援預期結果驗證
- 支援測試報告生成
