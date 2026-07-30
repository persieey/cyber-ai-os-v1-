# Skill: John the Ripper

## Purpose
Password และ hash cracking — crack hashed passwords จาก database dumps, `/etc/shadow`, ไฟล์ที่ password-protected, หรือ CTF challenges

## When to Use
- Phase: Post-Enumeration หรือ Exploitation
- ได้ password hash มาจาก database dump (SQLi, dump)
- ได้ /etc/shadow จาก LFI หรือ RCE
- มีไฟล์ที่ password-protected (ZIP, PDF, SSH key)
- CTF crypto challenge ที่เกี่ยวกับ hash

## Installation
```bash
sudo apt install john
# JtR Jumbo (ครอบคลุมกว่า)
sudo apt install john-data
```

## Command Reference

### Basic Password Cracking
```bash
# Wordlist attack (ใช้บ่อยที่สุด)
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# Auto-detect hash format + wordlist
john --wordlist=rockyou.txt hash.txt

# Show cracked passwords
john --show hash.txt

# แสดงผลพร้อม username:password
john --show --format=<format> hash.txt
```

### ระบุ Hash Format
```bash
# ระบุ format ชัดเจน
john --format=md5crypt --wordlist=rockyou.txt hash.txt
john --format=sha512crypt --wordlist=rockyou.txt hash.txt
john --format=ntlm --wordlist=rockyou.txt hash.txt
john --format=bcrypt --wordlist=rockyou.txt hash.txt

# ดู formats ทั้งหมด
john --list=formats
john --list=formats | grep -i md5
```

### ระบุ Hash Type ที่พบบ่อย

| Hash | Format Flag | Example |
|------|------------|---------|
| MD5 | `--format=raw-md5` | `5f4dcc3b5aa765d61d8327deb882cf99` |
| SHA1 | `--format=raw-sha1` | `5baa61e4c9b93f3f0682250b6cf8331b` |
| SHA256 | `--format=raw-sha256` | |
| MD5crypt (`$1$`) | `--format=md5crypt` | `$1$salt$hash` |
| SHA512crypt (`$6$`) | `--format=sha512crypt` | `$6$salt$hash` |
| bcrypt (`$2y$`) | `--format=bcrypt` | `$2y$...` |
| NTLM | `--format=nt` | Windows NTLM hash |

### /etc/shadow Cracking
```bash
# Unshadow (รวม passwd + shadow)
unshadow /etc/passwd /etc/shadow > unshadowed.txt
john --wordlist=rockyou.txt unshadowed.txt
john --show unshadowed.txt
```

### File Password Cracking
```bash
# ZIP file
zip2john protected.zip > zip_hash.txt
john --wordlist=rockyou.txt zip_hash.txt

# PDF file
pdf2john protected.pdf > pdf_hash.txt
john --wordlist=rockyou.txt pdf_hash.txt

# SSH private key
ssh2john id_rsa > ssh_hash.txt
john --wordlist=rockyou.txt ssh_hash.txt

# RAR file
rar2john protected.rar > rar_hash.txt
john --wordlist=rockyou.txt rar_hash.txt
```

### Rules (เพิ่ม pattern)
```bash
# ใช้ rules เพื่อ mutation (เพิ่ม suffix, leetspeak, etc.)
john --wordlist=rockyou.txt --rules hash.txt
john --wordlist=rockyou.txt --rules=best64 hash.txt

# แสดง rules ทั้งหมด
john --list=rules
```

### ดูความคืบหน้า
```bash
# กด 'q' หรือ 'Q' ขณะ crack เพื่อดู status
# หรือ
john --status
```

## Identify Hash Type ก่อน Crack
```bash
# hashid (tool แยก)
hashid <hash>

# hash-identifier
hash-identifier

# John เดา format อัตโนมัติ
john hash.txt     # ลอง auto-detect
```

## Wordlists ที่แนะนำ

```
/usr/share/wordlists/rockyou.txt          → CTF standard (14M+ passwords)
/usr/share/wordlists/fasttrack.txt        → Common passwords
/usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-100000.txt
```

## What to Do After Cracking
1. บันทึก credentials ใน `workspace/active/session.md` → Findings
2. ลอง login ด้วย password ที่ crack ได้
3. ลอง password reuse บน SSH, web login, database

## Hashcat vs John
- **John**: ง่ายกว่า, auto-detect format, ดีกับ `/etc/shadow` + file formats
- **Hashcat**: เร็วกว่ามาก (GPU), ดีกว่าสำหรับ MD5/NTLM volume สูง
