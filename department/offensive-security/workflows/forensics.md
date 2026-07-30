# Digital Forensics CTF Workflow

## Purpose
แนวทางทำ Forensics CTF challenge อย่างมีระบบ ตั้งแต่ identify artifact จนถึงหา hidden data หรือ flag

## Phases

---

### Phase 1: Identify Artifact
**Goal:** รู้ว่า file นี้คืออะไรจริงๆ

```bash
file <artifact>              # type detection จาก magic bytes
exiftool <artifact>          # metadata ทั้งหมด
xxd <artifact> | head -20    # hex dump (ดู magic bytes)
strings <artifact>           # readable strings
```

Magic bytes ที่พบบ่อย:
| Bytes | File Type |
|-------|-----------|
| 89 50 4E 47 | PNG |
| FF D8 FF | JPEG |
| 50 4B 03 04 | ZIP |
| 25 50 44 46 | PDF |
| 4D 5A | Windows PE (.exe) |
| 7F 45 4C 46 | Linux ELF |

Done when: รู้ file type จริง (ไม่ใช่แค่ extension)

---

### Phase 2: Extract Data
**Goal:** ดึง data ที่ซ่อนอยู่ออกมา

#### Embedded Files
```bash
binwalk <file>               # scan for embedded files
binwalk -e <file>            # extract all embedded files
foremost -i <file>           # file carving
```

#### Steganography (Images)
```bash
# JPEG
steghide info <image.jpg>    # มีข้อมูลซ่อนอยู่ไหม?
steghide extract -sf <image.jpg>   # extract (อาจต้องใช้ password)

# PNG
zsteg <image.png>            # LSB steganography
stegsolve                    # visual analysis (แต่ละ bit plane)

# ทั่วไป
strings <image> | grep -i "flag\|ctf"
xxd <image> | grep -i "flag"
```

#### Steganography (Audio)
```bash
# Spectrogram analysis
# ดูด้วย Audacity → Spectrogram view
# ดูด้วย Sonic Visualizer → Add layer → Spectrogram
# หา Morse code ใน audio
# DTMF tones
```

#### PCAP Analysis
```bash
# tshark
tshark -r capture.pcap -Y "http"
tshark -r capture.pcap -T fields -e http.request.uri -e http.file_data
tshark -r capture.pcap --export-objects http,./extracted/

# Wireshark filters
http                              # HTTP traffic
ftp-data                         # FTP file transfers
dns                              # DNS queries
tcp.stream eq 0                  # First TCP stream
frame contains "flag"            # หา "flag" ใน packets
```

#### Memory Dump (Volatility)
```bash
# Identify OS
volatility -f mem.dmp imageinfo

# Process list
volatility -f mem.dmp --profile=<Profile> pslist

# Network connections
volatility -f mem.dmp --profile=<Profile> netscan

# Clipboard
volatility -f mem.dmp --profile=<Profile> clipboard

# Dump process memory
volatility -f mem.dmp --profile=<Profile> memdump -p <PID> -D ./
```

---

### Phase 3: Analyze & Decode
**Goal:** แปลงข้อมูลที่ได้เป็น flag

```python
# Decode encoded strings
import base64
base64.b64decode("...")

# XOR decode
bytes([c ^ key for c in data])

# Reverse strings
"string"[::-1]
```

---

### Phase 4: Documentation
1. อัพเดต `workspace/active/session.md` → Findings
2. บันทึก technique ใน `/kb add ctf <technique>`
3. รัน Report Agent

---

## Forensics CTF Checklist

```
□ file <file>              → identify type
□ exiftool <file>          → metadata (GPS? Author? Comment?)
□ strings <file>           → readable content
□ xxd <file> | head        → magic bytes
□ binwalk <file>           → embedded files
□ binwalk -e <file>        → extract embedded
□ steghide extract         → JPEG steg
□ zsteg <file>             → PNG steg (LSB)
□ volatility               → memory dump
□ tshark / Wireshark       → PCAP analysis
□ foremost / photorec      → file carving (disk image)
```

## Quick Reference

```
File ID   → file + xxd + exiftool
Steg      → steghide + zsteg + stegsolve
PCAP      → tshark + Wireshark + follow stream
Memory    → volatility imageinfo → pslist/netscan/clipboard
Carving   → binwalk -e + foremost
```
