#!/bin/bash
# forensics-check.sh — Quick forensics triage on any file
# Usage: ./forensics-check.sh <file>

FILE=$1
OUTPUT_DIR="workspace/active/forensics-$(basename "$FILE")"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 <file>"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "============================================"
echo "[*] Forensics Check: $FILE"
echo "============================================"

# File info
echo ""
echo "[1] File identification:"
file "$FILE"
ls -lh "$FILE"
echo "MD5:    $(md5sum "$FILE" | cut -d' ' -f1)"
echo "SHA256: $(sha256sum "$FILE" | cut -d' ' -f1)"

# Metadata
echo ""
echo "[2] Metadata (exiftool):"
exiftool "$FILE" 2>/dev/null | grep -vE "^ExifTool|^File Name|^Directory|^File Size|^File Modification" | sed 's/^/    /'

# Strings
echo ""
echo "[3] Interesting strings:"
strings "$FILE" | grep -E "flag|CTF|password|secret|key|http|ftp|\{.*\}" | head -30

# Hex dump header
echo ""
echo "[4] File header (hex):"
xxd "$FILE" | head -8

# binwalk
echo ""
echo "[5] Embedded files (binwalk):"
binwalk "$FILE" 2>/dev/null
echo ""
echo "[*] Extracting embedded files..."
binwalk -e "$FILE" -C "$OUTPUT_DIR/extracted/" --quiet 2>/dev/null
if [ -d "$OUTPUT_DIR/extracted/" ]; then
  echo "[+] Extracted:"
  find "$OUTPUT_DIR/extracted/" -type f | sed 's/^/    /'
else
  echo "    Nothing extracted"
fi

# foremost (file carving)
if command -v foremost &>/dev/null; then
  echo ""
  echo "[6] File carving (foremost):"
  foremost -i "$FILE" -o "$OUTPUT_DIR/foremost/" -q 2>/dev/null
  cat "$OUTPUT_DIR/foremost/audit.txt" 2>/dev/null | tail -10
fi

# PCAP specific
if file "$FILE" | grep -qi "pcap\|tcpdump"; then
  echo ""
  echo "[7] PCAP analysis:"
  echo "  Protocols:"
  tshark -r "$FILE" -q -z io,phs 2>/dev/null | head -20
  echo "  HTTP requests:"
  tshark -r "$FILE" -Y http.request -T fields -e ip.src -e http.host -e http.request.uri 2>/dev/null | head -20
  echo "  Credentials in cleartext:"
  tshark -r "$FILE" -Y "ftp || telnet || http.authorization" -T fields -e frame.number -e _ws.col.Info 2>/dev/null | head -20
fi

echo ""
echo "============================================"
echo "[+] Done. Output in $OUTPUT_DIR/"
echo "============================================"
