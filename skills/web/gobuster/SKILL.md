# Skill: Gobuster

## Purpose
Directory/file brute-force และ DNS/VHost enumeration — หา paths, files, subdomains, virtual hosts ที่ซ่อนอยู่

## When to Use
- Phase: Enumeration
- ต้องการหา directories หรือ files ที่ไม่ได้ link มา
- ต้องการ enumerate subdomains
- ต้องการหา virtual hosts

## Installation
```bash
sudo apt install gobuster
# หรือ
go install github.com/OJ/gobuster/v3@latest
```

## Command Reference

### Directory Mode (`dir`) — ใช้บ่อยที่สุด
```bash
# Basic
gobuster dir -u http://<target> -w /usr/share/wordlists/dirb/common.txt

# พร้อม file extensions
gobuster dir -u http://<target> -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,js,bak

# CTF standard — ครอบคลุมกว่า
gobuster dir -u http://<target> \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -x php,html,txt,js,bak \
  -t 40 \
  -o gobuster_output.txt

# HTTPS (ignore SSL errors)
gobuster dir -u https://<target> -w wordlist.txt -k

# Custom headers (เช่น authenticated)
gobuster dir -u http://<target> -w wordlist.txt -H "Cookie: session=<value>"
```

### DNS Mode — Subdomain Enumeration
```bash
# Basic subdomain enum
gobuster dns -d <domain.com> -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Show IPs
gobuster dns -d <domain.com> -w subdomains.txt -i

# Larger wordlist
gobuster dns -d <domain.com> -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
```

### VHost Mode — Virtual Host Discovery
```bash
gobuster vhost -u http://<target-IP> -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain

# หาก domain คือ target.htb
gobuster vhost -u http://target.htb -w subdomains.txt --append-domain
```

## Flags อธิบาย

| Flag | ความหมาย |
|------|---------|
| `-u` | URL เป้าหมาย |
| `-w` | Wordlist path |
| `-x` | Extensions (php,html,txt) |
| `-t` | Threads (default 10, แนะนำ 40-100 สำหรับ lab) |
| `-o` | Output file |
| `-k` | Skip SSL verification |
| `-H` | Custom header |
| `-b` | Blacklist status codes (เช่น `-b 404,403`) |
| `--append-domain` | ต่อ domain กับ subdomain ใน vhost mode |

## Wordlists ที่แนะนำ

```
/usr/share/wordlists/dirb/common.txt              → เร็ว สำหรับ quick check
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt → ครอบคลุมขึ้น
/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt → แนะนำสำหรับ CTF
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt → DNS/VHost
```

## Output Interpretation

```
/admin               (Status: 301) [Size: 312]  → redirect (น่าสนใจ)
/login.php           (Status: 200) [Size: 1245]  → page ที่เข้าถึงได้
/config.php          (Status: 403) [Size: 287]   → forbidden (อาจมีข้อมูลสำคัญ)
/backup.zip          (Status: 200) [Size: 98234]  → ไฟล์ backup น่าดาวน์โหลด!
```

## What to Look For
- Status 200 + ชื่อน่าสนใจ (admin, backup, config, upload)
- Status 301/302 → follows redirect → มี path จริง
- Status 403 → อาจ bypass ได้ (`//path`, `/%2e/path`)
- ไฟล์ .bak, .old, .swp, .zip → backup files มักมี source code

## Next Steps After Gobuster
- /admin หรือ /login → ลอง default credentials หรือ bypass
- /upload → ลอง file upload vulnerability
- .php files → ลอง parameter fuzzing
- .bak/.zip → download และตรวจหา credentials/source
