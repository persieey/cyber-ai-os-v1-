# Threat Hunting Hypotheses

## Collection ของ Hypothesis ที่ดี

### Network-based
- "มี host กำลัง beacon ไป C2 ทุก X นาที"
  → Hunt: conn.log, เช็ค periodic connections ไป non-standard IP
- "มี DNS tunneling ใน environment"
  → Hunt: dns.log, หา query ที่ยาวผิดปกติ (> 50 chars)
- "มี data exfil ผ่าน HTTPS ไป cloud storage ที่ไม่ได้ approve"
  → Hunt: proxy log, dest domain ≠ whitelist, bytes_out สูง

### Endpoint-based
- "มี LOLBin ถูกใช้เพื่อ execute payload"
  → Hunt: process creation, parent = Office/browser, child = certutil/mshta/wscript
- "มี credential dumping เกิดขึ้น"
  → Hunt: EventCode 4656 (lsass handle), Sysmon 10 (lsass access)
- "มี new service ถูก install หลัง business hours"
  → Hunt: EventCode 7045, time = นอกเวลาทำงาน

### Identity-based
- "มี account login จาก location ใหม่ที่ผิดปกติ"
  → Hunt: auth logs, country ≠ usual
- "มี service account ถูกใช้แบบ interactive login"
  → Hunt: EventCode 4624 LogonType=2 จาก svc_ account
- "มี admin account ถูกสร้างใหม่"
  → Hunt: EventCode 4720 + 4732 (added to admin group)

## MITRE ATT&CK Quick Reference
| Technique | ID | Hunt Signal |
|-----------|-----|------------|
| Spearphishing | T1566 | email with attachment + click + child process |
| PowerShell | T1059.001 | powershell.exe -enc / -nop |
| Scheduled Task | T1053 | schtasks.exe + new XML file |
| LSASS Dump | T1003.001 | sekurlsa / comsvcs.dll / procdump -ma lsass |
| Pass-the-Hash | T1550.002 | EventCode 4624 LogonType=9 |
| Kerberoasting | T1558.003 | EventCode 4769 EncryptionType=0x17 |
