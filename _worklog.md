# Home OC — 工作日誌

## 2026-06-05 — Home OC 身分初始化 ✅

- **目標**：建立本機 OpenCode 獨立身分，與 Zeabur OC 明確區隔
- **執行項目**：
  - 讀取 KB-Vault 全數參考文件（團隊交接、Wiki駕駛艙、Hermes訓練、開發規則等）
  - 裝備檔案技能（huashu-design、Impeccable、Superpowers架構等）
  - 改寫 `AGENTS.md`：加入 Home OC 身分辨別表、開工/收工 SOP、可協助項目
- **結果**：Home OC 身分建立完成，待命中 🟢

## 2026-06-05 — 第一項任務：AI Agent 展示準備 ✅

- **目標**：建立 Home OC 作為客戶現場 demo 的工具
- **執行項目**：
  - 建立 `demo/README.md` 展示菜單（6 大類、15+ 子項目）
  - 建立展示 SOP，記錄在 `demo/README.md` 尾部
  - 實測項目 **1a — 檔案分類整理** ✅ 驗證通過
- **展示 SOP 要點**：
  - 在桌面建立資料夾，用 Finder 讓客戶眼見為憑
  - 每步驟做完要停，讓客戶看到階段變化
  - 先分類歸位 → 再清理檔名 → 最後展示
- **結果**：展示模式確立，待下一項展示任務 🟢

## 2026-06-05 — 展示項目 3b 方案比較 ✅

- **目標**：展示 AI 從主題搜尋到產出 HTML 比較表的完整能力
- **執行項目**：
  - 客戶主題：「LINE」
  - 比較對象：LINE 官方帳號 vs 自建聊天機器人平台
  - 從 KB-Vault grep 搜尋 LINE 相關資料
  - 產出 10 項維度比較表 + 結論區塊
  - 格式：先 MD → 客戶反應不友善 → 改產 HTML（瀏覽器開啟）✅
- **紀錄**：展示 SOP 已寫入 `demo/README.md`
- **結果**：done 🟢

## 2026-06-05 — 展示項目 6c HTML 互動簡報 ✅

- **目標**：展示 AI 即時產出多頁 HTML 簡報的能力
- **執行項目**：
  - 客戶主題：LINE + n8n 串接優勢
  - 產出 5 頁互動式 HTML 簡報（封面 / 痛點對比 / 流程 / 場景 / 總結）
  - 支援鍵盤 ← → 翻頁 + 滑鼠點擊切換
  - 瀏覽器直接開啟，客戶可自行操作
- **紀錄**：展示 SOP 已寫入 `demo/README.md`，菜單新增 6c 項目
- **結果**：done 🟢

## 2026-06-05 — 展示項目 3a 網頁抓取分析 ✅

- **目標**：展示 AI 從公開網頁抓取資料並產出分析報告
- **執行項目**：
  - 客戶給 URL：`apple.com/tw`
  - 使用 webfetch 抓取頁面（< 5 秒）
  - 分析頁面結構、產品線、主打活動
  - 產出 HTML 分析報告（含 AI 觀點總結）
  - 限制：需登入/JS 渲染的網站無法抓取
- **結果**：done 🟢

## 2026-06-11 — 製作 05-workflow 教學版 ✅

- **目標**：將 `skills/05-workflow/SKILL.md` 改寫為學員教學版
- **執行項目**：
  - 讀取原始 `SKILL.md`（開工/收工/初始化流程）
  - 補充「為什麼」說明、不做會怎樣的對照表
  - 新增敏感資料檢查清單（關鍵字搜尋、`.env` 檢查）
  - 新增收工筆記模板（可直接複製貼上）
  - 新增 Git 正確操作（`git add -p`、不用 `git add .`）
  - 新增 `.gitignore` 範例、`ANTIGRAVITY.md` 範本、`README.md` 範本
  - 新增常見錯誤對照表（7 個常見錯誤 + 正確做法）
  - 新增中斷/暫停處理流程
  - 新增開工/收工口訣快速參考卡
  - **另存為** `skills/05-workflow/SKILL-teaching.md`，**不覆蓋原始檔**
