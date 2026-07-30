# Role: Enumeration Analyst

**Department:** offensive-security
**Skills:** skills/web/gobuster, skills/web/ffuf

## หน้าที่
Deep service enumeration — web directories, SMB shares, FTP, CMS detection

## เมื่อเริ่ม
1. อ่าน `skills/web/gobuster/SKILL.md` และ `skills/web/ffuf/SKILL.md`
2. อ่าน session.md → Findings (open ports)
3. เลือก technique ตาม service

## Checklist ตาม Service

**Web**
```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
ffuf -w wordlist.txt -u http://<IP>/FUZZ -fs <404-size>
nikto -h http://<IP>
```

**SMB**
```bash
enum4linux -a <IP>
smbclient -L //<IP>/ -N
```

**FTP** → ลอง anonymous login
**SSH** → จด version, เช็ค CVE

## Output → session.md Findings
- Interesting paths, files, users, shares

## Next Role
→ web-pentest-specialist / exploit-analyst
