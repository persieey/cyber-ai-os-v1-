# Skill: FFuf

## Purpose
Fast web fuzzer — ค้นหา directories, files, parameters, virtual hosts, และ API endpoints ด้วยความเร็วสูง

## When to Use
- Phase: Enumeration
- ต้องการ fuzz เร็วกว่า gobuster (multi-thread, flexible)
- Parameter fuzzing
- POST body fuzzing
- VHost fuzzing
- หา API endpoints

## Installation
```bash
sudo apt install ffuf
# หรือ
go install github.com/ffuf/ffuf/v2@latest
```

## Command Reference

### Directory Fuzzing
```bash
# Basic
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://<target>/FUZZ

# พร้อม extensions
ffuf -w /usr/share/wordlists/dirb/common.txt \
     -u http://<target>/FUZZ \
     -e .php,.html,.txt,.js,.bak

# Filter by size (กรอง false positives)
ffuf -w wordlist.txt -u http://<target>/FUZZ -fs <size_of_404>

# Filter by status code
ffuf -w wordlist.txt -u http://<target>/FUZZ -fc 404,403

# Save output
ffuf -w wordlist.txt -u http://<target>/FUZZ -o result.json -of json
```

### GET Parameter Fuzzing
```bash
# หา hidden parameters
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
     -u "http://<target>/page?FUZZ=value"

# Fuzz parameter value
ffuf -w payloads.txt -u "http://<target>/page?id=FUZZ"

# Filter ตาม response size (หา anomaly)
ffuf -w payloads.txt -u "http://<target>/page?id=FUZZ" -fs <normal_size>
```

### POST Body Fuzzing
```bash
# Form login fuzzing
ffuf -w passwords.txt \
     -u http://<target>/login \
     -X POST \
     -d "username=admin&password=FUZZ" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -fc 200   # filter 200 ถ้า fail คือ 200

# JSON body
ffuf -w payloads.txt \
     -u http://<target>/api/login \
     -X POST \
     -d '{"username":"admin","password":"FUZZ"}' \
     -H "Content-Type: application/json"
```

### VHost / Subdomain Fuzzing
```bash
# Virtual host discovery
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
     -u http://<target-IP> \
     -H "Host: FUZZ.<domain>" \
     -fs <default_size>

# ตัวอย่าง: target 10.10.10.10, domain = target.htb
ffuf -w subdomains.txt \
     -u http://10.10.10.10 \
     -H "Host: FUZZ.target.htb" \
     -fs 1234
```

### API Endpoint Discovery
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/api/objects.txt \
     -u http://<target>/api/FUZZ \
     -mc 200,201,204
```

## Flags อธิบาย

| Flag | ความหมาย |
|------|---------|
| `-w` | Wordlist path (`FUZZ` = placeholder) |
| `-u` | URL (ใส่ `FUZZ` ที่ต้องการ fuzz) |
| `-e` | Extensions (ต่อท้าย FUZZ) |
| `-X` | HTTP method (default: GET) |
| `-d` | POST body data |
| `-H` | Custom header |
| `-t` | Threads (default 40) |
| `-fc` | Filter: status codes (comma-separated) |
| `-fs` | Filter: response size |
| `-fw` | Filter: word count |
| `-fl` | Filter: line count |
| `-mc` | Match: status codes |
| `-ms` | Match: size |
| `-o` | Output file |
| `-of` | Output format (json, csv, html) |
| `-c` | Colorize output |

## หา False Positive Size
```bash
# รัน request ที่รู้ว่า 404 ก่อน → ดู size
curl -I http://<target>/nonexistentpage123
# ดู Content-Length → ใช้เป็น -fs value
```

## Output ที่ต้องสังเกต
```
/admin              [Status: 301, Size: 0, Words: 1, Lines: 1]
/login.php          [Status: 200, Size: 2345, Words: 120, Lines: 45]
/config.bak         [Status: 200, Size: 8932, Words: 201, Lines: 89]  ← น่าสนใจ!
```

## Wordlists ที่แนะนำ
```
สำหรับ directory:
/usr/share/wordlists/dirb/common.txt              → เร็ว
/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt → ครอบคลุม

สำหรับ file:
/usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt

สำหรับ subdomain:
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

สำหรับ parameter:
/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
```
