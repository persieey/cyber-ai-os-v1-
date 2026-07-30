# Cyber AI OS

ระบบ AI สำหรับงาน Cybersecurity ที่รันอยู่บน Claude Code
ไม่ใช่แค่ chatbot — มันคือ OS ที่มี Departments, Roles, Skills, และ Memory

---

## ทำอะไรได้บ้าง

| งาน | Command |
|-----|---------|
| เริ่ม CTF challenge | `/ctf start <ชื่อ machine>` |
| เริ่ม Lab / Boot2Root | `/lab start <ชื่อ>` |
| Pentest engagement | `/pentest start <target>` |
| เรียน concept | `/learn <หัวข้อ>` |
| Incident Response | `/ir start` |
| Threat Hunting | `/hunt hypothesis` |
| Malware Analysis | `/malware <file>` |
| ค้นหา Knowledge Base | `/kb search <keyword>` |
| เขียน Report | `/pentest report` |
| ดู session ปัจจุบัน | `/ctx show` |

---

## Requirements

- [Claude Code](https://claude.ai/code) (CLI หรือ Desktop App)
- Python 3.x (สำหรับ tools/ scripts)
- PyYAML: `pip install pyyaml`

---

## Setup (2 ขั้นตอน)

**1. Clone แล้วเปิดใน Claude Code**

```bash
git clone <repo-url> Cyber-AI-OS
cd Cyber-AI-OS
claude  # เปิด Claude Code ใน folder นี้
```

**2. ตั้งค่า IP / Wordlists**

แก้ไฟล์ [`config/tools.yaml`](config/tools.yaml) ก่อนเริ่ม session:

```yaml
lhost: 10.10.14.x      # IP ของคุณ (จาก ip a / ifconfig tun0)
lport: 4444
wordlists:
  password: /usr/share/wordlists/rockyou.txt
  directory: /usr/share/wordlists/dirbuster/...
```

เปลี่ยน VPN ครั้งไหน แก้แค่ไฟล์นี้ — tools ทุกตัวอ่านจากนี้อัตโนมัติ

---

## โครงสร้างระบบ

```
Cyber AI OS
├── CLAUDE.md              ← Coordinator (อ่าน ROUTING_RULES → ส่งงานให้ dept ที่ถูก)
│
├── .claude/
│   ├── agents/            ← 7 Department Agents (offensive, defensive, malware, ...)
│   └── commands/          ← /ctf /lab /pentest /learn /ir /hunt /malware
│
├── department/            ← แต่ละแผนก: manifest + roles + workflows
├── skills/                ← เครื่องมือแต่ละตัว (nmap, gobuster, sqlmap, ...)
├── knowledge/             ← CTF patterns, IR playbooks, malware families
├── tools/                 ← Automation scripts (quick-scan, rev-shell, hash-crack, ...)
├── templates/             ← CTF writeup, pentest report, lab report
├── workspace/             ← Session memory (active/) + ผลลัพธ์ (outputs/)
│
├── config/
│   ├── tools.yaml         ← ตั้งค่า IP/wordlists (แก้ทุก session)
│   └── ai.yaml            ← ตั้งค่า AI behavior / department flags
│
└── tests/
    └── validate.py        ← ตรวจสอบว่าทุก path ในระบบถูกต้อง
```

---

## 7 Departments

| Department | หน้าที่ | Roles |
|-----------|---------|-------|
| **offensive-security** | CTF, Pentest, Exploit, Rev, PWN | 8 roles |
| **defensive-security** | SOC, Incident Response, Threat Hunt, Hardening | 4 roles |
| **malware-analysis** | Static/Dynamic analysis, IOC, YARA | 3 roles |
| **cloud-security** | AWS/Azure audit, Cloud Pentest | 3 roles |
| **mobile-security** | Android/iOS analysis, Mobile Pentest | 3 roles |
| **learning** | Learning path, Concept explainer | 3 roles |
| **reporting** | CTF Writeup, Pentest Report | 2 roles |

---

## Modes

ทุก Department รองรับ 4 modes — บอก AI ได้เลยว่าอยากได้แบบไหน:

| Mode | ได้อะไร |
|------|---------|
| **Hint** (default) | แนวคิด ไม่ให้คำตอบตรง |
| **Guided** | ทำด้วยกัน step by step |
| **Walkthrough** | อธิบายละเอียดทุกขั้น |
| **Full Solution** | ให้คำตอบทันที |

---

## Workflow ใน 1 Session

```
1. /ctx new ctf    → เปิด session ใหม่
2. /ctf start <machine>   → เริ่ม CTF
   (ถาม-ตอบกับ AI จน solve ได้)
3. /ctf report     → สร้าง writeup อัตโนมัติ
4. /kb add         → บันทึก pattern ลง knowledge base
```

---

## Tools ที่มี

```bash
# Recon
bash tools/recon/quick-scan.sh <ip>
bash tools/recon/subdomain-enum.sh <domain>

# CTF
bash tools/ctf/stego-check.sh <file>
python3 tools/ctf/crypto-solver.py <file>
bash tools/ctf/web-enum.sh <url>

# Exploitation
python3 tools/exploitation/rev-shell.py        # อ่าน LHOST จาก config อัตโนมัติ
bash tools/exploitation/hash-crack.sh <hash>

# Utils
python3 tools/utils/decode.py <string>
python3 tools/utils/hash-identify.py <hash>
```

---

## Validate ระบบ

ใช้หลังเพิ่ม department/role/skill ใหม่:

```bash
python3 tests/validate.py
```

ตรวจ 100+ paths ใน manifests, agents, commands — ถ้าขึ้น ✓ แปลว่า clean

---

## Version

**v1.1.0** — Cybersecurity Department Complete (7 Depts / 26 Roles / 20+ Skills)

Architecture: `Coordinator → Department Agent → Role → Skill`
