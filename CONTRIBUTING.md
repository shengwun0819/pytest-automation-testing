# 貢獻指南

感謝您對本專案的關注！本指南將幫助您了解如何為專案做出貢獻。

## 📋 專案背景

本專案是一個 API 自動化測試框架範例，改寫自實際的企業級測試框架。專案保留了核心架構和設計模式，移除了公司特定的業務邏輯和機密資訊，作為學習和參考的範例。

## 🎯 如何貢獻

### 1. 報告問題

如果您發現了 bug 或有改進建議，請：

1. 檢查 [Issues](https://github.com/your-username/api-automation-testing/issues) 是否已有相關問題
2. 如果沒有，請建立新的 Issue，包含：
   - 問題描述
   - 重現步驟
   - 預期行為
   - 實際行為
   - 環境資訊（Python 版本、作業系統等）

### 2. 提交 Pull Request

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 3. 程式碼規範

- 遵循 PEP 8 Python 程式碼風格
- 使用有意義的變數和函數名稱
- 添加適當的註解和文檔字串
- 確保所有測試通過

### 4. 測試

在提交 PR 前，請確保：

- 所有現有測試通過
- 新增的功能有對應的測試
- 程式碼通過 linter 檢查

## 📝 開發指南

### 新增 API 端點測試

1. 在 `api/example/` 中新增 API 方法
2. 在 `tests/` 中建立測試檔案
3. 在 `test_data/dev/` 中新增測試資料（CSV 和預期結果）

### 新增驗證器

1. 在 `Validator/` 中建立新的驗證器類別
2. 繼承 `Validator` 基礎類別
3. 實作自訂驗證邏輯

## 🤝 行為準則

- 尊重所有貢獻者
- 建設性的批評和建議
- 保持專業和友善的溝通

## 📄 授權

貢獻的程式碼將遵循本專案的 MIT 授權。
