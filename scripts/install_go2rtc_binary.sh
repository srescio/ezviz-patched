#!/usr/bin/env bash
# Home Assistant in Docker expects `go2rtc` on PATH when using default_config (no go2rtc URL).
# Idempotent: skips download if /usr/local/bin/go2rtc already runs.
set -euo pipefail

GO2RTC_VER="${GO2RTC_VER:-1.9.14}"
TARGET="${GO2RTC_INSTALL_PATH:-/usr/local/bin/go2rtc}"

if [[ -x "$TARGET" ]] && "$TARGET" -version 2>/dev/null | grep -q "go2rtc version"; then
  echo "go2rtc already installed: $($TARGET -version 2>&1 | head -1)"
  exit 0
fi

GO2RTC_ARCH=""
case "$(uname -m)" in
  x86_64) GO2RTC_ARCH="amd64" ;;
  aarch64) GO2RTC_ARCH="arm64" ;;
  armv7l) GO2RTC_ARCH="arm" ;;
  armv6l) GO2RTC_ARCH="armv6" ;;
  *) echo "install_go2rtc_binary: unsupported arch $(uname -m)" >&2; exit 1 ;;
esac

echo "Downloading go2rtc ${GO2RTC_VER} (linux_${GO2RTC_ARCH})..."
curl -fsSL -o "$TARGET" \
  "https://github.com/AlexxIT/go2rtc/releases/download/v${GO2RTC_VER}/go2rtc_linux_${GO2RTC_ARCH}"
chmod +x "$TARGET"
"$TARGET" -version
