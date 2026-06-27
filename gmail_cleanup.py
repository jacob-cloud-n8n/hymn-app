#!/usr/bin/env python3
"""Gmail 批次清理 + 自動分類腳本 — 使用已有 OAuth token"""

import json, os, sys, time
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser("~/.gmail-mcp/credentials.json")

with open(TOKEN_PATH) as f:
    tok = json.load(f)

CLIENT_SECRET_PATH = os.path.expanduser(
    "~/Downloads/client_secret_21892808378-87c0tvohebm2h8qsv3oi097bmcnujsvq.apps.googleusercontent.com.json"
)
with open(CLIENT_SECRET_PATH) as f:
    client_data = json.load(f)
inst = client_data.get("installed", client_data.get("web", {}))

creds = Credentials(
    token=tok["access_token"],
    refresh_token=tok["refresh_token"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=inst["client_id"],
    client_secret=inst["client_secret"],
    scopes=tok["scope"].split(" "),
)

gmail = build("gmail", "v1", credentials=creds)

LABELS = {
    "01-急/需回覆":   "#ff0000",
    "02-團隊/AI":     "#4285f4",
    "03-客戶專案":    "#34a853",
    "04-系統通知":    "#fbbc04",
    "05-一般":        "#a0a0a0",
}

# ============================================================
# 第一步：建立標籤
# ============================================================
def setup_labels():
    existing = {l["name"]: l["id"] for l in gmail.users().labels().list(userId="me").execute()["labels"]}
    for name, color in LABELS.items():
        if name not in existing:
            body = {"name": name, "labelListVisibility": "labelShow", "messageListVisibility": "show",
                    "color": {"backgroundColor": color, "textColor": "#ffffff"}}
            gmail.users().labels().create(userId="me", body=body).execute()
            print(f"建立標籤: {name}")
        else:
            print(f"標籤已存在: {name}")

# ============================================================
# 第二步：預覽 — 統計各時期的郵件數量
# ============================================================
def preview():
    now = datetime.now()
    thresholds = [
        ("> 5 年前", now - timedelta(days=5*365)),
        ("3-5 年前", now - timedelta(days=3*365)),
        ("2-3 年前", now - timedelta(days=2*365)),
        ("1-2 年前", now - timedelta(days=1*365)),
        ("6月-1年前", now - timedelta(days=180)),
        ("最近6個月", now - timedelta(days=180)),
    ]

    print("\n=== Gmail 收件匣預覽 ===")
    total = 0
    for i, (label, since) in enumerate(thresholds):
        if i < len(thresholds) - 1:
            before = thresholds[i+1][1]
            query = f"before:{since.strftime('%Y/%m/%d')} after:{before.strftime('%Y/%m/%d')}"
        else:
            query = f"after:{since.strftime('%Y/%m/%d')}"

        result = gmail.users().messages().list(userId="me", q=query, maxResults=1).execute()
        count = result.get("resultSizeEstimate", 0)
        total += count
        action = "🗑 刪除" if "2-3" in label or "3-5" in label or "> 5" in label else ("📦 封存" if "1-2" in label else "📥 保留")
        print(f"  {action}  {label}: ~{count:,} 封")

    print(f"\n  總計約: {total:,} 封")
    print("\n=== 建議操作 ===")
    print("  > 2 年前 → 🗑 刪除（移到垃圾桶，30天後永久清除）")
    print("  1-2 年前  → 📦 封存（保留可搜尋，收件匣清空）")
    print("  1 年內    → 📥 保留在收件匣")

# ============================================================
# 第三步：執行清理
# ============================================================
def execute_cleanup():
    now = datetime.now()
    cutoff_delete = (now - timedelta(days=2*365)).strftime("%Y/%m/%d")
    cutoff_archive = (now - timedelta(days=1*365)).strftime("%Y/%m/%d")

    print(f"\n🗑 刪除 before:{cutoff_delete}（超過 2 年）")
    deleted = batch_process(f"before:{cutoff_delete}", "trash")
    print(f"✅ 已移到垃圾桶: {deleted} 封")

    print(f"\n📦 封存 before:{cutoff_archive} after:{cutoff_delete}（1-2 年）")
    archived = batch_process(f"before:{cutoff_archive} after:{cutoff_delete}", "archive")
    print(f"✅ 已封存: {archived} 封")

    print(f"\n=== 清理完成 ===")
    print(f"🗑 垃圾桶: {deleted} 封")
    print(f"📦 封存: {archived} 封")

def batch_process(query, action, batch_size=100):
    count = 0
    page_token = None
    while True:
        result = gmail.users().messages().list(
            userId="me", q=query, maxResults=batch_size,
            pageToken=page_token
        ).execute()
        messages = result.get("messages", [])
        if not messages:
            break

        ids = [m["id"] for m in messages]
        if action == "trash":
            gmail.users().messages().batchDelete(userId="me", body={"ids": ids}).execute()
        elif action == "archive":
            gmail.users().messages().batchModify(
                userId="me", body={"ids": ids, "removeLabelIds": ["INBOX"]}
            ).execute()

        count += len(ids)
        print(f"  處理中... {count} 封", end="\r")
        time.sleep(1.2)

        page_token = result.get("nextPageToken")
        if not page_token:
            break
    return count

# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "preview":
        setup_labels()
        preview()
        print("\n執行清理請加參數: python3 gmail_cleanup.py execute")
    elif sys.argv[1] == "execute":
        setup_labels()
        execute_cleanup()
