# OpenCode 遠端編碼工作區

這個資料夾用於準備與追蹤 OpenCode 的遠端編碼環境。最新交接規劃是透過
Zeabur 上的 OpenAB 服務連接 OpenCode，供外出遠端編碼與受控的工程任務使用。

## 目前狀態

- 狀態：Discord 部署完成並通過首次唯讀驗收（2026-05-27）
- 目前任務：`OpenAB + OpenCode Zeabur 部署` 已完成
- 已驗證：Discord 觸發 OpenCode thread 回覆，預設模型為 DeepSeek `deepseek-v4-pro`
- 狀態來源：KB-Vault 的 `團隊交接.md`

## 開工讀取順序

Mac 上的 KB-Vault 根目錄（目前仍在 Google Drive 同步區；OpenCode 專案工作目錄本身已在 `/Users/jacob/Projects/2026 open-code`）：

```text
~/Library/CloudStorage/GoogleDrive-chen.uvtai12@gmail.com/我的雲端硬碟/wiki/KB-Vault/
```

開始部署或遠端編碼任務前，依序讀取：

1. `團隊交接.md`
2. `Wiki駕駛艙.md`
3. `AGENTS.md`
4. `Projects/open-code/AGENTS.md`
5. `Projects/open-code/_worklog.md`

## 部署決策

- 採用 Zeabur `OpenAB OpenCode` 官方模板的 Discord 原生連線路線。
- Discord 手機版已能滿足外出使用，不追加 Telegram gateway 或 webhook。
- 模型預設採 DeepSeek API `deepseek-v4-pro`；`deepseek-v4-flash` 僅作低風險快速任務備選。
- Discord webhook URL 不能取代 OpenAB 所需的 Bot Token。
- Discord 目前限制於指定頻道；實際操作使用 Bot 身分組提及，已納入 OpenAB role trigger。

## 操作界線

- 不自行新增或改派任務。
- 每項實作都需當場驗證實際產出，不能只以文字回報完成。
- Bot Token 與 API Key 僅保存在 Zeabur 私密變數，不寫入文件。
- DeepSeek key 會提供給 OpenCode agent 使用；不以遠端指令處理來源不明的提示或檔案。

## 本地文件

- `AGENTS.md`：這個工作區的固定操作規則
- `docs/project-cockpit.md`：初始化盤點與後續檢核紀錄

## KB-Vault 可重用文件

- `Projects/open-code/OpenAB部署指南.md`：正式部署設定
- `Projects/open-code/OpenAB部署懶人包.md`：下次部署與排錯的快速流程
- `Projects/open-code/OpenAB部署實戰紀錄-2026-05-27.md`：首次成功部署完整過程與驗證依據
