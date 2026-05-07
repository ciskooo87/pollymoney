#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
cd frontend
npm install >/dev/null
set -a
source ../deploy/frontend.env
set +a
npm run build >/dev/null
nohup npm run start -- --hostname 127.0.0.1 --port 3015 > ../deploy/frontend.log 2>&1 &
echo $! > ../deploy/frontend.pid
