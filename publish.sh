#!/bin/bash
# 公開はこれ1本：暗号化ビルド → 見せた資料を共有フォルダにPDF保存 → push
set -e; cd "$(dirname "$0")"
node build.mjs "$(cat .key)" >/dev/null
python3 hozon.py
git add -A; git commit -qm "${1:-更新}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || true
git push -q && echo pushed
