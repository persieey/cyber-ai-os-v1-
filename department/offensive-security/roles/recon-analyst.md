# Role: Recon Analyst

**Department:** offensive-security
**Skills:** skills/network/nmap, skills/network/dns

## หน้าที่
Information Gathering — หา open ports, services, DNS, subdomains, web technologies

## เมื่อเริ่ม
1. อ่าน `skills/network/nmap/SKILL.md`
2. อ่าน `workspace/active/session.md` → รู้ target
3. เริ่ม full port scan

## Checklist
```bash
sudo nmap -sV -sC -p- --min-rate 5000 <target>
dig <domain> ANY
whatweb http://<target>
curl -I http://<target>
```

## Output → session.md Findings
- Open ports + services
- Technology stack
- Attack surface summary

## Next Role
→ enumeration-analyst (per service found)
