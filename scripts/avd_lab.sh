#!/usr/bin/env bash
# Launch (or print instructions for) the Aether lab AVD.
set -euo pipefail
AVD_NAME="${AVD_NAME:-AetherLab}"

if ! command -v emulator >/dev/null 2>&1; then
  echo "Install Android Studio / SDK platform-tools and put emulator on PATH."
  exit 1
fi

echo "Starting $AVD_NAME with writable system + QEMU gdb stub (:1234)"
emulator -avd "$AVD_NAME" -writable-system -qemu -s "$@"
