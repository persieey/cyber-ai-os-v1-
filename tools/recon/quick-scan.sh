#!/bin/bash
# quick-scan.sh — Full recon pipeline: nmap + web enum
# Usage: ./quick-scan.sh <target-ip> [domain]

# Load config
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
# shellcheck source=../../config/_load.sh
source "$PROJECT_ROOT/config/_load.sh" 2>/dev/null || true

TARGET=$1
DOMAIN=$2
OUTPUT_DIR="${WS_ACTIVE:-workspace/active}"

if [ -z "$TARGET" ]; then
  echo "Usage: $0 <target-ip> [domain]"
  exit 1
fi

echo "============================================"
echo "[*] Quick Scan: $TARGET"
echo "============================================"

# Phase 1: Fast port discovery
echo ""
echo "[Phase 1] Fast port discovery..."
PORTS=$(nmap -p- --min-rate 5000 -T4 "$TARGET" -oG - 2>/dev/null | grep "Ports:" | grep -oP '\d+/open' | cut -d/ -f1 | tr '\n' ',')
echo "[+] Open ports: $PORTS"

# Phase 2: Service scan on open ports
echo ""
echo "[Phase 2] Service/version scan..."
nmap -sV -sC -p"$PORTS" "$TARGET" -oN "$OUTPUT_DIR/nmap-full.txt" 2>/dev/null
echo "[+] Saved to $OUTPUT_DIR/nmap-full.txt"

# Phase 3: Web enum (if 80/443 open)
if echo "$PORTS" | grep -qE "80|443|8080|8443"; then
  echo ""
  echo "[Phase 3] Web enumeration..."

  PROTO="http"
  PORT=80
  echo "$PORTS" | grep -q "443" && PROTO="https" && PORT=443

  URL="$PROTO://$TARGET"

  echo "[*] WhatWeb fingerprint..."
  whatweb "$URL" 2>/dev/null | tee "$OUTPUT_DIR/whatweb.txt"

  echo ""
  echo "[*] Directory bruteforce (gobuster)..."
  gobuster dir -u "$URL" \
    -w "${WL_DIRECTORY:-/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt}" \
    -x php,html,txt,js,py \
    -t 50 --no-error -q \
    -o "$OUTPUT_DIR/gobuster.txt" 2>/dev/null
  echo "[+] Saved to $OUTPUT_DIR/gobuster.txt"
fi

# Phase 4: DNS enum (if domain provided)
if [ -n "$DOMAIN" ]; then
  echo ""
  echo "[Phase 4] DNS enumeration ($DOMAIN)..."
  dig "$DOMAIN" ANY 2>/dev/null | tee "$OUTPUT_DIR/dns.txt"
  echo "[*] Attempting zone transfer..."
  dig axfr "$DOMAIN" 2>/dev/null | tee -a "$OUTPUT_DIR/dns.txt"
fi

echo ""
echo "============================================"
echo "[+] Scan complete. Results in $OUTPUT_DIR/"
echo "============================================"
