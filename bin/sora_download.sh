#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-9333}"
PROFILE_DIR="${SORA_PROFILE_DIR:-$HOME/chrome_sora_profile_${PORT}}"
OUT_DIR="${OUT_DIR:-$PWD/downloads/sora}"

python -m agents.sora_download \
  --debugger-port "$PORT" \
  --start-chrome \
  --no-headless \
  --user-data-dir "$PROFILE_DIR" \
  --out-dir "$OUT_DIR" \
  "${@:-}"

