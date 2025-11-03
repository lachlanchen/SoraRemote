#!/usr/bin/env bash
set -euo pipefail

# Fixed debug port to reuse login cache
PORT="${PORT:-9333}"
PROFILE_DIR="${SORA_PROFILE_DIR:-$HOME/chrome_sora_profile_${PORT}}"

# Text to type (all args joined)
TEXT="${*:-A calm lake at sunrise, cinematic.}"

python -m agents.sora_agent \
  --debugger-port "$PORT" \
  --start-chrome \
  --no-headless \
  --user-data-dir "$PROFILE_DIR" \
  --timeout "${TIMEOUT:-90}" \
  --login-timeout "${LOGIN_TIMEOUT:-600}" \
  --text "$TEXT"

