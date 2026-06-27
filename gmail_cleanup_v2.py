#!/usr/bin/env python3
"""Gmail 批次清理 + 自動分類腳本 — 直接 HTTP + access_token"""

import json, os, sys, time, requests
from datetime import datetime, timedelta

TOKEN_PATH = os.path.expanduser("~/.gmail-mcp/credentials.json")
with open(TOKEN_PATH) as f:
    tok = json.load(f)
ACCESS_TOKEN = tok["access_token"]
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def gmail_api(method, path, params=None, json_body=None):
    url = f"https://gmail.googleapis.com/gmail/v1/users/me/{path}"
    if method == "GET":
        r = requests.get(url, headers=HEADERS, params=params or {})
    elif method == "POST":
        r = requests.post(url, headers=HEADERS, json=json_body)
    elif method == "PUT":
        r = requests.put(url, headers=HEADERS, json=json_body)
    else:
        r = requests.request(method, url, headers=HEADERS, json=json_body)
    if r.status_code == 401:
        print("⚠️ Token 已過期，需要重新授權。")
        sys.exit(1)
    r.raise_for_status()
    return r.json()

LABELS = {
    "01-急/需回覆":   {"bg": "#ff0000", "text": "#ffffff"},
    "02-團隊/AI":     {"bg": "#4285f4", "text": "#ffffff"},
    "03-客戶專案":    {"bg": "#34a853", "text": "#ffffff"},
    "04-系統通知":    {"bg": "#fbbc04", "text": "#000000"},
    "05-一般":        {"bg": "#a0a0a0", "text": "#ffffff"},
}