- **結果**：
  - 新檔案：`2026 antig2/skills/05-workflow/SKILL-teaching.md`（267 行）
  - 原始檔案 `SKILL.md` 保留未更動
  - Commit：`870430f`（已提交至 `2026 antig2`）
  - 狀態：done 🟢

## 2026-06-13 — 查詢 Kimi 模型狀態 ✅

- **目標**：確認 Kimi 模型今天是否有異常
- **執行項目**：
  - 查詢 Moonshot AI 官方狀態頁面（`status.moonshot.cn`）
  - 檢查今天（6/13）事件與近期歷史
- **結果**：
  - 今天（6/13）核心模型正常，只有短暫短信登錄問題（11:09-11:59，已解決）
  - **Agentic 模型（Researcher / Kimi Agent）6/1-6/11 反覆不穩定**，多次錯誤報警
  - 6/2 最嚴重（7次報警），影響 Agent 任務延長或阻塞
  - 無檔案變更，無需 commit
  - 狀態：done 🟢

## 2026-06-19 — 詩歌點播網頁製作 ✅

- **目標**：將 4 本 PDF 詩歌本做成手機點播網頁（比照既有 App 截圖）
- **執行項目**：
  - 安裝 PyPDF2（`python3 -m pip install PyPDF2`）轉換 5 個 PDF 為文字檔
  - 4 本可讀取：《大本詩歌》(818頁)、《新歌頌詠》(149頁)、《新詩》(90頁)、《補充本詩歌_2012版》(525頁)
  - 1 本無法提取文字：《新詩歌譜輯 V1.0》（圖片型樂譜），暫時放棄
  - 撰寫 `parse_hymns.py` 解析文字為結構化 JSON（編號/歌名/調性/歌詞）
  - 解析結果：大本 148 首 / 新歌 122 首 / 新詩 75 首 / 補充本 512 首（共 857 首）
  - 建立前端：`index.html` + `style.css` + `app.js`
    - 比照截圖風格：暖色背景、圓形數字鍵、分頁切換、純文字歌詞頁
    - 功能：數字點播 / 分類切換 / 歌詞顯示 / 目錄搜尋 / 上下首切換
    - RWD：手機優先，最大寬度 480px 置中
    - 互動：鍵盤支援（0-9/Backspace/Enter）、觸控滑動切換上下首
  - 測試：本機 `python3 -m http.server 8765` 驗證資料載入正常
- **檔案清單**：
  - `hymn-app/index.html`
  - `hymn-app/style.css`
  - `hymn-app/app.js`
  - `hymn-app/parse_hymns.py`
  - `hymn-app/data/hymns.json`
  - `tmp_pdf_txt/`（4 個 txt 轉檔，暫存）
- **已知限制**（待後續修復）：
  - 大本詩歌僅解析 148 首（PDF 格式不規則，部分跳號未抓到）
  - 新歌頌詠/新詩數量偏多（解析器誤判部分非歌詞內容為歌曲）
  - 部分歌曲歌詞全擠在一行（PDF 提取問題），已用「一)」「副)」自動分段
  - 4 本資料中均無「附」編號詩歌
  - 暫無音樂/樂譜播放，純文字版
- **後續可擴充**：
  - 修復解析器，補齊大本詩歌全部 188+ 首
  - 清理新歌頌詠/新詩誤判資料
  - 加入書籤功能（localStorage）
  - 加入播放清單（多首連播）
  - 加入 MP3 音檔連結
  - 做成 PWA（離線使用）
  - 部署到 GitHub Pages 或 Zeabur
- **2026-06-19 晚間更新**：
  - Jacob 提供大本詩歌完整目錄網址：`churchinmontereypark.org/Docs/Hymn/firstBookHymnIndex.html`
  - 從網頁抓取完整目錄：1~780 + 附1~附6，共 786 筆（解析後 351 首有明確標題）
  - 合併既有歌詞資料：大本詩歌從 148 首擴充至 351 首（345 首有完整歌詞，6 首暫無歌詞）
  - **修復 JavaScript 語法錯誤**：`app.js:56` 正則表達式 `\d/\d` 未轉義斜線，導致整個腳本無法載入。修正為 `\d\/\d`
  - **修復 UX 問題**：從歌詞頁/目錄頁返回撥號盤時，輸入值未清除。現在會自動清空
  - 歌詞分段邏輯正常運作：以「一)」「二)」「副)」自動分段顯示
  - Playwright 截圖驗證通過：附1（暫無歌詞）、010（有歌詞分段顯示）均正常
