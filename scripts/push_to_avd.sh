#!/usr/bin/env bash
# Copy this repo's aether/ package into a running rooted emulator.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

adb wait-for-device
adb root || true
adb shell mkdir -p /data/local/aether
adb push "$ROOT/aether" /data/local/aether/aether
echo "On device:  adb shell  then  PYTHONPATH=/data/local/aether python3 -m aether.cli"
echo "If the image has no python3, install Termux or push a static python later."
