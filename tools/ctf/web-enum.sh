#!/bin/bash
# web-enum.sh — Web enumeration pipeline: gobuster + ffuf + nikto
# Usage: ./web-enum.sh <url> [wordlist]

# Load config
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$PROJECT_ROOT/config/_load.sh" 2>/dev/null || true

URL=$1
WORDLIST=${2:-"${WL_DIRECTORY:-/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt}"}
OUTPUT_DIR="${WS_ACTIVE:-workspace/active}"

if [ -z "$URL" ]; then
  echo "Usage: $0 <url> [wordlist]"
  echo "Example: $0 http://10.10.10.1"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "============================================"
echo "[*] Web Enum: $URL"
echo "============================================"

# Tech fingerprint
echo ""
echo "[1] Tech fingerprint:"
whatweb "$URL" 2>/dev/null
curl -sI "$URL" 2>/dev/null | grep -E "Server:|X-Powered-By:|Content-Type:|Set-Cookie:" | sed 's/^/    /'

# gobuster dirs
echo ""
echo "[2] Directory enum (gobuster)..."
gobuster dir -u "$URL" \
  -w "$WORDLIST" \
  -x php,html,txt,js,asp,aspx,py,sh,bak,zip,sql \
  -t 50 --no-error -q \
  -o "$OUTPUT_DIR/gobuster-dirs.txt" 2>/dev/null
echo "[+] Found $(wc -l < "$OUTPUT_DIR/gobuster-dirs.txt") entries → $OUTPUT_DIR/gobuster-dirs.txt"
cat "$OUTPUT_DIR/gobuster-dirs.txt"

# ffuf vhost enum
echo ""
echo "[3] VHost fuzzing (ffuf)..."
HOST=$(echo "$URL" | sed 's|https\?://||' | cut -d/ -f1)
ffuf -u "$URL" \
  -H "Host: FUZZ.$HOST" \
  -w "${WL_DNS:-/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt}" \
  -mc 200,301,302,403 \
  -t 50 -s \
  -o "$OUTPUT_DIR/ffuf-vhost.json" 2>/dev/null
echo "[+] vhost results → $OUTPUT_DIR/ffuf-vhost.json"

# nikto quick scan
echo ""
echo "[4] Nikto vulnerability scan..."
nikto -h "$URL" -o "$OUTPUT_DIR/nikto.txt" -Format txt 2>/dev/null
echo "[+] Saved to $OUTPUT_DIR/nikto.txt"

echo ""
echo "============================================"
echo "[+] Done. Results in $OUTPUT_DIR/"
echo "============================================"
