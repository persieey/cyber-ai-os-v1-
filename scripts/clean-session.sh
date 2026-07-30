#!/bin/bash
# scripts/clean-session.sh — Reset workspace/active/ for a fresh session
# Usage: bash scripts/clean-session.sh [--hard]
#   default : archive current session then clear active/
#   --hard  : delete without archiving

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ACTIVE="$ROOT/workspace/active"
ARCHIVE="$ROOT/workspace/archive"

if [ ! -f "$ACTIVE/session.md" ]; then
  echo "[*] No active session found."
  exit 0
fi

TARGET="$ARCHIVE/session-$(date '+%Y%m%d-%H%M%S').md"

if [ "$1" = "--hard" ]; then
  rm -f "$ACTIVE/session.md"
  echo "[+] Hard reset — session deleted (no archive)"
else
  mkdir -p "$ARCHIVE"
  cp "$ACTIVE/session.md" "$TARGET"
  rm -f "$ACTIVE/session.md"
  echo "[+] Session archived to: $TARGET"
  echo "[+] workspace/active/ is now clean"
fi
