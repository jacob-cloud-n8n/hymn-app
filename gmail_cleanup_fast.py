#!/usr/bin/env python3
"""Gmail 批次清理 — batchModify 高效版"""

import json, os, time
from datetime import datetime, timedelta
import requests

with open(os.path.expanduser("~/.gmail-mcp/credentials.json")) as f:
    tok = json.load(f)
HEADERS = {"Authorization": f"Bearer {tok['access_token']}"}

def api(path, body=None):
    url = f"https://gmail.googleapis.com/gmail/v1/users/me/{path}"
    if body:
        r = requests.post(url, headers={**HEADERS, "Content-Type": "application/json"}, json=body)
    else:
        r = requests.get(url, headers=HEADERS)
    if r.status_code == 204:
        return {}
    r.raise_for_status()
    return r.json() if r.text else {}

now = datetime.now()
cutoff_del = (now - timedelta(days=2*365)).strftime("%Y/%m/%d")
cutoff_arc = (now - timedelta(days=1*365)).strftime("%Y/%m/%d")

print("📊 正在統計...")

# 檢查還有多少要處理
old_inbox = api(f"messages?q=in:inbox before:{cutoff_del}&maxResults=1").get("resultSizeEstimate", 0)
mid_inbox = api(f"messages?q=in:inbox before:{cutoff_arc} after:{cutoff_del}&maxResults=1").get("resultSizeEstimate", 0)

print(f"\n  收件匣中待刪除（before {cutoff_del}）: ~{old_inbox} 封")
print(f"  收件匣中待封存（{cutoff_del} - {cutoff_arc}）: ~{mid_inbox} 封")

# 批次刪除（移到垃圾桶）
if old_inbox > 0:
    print(f"\n🗑 開始刪除 before:{cutoff_del}...")
    count = 0
    while True:
        msgs = api(f"messages?q=in:inbox before:{cutoff_del}&maxResults=100").get("messages", [])
        if not msgs:
            break
        ids = [m["id"] for m in msgs]
        # batchModify: 添加 TRASH + 移除 INBOX
        api("messages/batchModify", {"ids": ids, "addLabelIds": ["TRASH"], "removeLabelIds": ["INBOX"]})
        count += len(ids)
        print(f"  已處理 {count} 封", end="\r")
        time.sleep(1)
    print(f"\n✅ 已移到垃圾桶: {count} 封")

# 批次封存（移除 INBOX）
if mid_inbox > 0:
    print(f"\n📦 開始封存 before:{cutoff_arc} after:{cutoff_del}...")
    count = 0
    while True:
        msgs = api(f"messages?q=in:inbox before:{cutoff_arc} after:{cutoff_del}&maxResults=100").get("messages", [])
        if not msgs:
            break
        ids = [m["id"] for m in msgs]
        api("messages/batchModify", {"ids": ids, "removeLabelIds": ["INBOX"]})
        count += len(ids)
        print(f"  已處理 {count} 封", end="\r")
        time.sleep(1)
    print(f"\n✅ 已封存: {count} 封")

print(f"\n{'='*50}")
print("🎉 清理完成！")
print(f"{'='*50}")
