#!/bin/bash
# subdomain-enum.sh — Passive + active subdomain enumeration
# Usage: ./subdomain-enum.sh <domain>

DOMAIN=$1
OUTPUT_DIR="workspace/active"

if [ -z "$DOMAIN" ]; then
  echo "Usage: $0 <domain>"
  exit 1
fi

echo "============================================"
echo "[*] Subdomain Enum: $DOMAIN"
echo "============================================"

mkdir -p "$OUTPUT_DIR"
OUTFILE="$OUTPUT_DIR/subdomains-$DOMAIN.txt"
> "$OUTFILE"

# subfinder (passive)
if command -v subfinder &>/dev/null; then
  echo "[*] subfinder (passive)..."
  subfinder -d "$DOMAIN" -silent | tee -a "$OUTFILE"
fi

# amass (passive)
if command -v amass &>/dev/null; then
  echo "[*] amass passive..."
  amass enum -passive -d "$DOMAIN" 2>/dev/null | tee -a "$OUTFILE"
fi

# dnsrecon bruteforce
if command -v dnsrecon &>/dev/null; then
  echo "[*] dnsrecon bruteforce..."
  dnsrecon -d "$DOMAIN" -D /usr/share/wordlists/dnsmap.txt -t brt 2>/dev/null \
    | grep "\[+\]" | tee -a "$OUTFILE"
fi

# Deduplicate + resolve
echo ""
echo "[*] Deduplicating and resolving..."
sort -u "$OUTFILE" -o "$OUTFILE"
COUNT=$(wc -l < "$OUTFILE")

echo ""
echo "[+] Found $COUNT unique subdomains → $OUTFILE"

# Quick HTTP check on each
echo "[*] Checking live HTTP(S)..."
while IFS= read -r sub; do
  if curl -s --connect-timeout 3 -o /dev/null -w "%{http_code}" "http://$sub" 2>/dev/null | grep -qE "^[23]"; then
    echo "  [LIVE] http://$sub"
  fi
done < "$OUTFILE"