- **狀態**：done 🟢，本機伺服器運行中 `http://localhost:8765`，待 Jacob 實機測試

## 2026-06-19 (後續) — 收工彙整 + 同步團隊區 ✅

- **收工動作**：
  - 更新本工作區 `_worklog.md`：修正大本詩歌有歌詞數量為 345 首，補充 6 首暫無歌詞原因
  - 將進度報告同步至 KB-Vault：`Projects/open-code/_worklog.md`
  - KB-Vault 本地 commit：`c5f15c5`
  - 將 `tmp_pdf_txt/` 加入 `.gitignore`，避免臨時轉檔被提交
  - 本工作區 commit：`4e6828e`
- **6 首暫無歌詞原因**：
  - 第 180 首在 hymnal.net 為外部連結（gracefinder.com），未抓取
  - 附1~附6 在 hymnal.net 的 URL 路徑與一般編號不同，尚未對應

## 2026-06-22 — 詩歌 app 轉交 mimocode + 開工收工文件搜尋 ✅

- **事件**：Jacob 指示詩歌點播網頁改由 **MiMoCode** 接手處理
- **執行項目**：
  - 提供開工/收工 skill 給 Jacob：
    - `~/.codex/skills/startup-sync/SKILL.md`
    - `~/.codex/skills/shutdown-sync/SKILL.md`
  - 搜尋並比對其他開工/收工 SOP 文件：
    - KB-Vault `參考資料/Hermes新人訓練安全版.md`（新人訓練 + 安全規則 + 開工收工流程）
    - `~/Projects/2026 codex/docs/專案工作流程.md`（Codex 專案開工/收工流程）
    - `~/Projects/2026 antig2/ANTIGRAVITY.md`（AntiGravity 懶人包開工/收工/初始化流程）
  - `Documents/Obsidian Vault/` 無相關開工收工文件
- **狀態**：
  - 詩歌 app 後續由 MiMoCode 接手
  - 開工/收工 SOP 最終交付版本待 Jacob / AntiGravity 確認
  - Home OC 不再主動處理詩歌 app 程式碼修改

## 2026-06-23 — AGENTS.md 同步團隊共識 + 提案建立 + 推薦碼確認 ✅

### 1. 團隊共識同步
- **事件**：Jacob 指示讀取 antig2 新團隊共識並同步至 Home OC 工作區
- **來源**：`/Users/jacob/Projects/2026 antig2/團隊共識-開工收工初始化.md`（2026-06-22 建立）
  - 這份正是前次一直找不到的「開工/收工說明」— 由 Claude 在 6/22 統一建立
- **同步至 `AGENTS.md` 的變更**：
  - 開工 SOP：加入讀 `團隊共識-開工收工初始化.md` + `團隊專區.md`「📋 今日重點」+ 限制載入規則
  - 收工 SOP：新增安全掃描步驟（api_key/token/secret 等敏感字）、`git add .` 禁令、治理 repo 只 stage 不 commit/push（AG 統一執行）
  - 新增 Agent 分工矩陣（6 人：Claude/AG/Codex/OpenCode/Hermes/n8n）
  - 新增 Loop Engineering 5 條防護規則
  - 安全鐵律獨立成章（5 條）
  - 禁止事項新增「不用 `git add .`」
  - 狀態更新：詩歌 app 轉交 MiMoCode，最後同步日期 2026-06-23
- **Commit**：`80c6062`（本工作區）+ `a5e7918`（收工記錄）

## 2026-06-27 — 開工 + 簡報查找 ✅

- **開工摘要**：
  - 團隊共識已更新至 2026-06-25：新增「團隊通訊協議」章節
  - 🎉 提案 A（「阻塞於」欄位）已被 AG 採納並實施
  - `團隊專區.md`：OpenCode 暫緩，無指派任務
- **執行項目**：
  - 協助查找「隨身書僮簡報第一課」→ `antig2/草屯班簡報/第1堂-認識AI書僮/index.html`
  - htmlpreview 失敗（400）、local server 端口衝突，最終用 `open` 在瀏覽器開啟 ✅
- **狀態**：待命中 🟢
