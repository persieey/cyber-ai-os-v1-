# Skill: Nmap

## Purpose
Network reconnaissance — ค้นหา open ports, services, versions, และ OS ของ target

## When to Use
- Phase: Recon หรือ Enumeration
- ต้องการรู้ว่า target เปิด port อะไรบ้าง
- ต้องการรู้ service และ version ที่รันอยู่

## Command Reference

### Basic scan (top 1000 ports)
```bash
nmap <target>
```

### Full port scan
```bash
nmap -p- <target>
```

### Service + version detection
```bash
nmap -sV <target>
```

### OS detection (ต้องใช้ sudo)
```bash
sudo nmap -O <target>
```

### Aggressive scan (OS + version + script + traceroute)
```bash
sudo nmap -A <target>
```

### Common CTF/Lab combo
```bash
sudo nmap -sV -sC -p- --min-rate 5000 <target>
```
- `-sV` — version detection
- `-sC` — default scripts
- `-p-` — all 65535 ports
- `--min-rate 5000` — เร็วขึ้น (ใช้ใน lab เท่านั้น ไม่ใช้ production)

### UDP scan (ช้า ใช้เมื่อจำเป็น)
```bash
sudo nmap -sU --top-ports 20 <target>
```

## Output Interpretation

| State    | ความหมาย                            |
|----------|--------------------------------------|
| open     | port เปิด มี service รันอยู่         |
| closed   | port ปิด แต่ host ตอบสนอง           |
| filtered | firewall บล็อก ไม่รู้สถานะจริง       |

## What to Look For
- Port 80/443 → Web application → ต่อด้วย web enum
- Port 22 → SSH → เช็ค version, ลอง creds ถ้ามี
- Port 21 → FTP → เช็ค anonymous login
- Port 445/139 → SMB → enum shares, เช็ค vulns
- Port 3306 → MySQL → เช็ค auth
- Port ที่ไม่คุ้นเคย → google "port XXXX exploit" หรือ searchsploit

## Next Steps After Nmap
- Web ports → gobuster / nikto / manual browse
- SMB → enum4linux / smbclient
- Unknown service → nc -nv <target> <port> (banner grab)
