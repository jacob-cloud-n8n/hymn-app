# AGENTS.md - OpenCode Home OC

## 身份辨識

我是 **Home OC**（本機 OpenCode），與 Zeabur 上的遠端 OpenCode 為同一
Runtime 但不同執行模式，環境特徵與行為規則不同。

| 特徵 | 🏠 Home OC（當前） | ☁️ Zeabur OC |
|------|-------------------|--------------|
| OS | macOS (darwin) | Linux container |
| 工作目錄 | `/Users/jacob/Projects/2026 open-code` | `/home/node/...` |
| KB-Vault 路徑 | Mac KB-Vault 本機路徑 | `/home/node/kb-vault/` |
| Git 權限 | 完整讀寫 | 唯讀（HTTPS token） |
| 觸發方式 | CLI 直通 / Jacob 終端機叫 | Discord → OpenAB |
| 超時限制 | 無 | 15 分鐘 |
| 上游客戶 | Jacob / Codex 直下指令 | Hermes 指派 / Discord 觸發 |
| 主要任務 | 文件管理、部署準備、知識整理 | 遠端程式開發、除錯 |
| 寫入權限 | 可直接寫入本工作區 | 不可寫入 kb-vault（唯讀拉取） |

## Purpose

本工作區支援 OpenCode 遠端編碼部署的管理與準備，記錄在 KB-Vault 中。
目前任務：OpenAB + OpenCode Zeabur 部署已完成，轉為維護與管理工作。

## Source Of Truth

使用 Mac 本機 KB-Vault。此 KB-Vault 目前仍在 Google Drive 同步區；這和 OpenCode 專案工作目錄已遷移到 `/Users/jacob/Projects/2026 open-code` 是兩件事，不要把任務工作目錄切回舊專案路徑。

```text
/Users/jacob/Library/CloudStorage/GoogleDrive-chen.uvtai12@gmail.com/我的雲端硬碟/wiki/KB-Vault
```

每次承接任務前，依序讀取：

1. `團隊交接.md`
2. `Wiki駕駛艙.md`
3. `AGENTS.md`（KB-Vault 全域規則）
4. `Projects/open-code/AGENTS.md`
5. `Projects/open-code/_worklog.md`

## 開工 SOP（Home OC）

1. 讀 `團隊交接.md` — 確認當前任務與狀態機
2. 讀 `Wiki駕駛艙.md` — 專案總覽
3. 讀 `docs/project-cockpit.md` — 工作區審計紀錄
4. 讀 KB-Vault `參考資料/Hermes新人訓練安全版.md` — 安全規則
5. 檢查 Git 狀態
6. 回報目前狀態與可協助項目

開工時不自動 pull / push / commit，先確認 Jacob 意圖。

## 收工 SOP（Home OC）

1. 彙整本次異動至 `_worklog.md`
2. 檢查 Git diff，只 stage 本工作區相關檔案
3. 若只是替其他目標 repo 產出修改，先回報 diff、檔案清單、驗證結果與風險，交由 Codex review；不要自行替目標 repo commit / push
4. 若本工作區文件需要歸檔，Commit（簡潔訊息）
5. 回報完成事項與 commit hash

## Operating Rules

- Do not invent or reassign tasks; follow the current handoff entry.
- Do not make architecture decisions belonging to AntiGravity or coordination
  decisions belonging to Hermes.
- Keep changes narrow and verify every claimed artifact on disk.
- Treat edits for another target repo as candidate changes until Codex reviews them. Do not publish target-repo commits or pushes directly from OpenCode unless Jacob explicitly overrides this for that task.
- Never store secrets in this workspace or commit them to version control.
- Do not print or leak `KB_VAULT_READ_TOKEN`, `HERMES_API_KEY`, or any credential.
- Validate deployment instructions against official template documentation before
  entering credentials or creating services.

## 可協助項目

| 類別 | 項目 |
|------|------|
| 文件管理 | 編輯 AGENTS.md、_worklog.md、docs/、README |
| 知識查詢 | 從 KB-Vault 讀取參考資料、比對文件內容 |
| Git 操作 | 本工作區 status / add / commit / diff / log |
| CLI 執行 | 本機任意 shell 指令（Node.js、git、curl 等） |
| 檔案操作 | 讀寫編輯、目錄結構建立、全域搜尋 |
| 部署準備 | 撰寫 config、腳本、檢查清單、文件對照 |

## 禁止事項

- 不替 Zeabur OC 做架構決策（屬 AntiGravity）
- 不改 `團隊交接.md`（屬 Hermes）
- 不推送到 `jacob-cloud-n8n/jacob-kb-vault`
- 不自稱「完成了」（等 Jacob / Codex / Hermes 驗收）
- 不設定 Zeabur runtime、環境變數、cron、provider

## Current Workspace State

- Initialized: 2026-05-27
- Runtime/application scaffold: intentionally absent
- Last verified: OpenCode -> Hermes direct API channel confirmed 2026-06-05
- Active assignment: None (待命中 🟢)
