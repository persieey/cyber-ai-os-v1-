#!/bin/bash
# stego-check.sh — Run full steganography toolkit on a file
# Usage: ./stego-check.sh <file> [password]

FILE=$1
PASS=${2:-""}
OUTPUT_DIR="workspace/active/stego-$(basename "$FILE")"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 <file> [password]"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "============================================"
echo "[*] Stego Check: $FILE"
echo "============================================"

# File identification
echo ""
echo "[1] File type:"
file "$FILE"
exiftool "$FILE" 2>/dev/null | grep -E "Comment|Description|Artist|Software|GPS" | sed 's/^/    /'

# Strings
echo ""
echo "[2] Interesting strings:"
strings "$FILE" | grep -E "flag|CTF|password|secret|key|hidden|\{|\}" | head -20

# binwalk
echo ""
echo "[3] Embedded files (binwalk):"
binwalk "$FILE" 2>/dev/null
binwalk -e "$FILE" -C "$OUTPUT_DIR/binwalk/" --quiet 2>/dev/null
ls "$OUTPUT_DIR/binwalk/" 2>/dev/null && echo "    [+] Extracted to $OUTPUT_DIR/binwalk/"

# steghide
echo ""
echo "[4] steghide extract:"
if [ -n "$PASS" ]; then
  steghide extract -sf "$FILE" -p "$PASS" -xf "$OUTPUT_DIR/steghide-out" 2>/dev/null \
    && echo "    [+] Extracted! → $OUTPUT_DIR/steghide-out" \
    || echo "    [-] Wrong password or no data"
else
  steghide extract -sf "$FILE" -p "" -xf "$OUTPUT_DIR/steghide-out" 2>/dev/null \
    && echo "    [+] Extracted (empty pass)! → $OUTPUT_DIR/steghide-out" \
    || echo "    [-] No data with empty password (try: $0 $FILE <password>)"
fi

# zsteg (PNG/BMP)
if echo "$FILE" | grep -qiE "\.png|\.bmp"; then
  echo ""
  echo "[5] zsteg (LSB):"
  zsteg "$FILE" 2>/dev/null | head -20
fi

# stegoveritas
if command -v stegoveritas &>/dev/null; then
  echo ""
  echo "[6] stegoveritas auto-analysis:"
  stegoveritas "$FILE" -out "$OUTPUT_DIR/stegoveritas/" 2>/dev/null
  echo "    Results in $OUTPUT_DIR/stegoveritas/"
fi

# Hex tail (data after EOF)
echo ""
echo "[7] Data after EOF marker:"
if file "$FILE" | grep -qi "jpeg\|jpg"; then
  python3 -c "
data = open('$FILE','rb').read()
idx = data.rfind(b'\xff\xd9')
if idx != -1 and idx+2 < len(data):
    print('[+] Found data after JPEG EOF:')
    print(data[idx+2:idx+200])
else:
    print('[-] Nothing after JPEG EOF')
" 2>/dev/null
fi

echo ""
echo "============================================"
echo "[+] Done. Full output in $OUTPUT_DIR/"
echo "============================================"
