#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for name in frontend backend; do
  if [ -f "$name.pid" ]; then
    pid=$(cat "$name.pid" || true)
    if [ -n "${pid:-}" ] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" || true
    fi
    rm -f "$name.pid"
  fi
done