# ============================================================
# 第一步：建立標籤
# ============================================================
def setup_labels():
    result = gmail_api("GET", "labels")
    existing = {l["name"]: l["id"] for l in result.get("labels", [])}
    for name in LABELS.keys():
        if name not in existing:
            body = {"name": name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
            try:
                gmail_api("POST", "labels", json_body=body)
                print(f"  ✅ 建立標籤: {name}")
            except Exception as e:
                print(f"  ⚠️ 標籤建立失敗: {name} — {e}")
        else:
            print(f"  ℹ️ 標籤已存在: {name}")

# ============================================================
# 第二步：預覽 — 只統計，不動任何郵件
# ============================================================
def preview():
    now = datetime.now()
    buckets = [
        ("📊 所有郵件總數", ""),
        ("🗑 超過 2 年前（將刪除）", f"before:{(now - timedelta(days=2*365)).strftime('%Y/%m/%d')}"),
        ("📦 1-2 年前（將封存）", f"before:{(now - timedelta(days=1*365)).strftime('%Y/%m/%d')} after:{(now - timedelta(days=2*365)).strftime('%Y/%m/%d')}"),
        ("📥 最近 1 年內（保留）", f"after:{(now - timedelta(days=1*365)).strftime('%Y/%m/%d')}"),
    ]

    print("\n" + "="*60)
    print("📋 Gmail 收件匣預覽（只統計，不動任何郵件）")
    print("="*60)

    for label, query in buckets:
        if not query:
            result = gmail_api("GET", "messages", {"maxResults": 1})
            count = result.get("resultSizeEstimate", 0)
            print(f"\n  {label}: ~{count:,} 封")
        else:
            result = gmail_api("GET", "messages", {"q": query, "maxResults": 1})
            count = result.get("resultSizeEstimate", 0)
            print(f"  {label}: ~{count:,} 封")

    print("\n" + "="*60)
    print("⚠️ 重要：以下操作將永久影響郵件，請確認：")
    print("  • 🗑 刪除 = 移到垃圾桶（30天後永久清除）")
    print("  • 📦 封存 = 保留可搜尋，但從收件匣移除")
    print("  • 📥 保留 = 不動")
    print("="*60)
    print("\n執行清理前請先確認 OK。")

# ============================================================
# 第三步：取得樣本（讓用戶確認）
# ============================================================
def show_samples():
    now = datetime.now()
    
    # 顯示 2 年前最舊的 3 封郵件主旨
    cutoff = (now - timedelta(days=2*365)).strftime("%Y/%m/%d")
    print(f"\n🗑 將刪除的信件樣本（before:{cutoff}）：")
    result = gmail_api("GET", "messages", {"q": f"before:{cutoff}", "maxResults": 3})
    for msg in result.get("messages", []):
        detail = gmail_api("GET", f"messages/{msg['id']}", {"format": "metadata", "metadataHeaders": ["Subject", "From", "Date"]})
        headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        print(f"    [{headers.get('Date','')[:16]}] {headers.get('From','')[:30]:30} | {headers.get('Subject','')[:50]}")

    # 顯示 1-2 年前的 3 封郵件主旨
    cutoff_del = (now - timedelta(days=2*365)).strftime("%Y/%m/%d")
    cutoff_arc = (now - timedelta(days=1*365)).strftime("%Y/%m/%d")
    print(f"\n📦 將封存的信件樣本（before:{cutoff_arc} after:{cutoff_del}）：")
    result = gmail_api("GET", "messages", {"q": f"before:{cutoff_arc} after:{cutoff_del}", "maxResults": 3})
    for msg in result.get("messages", []):
        detail = gmail_api("GET", f"messages/{msg['id']}", {"format": "metadata", "metadataHeaders": ["Subject", "From", "Date"]})
        headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        print(f"    [{headers.get('Date','')[:16]}] {headers.get('From','')[:30]:30} | {headers.get('Subject','')[:50]}")

# ============================================================
# 第四步：執行清理（需使用者確認後才呼叫）
# ============================================================
def execute_cleanup():
    now = datetime.now()
    cutoff_delete = (now - timedelta(days=2*365)).strftime("%Y/%m/%d")
    cutoff_archive = (now - timedelta(days=1*365)).strftime("%Y/%m/%d")

    print(f"\n🗑 開始刪除 before:{cutoff_delete}")
    deleted = batch_process(f"before:{cutoff_delete}", "trash")
    print(f"\n✅ 已移到垃圾桶: {deleted} 封")

    print(f"\n📦 開始封存 before:{cutoff_archive} after:{cutoff_delete}")
    archived = batch_process(f"before:{cutoff_archive} after:{cutoff_delete}", "archive")
    print(f"\n✅ 已封存: {archived} 封")

    print(f"\n{'='*60}")
    print(f"清理完成：🗑 {deleted} 封 | 📦 {archived} 封")
    print(f"{'='*60}")

def batch_process(query, action):
    count = 0
    while True:
        result = gmail_api("GET", "messages", {"q": query, "maxResults": 100})
        messages = result.get("messages", [])
        if not messages:
            break
        for m in messages:
            mid = m["id"]
            if action == "trash":
                try:
                    gmail_api("POST", f"messages/{mid}/trash")
                except Exception as e:
                    print(f"  ⚠️ Trash failed {mid}: {e}")
            elif action == "archive":
                try:
                    gmail_api("POST", "messages/batchModify", json_body={"ids": [mid], "removeLabelIds": ["INBOX"]})
                except Exception as e:
                    print(f"  ⚠️ Archive failed {mid}: {e}")
            count += 1
            if count % 10 == 0:
                print(f"  處理中... {count} 封", end="\r")
            time.sleep(0.2)
    return count

# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "preview":
        setup_labels()
        preview()
        print(f"\n顯示樣本請加參數: python3 gmail_cleanup_v2.py sample")
    elif sys.argv[1] == "sample":
        setup_labels()
        show_samples()
        print(f"\n確認後執行: python3 gmail_cleanup_v2.py execute")
    elif sys.argv[1] == "execute":
        execute_cleanup()
    else:
        print("用法:")
        print("  preview  — 統計數量（不動郵件）")
        print("  sample   — 顯示樣本主旨讓你確認")
        print("  execute  — 執行刪除+封存（需你先確認 OK）")
