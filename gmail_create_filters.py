#!/usr/bin/env python3
"""建立 Gmail 自動分類篩選器"""

import json, os, requests

with open(os.path.expanduser("~/.gmail-mcp/credentials.json")) as f:
    tok = json.load(f)
HEADERS = {"Authorization": f"Bearer {tok['access_token']}", "Content-Type": "application/json"}

def create_filter(criteria, action):
    url = "https://gmail.googleapis.com/gmail/v1/users/me/settings/filters"
    body = {"criteria": criteria, "action": action}
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code == 200:
        print(f"  ✅ 已建立: {json.dumps(criteria)[:60]}...")
        return True
    else:
        print(f"  ⚠️ 失敗: {r.status_code} - {r.text[:100]}")
        return False

# 先列出現有篩選器
r = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/settings/filters", headers={"Authorization": f"Bearer {tok['access_token']}"})
existing = r.json().get("filter", [])
print(f"現有篩選器: {len(existing)} 個")
print("將追加新篩選器，保留現有設定。\n")

print("\n=== 建立自動分類篩選器 ===\n")

filters = [
    # 1. 緊急：團隊來信 + 主旨含 error/urgent
    {
        "criteria": {
            "from": "(codex OR hermes OR antigravity OR opencode OR n8n)",
            "subject": "(error OR 錯誤 OR urgent OR 緊急 OR down OR crash)"
        },
        "action": {
            "addLabelIds": ["Label_1"],  # 01-急/需回覆
            "addLabelIdsNames": ["01-急/需回覆"],
            "shouldArchive": False,
            "markImportant": True
        }
    },
    # 2. 團隊溝通
    {
        "criteria": {"from": "(codex OR hermes OR antigravity OR opencode OR mimocode OR claude OR n8n OR anti-gravity)"},
        "action": {
            "addLabelIdsNames": ["02-團隊/AI"],
            "shouldArchive": False
        }
    },
    # 3. 客戶專案
    {
        "criteria": {"subject": "(美地 OR 琢石 OR 羊奶 OR STAR OR 書僮 OR 課程 OR 客戶 OR client OR invoice OR 合約 OR 報價)"},
        "action": {
            "addLabelIdsNames": ["03-客戶專案"],
            "markImportant": True
        }
    },
    # 4. 系統通知（noreply 類）
    {
        "criteria": {"from": "(noreply OR no-reply OR notification OR @google.com OR @github.com OR @firebase.com OR telegram OR discord)"},
        "action": {
            "addLabelIdsNames": ["04-系統通知"],
            "shouldArchive": True,
            "markImportant": False
        }
    },
    # 5. Google 帳號通知 → 封存
    {
        "criteria": {"from": "(accounts.google.com OR no-reply@accounts.google.com)"},
        "action": {
            "addLabelIdsNames": ["04-系統通知"],
            "shouldArchive": True,
            "markImportant": False
        }
    },
]

# 需要先取得 label ID
labels_resp = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/labels", headers={"Authorization": f"Bearer {tok['access_token']}"})
labels_map = {l["name"]: l["id"] for l in labels_resp.json().get("labels", [])}
print(f"現有標籤: {list(labels_map.keys())[:10]}...")

success = 0
for f in filters:
    # 將標籤名稱轉換為 ID
    label_names = f["action"].get("addLabelIdsNames", [])
    label_ids = []
    for name in label_names:
        if name in labels_map:
            label_ids.append(labels_map[name])
        else:
            print(f"  ⚠️ 標籤不存在: {name}")
    if label_ids:
        f["action"]["addLabelIds"] = label_ids
    f["action"].pop("addLabelIdsNames", None)
    
    if create_filter(f["criteria"], f["action"]):
        success += 1

print(f"\n{'='*50}")
print(f"完成: {success}/{len(filters)} 個篩選器已建立")
print(f"{'='*50}")
