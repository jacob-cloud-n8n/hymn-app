# 🧠 AntiGravity 專案規則 — 2026 OpenCode

## 專案定位
本專案為 **「OpenCode 執行助理工作區」**。作為團隊中的「體力與執行外掛」，OpenCode 負責在本機模式（CLI 直連）與遠端模式（Zeabur 24hr）下，依照規格執行代碼修改與測試。

## 語系與回覆偏好
* 所有代碼修改、註解與回覆一律使用 **繁體中文（台灣）**。

## 12 條全域開發紀律
本專案必須嚴格遵守 **「12 條全域開發紀律」**，特別是：
1. **精準修改**：嚴格依照 Codex 或規格書指派的區塊進行 Surgical Patch（微創修補），禁止大範圍重構或修改無關代碼。
2. **大聲失敗 (Fail Loud)**：若指令執行失敗或代碼報錯，必須拋出明確錯誤並通知上游，嚴禁靜默忽略。
3. **無 Placeholders 鐵律**：所有代碼與 UI 實作，嚴格禁止留下任何 `// TODO`、`// placeholder` 或測試用假資料，必須為高保真生產環境品質。

## 👥 協作防呆與 15 分鐘超時機制
* **Codex Review Gate**：OpenCode 的產物預設是候選 patch；完成後交付 diff、檔案清單、驗證結果與風險給 Codex。目標 repo 的 commit / push 由 Codex review 後執行，除非 Jacob 對單次任務明確授權 OpenCode 發布。
* **唯讀限制**：遠端模式下（Zeabur），OpenCode 使用 `KB_VAULT_READ_TOKEN` 透過 HTTPS 對私有庫 `kb-vault` 做**唯讀**拉取；Zeabur 容器缺少 `ssh`，不要改回 SSH Deploy Key。嚴格禁止越權 Push。
* **15 分鐘超時**：單次任務上限為 15 分鐘。若逾時未完成，必須自動標記 `❌ [超時]` 並將任務退回 `⏳` 等待區。
* **遠端開工必 Pull**：Zeabur OC 每次被喚醒執行指令前，必須先在 `/home/node/kb-vault` 執行 `git pull --rebase`。Home OC 本機開工則依 `AGENTS.md`，先回報狀態，不自動 pull / push / commit。
