#!/usr/bin/env bash
# Start Home Assistant for local dev. If another instance already uses the same
# config dir (/.ha_run.lock), stop it first so "Run Task" does not fail with
# "Another Home Assistant instance is already running".
#
# Set EZVIZ_HA_KEEP_EXISTING=1 to skip stopping (fail if lock is held).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="${HASS_CONFIG:-/config}"
LOCK="${CONFIG}/.ha_run.lock"

_read_lock_pid() {
  python3 -c "
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
if not p.is_file() or p.stat().st_size == 0:
    sys.exit(1)
try:
    print(int(json.loads(p.read_text(encoding='utf-8'))['pid']))
except (KeyError, ValueError, json.JSONDecodeError, OSError):
    sys.exit(1)
" "$LOCK" 2>/dev/null || true
}

_stop_existing_ha() {
  local pid
  pid="$(_read_lock_pid)"
  [[ -n "${pid:-}" ]] || return 0
  if ! kill -0 "$pid" 2>/dev/null; then
    return 0
  fi
  echo "Stopping existing Home Assistant (PID ${pid}) using ${CONFIG} ..."
  kill -TERM "$pid" 2>/dev/null || true
  local i
  for i in $(seq 1 30); do
    if ! kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
    sleep 1
  done
  if kill -0 "$pid" 2>/dev/null; then
    echo "PID ${pid} did not exit; sending SIGKILL" >&2
    kill -KILL "$pid" 2>/dev/null || true
    sleep 1
  fi
}

if [[ "${EZVIZ_HA_KEEP_EXISTING:-}" != "1" ]]; then
  _stop_existing_ha
  # Brief pause so /.ha_run.lock is released after the old process exits (helps terminal “reload”).
  sleep 0.5
fi

bash "${ROOT}/scripts/install_go2rtc_binary.sh"
exec hass -c "${CONFIG}" --debug -v "$@"
