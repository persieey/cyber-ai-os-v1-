# Boot2Root Workflow

## Purpose
แนวทางทำ boot2root lab อย่างมีระบบ ตั้งแต่เริ่มจนได้ root + เขียน report

## Phases

---

### Phase 1: Recon
**Goal:** รู้ว่า target มีอะไรเปิดอยู่บ้าง

```
Skills: nmap
```

Steps:
1. Full port scan → `sudo nmap -sV -sC -p- --min-rate 5000 <IP>`
2. บันทึก open ports ทั้งหมดใน session.md → Findings
3. ระบุ attack surface เบื้องต้น (web? ssh? smb? ftp?)

Done when: รู้ทุก port และ service version

---

### Phase 2: Enumeration
**Goal:** หาข้อมูลลึกขึ้นจาก service ที่เปิดอยู่

Checklist ตาม service:

**Web (80/443/8080)**
- [ ] Browse manually, ดู source code
- [ ] `gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt`
- [ ] `nikto -h http://<IP>`
- [ ] เช็ค robots.txt, sitemap.xml

**SMB (445/139)**
- [ ] `enum4linux -a <IP>`
- [ ] `smbclient -L //<IP>/ -N`
- [ ] เช็ค anonymous share access

**FTP (21)**
- [ ] ลอง anonymous login: `ftp <IP>` → user: anonymous
- [ ] list files ถ้าเข้าได้

**SSH (22)**
- [ ] จด version ไว้ เช็ค CVE ถ้า version เก่า
- [ ] ยังไม่ต้อง brute force ในขั้นนี้

Done when: มี potential vulnerability หรือ entry point อย่างน้อย 1 ตัว

---

### Phase 3: Exploitation
**Goal:** เข้าถึง target ได้ (user shell)

Steps:
1. เลือก vulnerability ที่น่าจะ work จาก enum
2. หา exploit: `searchsploit <service> <version>`
3. ทดสอบ exploit (เริ่มจาก low-impact ก่อน)
4. ได้ shell → ยืนยัน `whoami`, `id`, `hostname`
5. บันทึก exploit ที่ใช้ได้ใน session.md → Findings

Done when: มี shell บน target

---

### Phase 4: Post-Exploitation / Privilege Escalation
**Goal:** ยกระดับจาก user → root

Checklist:
- [ ] `sudo -l` — ทำ sudo ได้ command ไหนบ้าง
- [ ] `find / -perm -4000 2>/dev/null` — SUID binaries
- [ ] `cat /etc/crontab` — cron jobs
- [ ] `uname -a` — kernel version (เช็ค kernel exploit)
- [ ] `cat /etc/passwd` — users ที่มีในระบบ
- [ ] เช็ค writable directories/files

Done when: `whoami` = root (หรือ NT AUTHORITY\SYSTEM บน Windows)

---

### Phase 5: Loot & Report
**Goal:** เก็บ proof + เขียน report

Steps:
1. Screenshot หรือ copy `proof.txt` / `root.txt` / `flag`
2. `cat /root/proof.txt` หรือ `cat /root/root.txt`
3. บันทึกใน session.md → Notes
4. รัน `/report` เพื่อ generate lab report อัตโนมัติ
5. ย้าย session ไป archive: `/ctx done`

---

## Quick Reference Card

```
Phase 1  nmap -sV -sC -p- --min-rate 5000 <IP>
Phase 2  gobuster / enum4linux / nikto ตาม service
Phase 3  searchsploit → exploit
Phase 4  sudo -l / SUID / cron / kernel
Phase 5  proof.txt → /report → /ctx done
```
