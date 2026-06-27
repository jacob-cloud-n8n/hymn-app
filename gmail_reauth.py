#!/usr/bin/env python3
"""重新取得 Gmail OAuth Token"""

import json, os, urllib.parse, urllib.request, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

CLIENT_SECRET_PATH = os.path.expanduser(
    "~/Downloads/client_secret_21892808378-87c0tvohebm2h8qsv3oi097bmcnujsvq.apps.googleusercontent.com.json"
)
with open(CLIENT_SECRET_PATH) as f:
    data = json.load(f)
inst = data.get("installed", data.get("web", {}))
CLIENT_ID = inst["client_id"]
CLIENT_SECRET = inst["client_secret"]
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"  # Out-of-band (manual copy)

SCOPES = "https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/gmail.settings.basic"

# 生成授權 URL
auth_url = (
    "https://accounts.google.com/o/oauth2/v2/auth?"
    + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
    })
)

print("="*70)
print("請點擊以下連結授權 Gmail 存取權限：")
print()
print(auth_url)
print()
print("授權後會顯示一串 code，請複製貼回來。")
print("="*70)

# 嘗試用瀏覽器開啟
try:
    os.system(f'open "{auth_url}"')
except:
    pass

code = input("\n請貼上 authorization code: ").strip()

# 交換 token
token_data = urllib.parse.urlencode({
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}).encode()

req = urllib.request.Request(
    "https://oauth2.googleapis.com/token",
    data=token_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
resp = urllib.request.urlopen(req)
token = json.loads(resp.read())

# 儲存
SAVE_PATH = os.path.expanduser("~/.gmail-mcp/credentials.json")
with open(SAVE_PATH, "w") as f:
    json.dump(token, f, indent=2)

print(f"\n✅ Token 已儲存至 {SAVE_PATH}")
print(f"   access_token: {token['access_token'][:20]}...")
print(f"   refresh_token: {'已獲取' if 'refresh_token' in token else '未獲取（可能之前授權過）'}")
print(f"   expires_in: {token.get('expires_in', 'N/A')} 秒")
