# Tools

Automation scripts สำหรับ CTF และ Pentest — รันได้จริง ไม่ใช่แค่ reference

## Structure

```
tools/
├── recon/
│   ├── quick-scan.sh       nmap pipeline (port → service → web enum)
│   └── subdomain-enum.sh   subfinder + amass + dnsrecon
├── ctf/
│   ├── stego-check.sh      steghide + binwalk + zsteg + exiftool
│   ├── crypto-solver.py    XOR brute / Caesar / ROT13 / B64 / RSA small-e
│   ├── web-enum.sh         gobuster + ffuf vhost + nikto
│   └── forensics-check.sh  file triage + binwalk + pcap analysis
├── exploitation/
│   ├── rev-shell.py        generate reverse shell one-liners (all types)
│   └── hash-crack.sh       auto-identify + hashcat/john
├── utils/
│   ├── decode.py           auto-detect: b64/hex/url/rot13/binary/morse
│   └── hash-identify.py    identify hash type + suggest hashcat mode
└── reporting/
    └── gen-report.py       generate report from session.md
```

## Quick Usage

```bash
# Recon
./tools/recon/quick-scan.sh 10.10.10.1
./tools/recon/quick-scan.sh 10.10.10.1 example.com

# CTF
./tools/ctf/stego-check.sh challenge.png
./tools/ctf/stego-check.sh challenge.jpg "password123"
./tools/ctf/forensics-check.sh suspicious.bin
./tools/ctf/web-enum.sh http://10.10.10.1

python3 tools/ctf/crypto-solver.py xor-brute 4a2f3d1b...
python3 tools/ctf/crypto-solver.py caesar "KHOOR ZRUOG"
python3 tools/ctf/crypto-solver.py b64 "SGVsbG8="

# Exploitation
python3 tools/exploitation/rev-shell.py 10.10.14.1 4444
python3 tools/exploitation/rev-shell.py 10.10.14.1 4444 bash
./tools/exploitation/hash-crack.sh 5f4dcc3b5aa765d61d8327deb882cf99

# Utils
python3 tools/utils/decode.py "SGVsbG8gV29ybGQ="
python3 tools/utils/decode.py "68 65 6c 6c 6f"
python3 tools/utils/hash-identify.py 5f4dcc3b5aa765d61d8327deb882cf99

# Reporting
python3 tools/reporting/gen-report.py ctf
python3 tools/reporting/gen-report.py workspace/active/session.md --type=lab
```

## chmod (Linux/Kali)
```bash
chmod +x tools/recon/*.sh tools/ctf/*.sh tools/exploitation/*.sh
```
