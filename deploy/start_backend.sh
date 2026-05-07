#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
cd backend
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q -r requirements.txt
set -a
source ../deploy/backend.env
set +a
nohup .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8019 > ../deploy/backend.log 2>&1 &
echo $! > ../deploy/backend.pid
