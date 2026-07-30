# Workflow: Incident Response

## Phases
```
Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned
```

## Phase 1: Identification
- รับ alert จาก SIEM / user / external report
- ยืนยัน: จริงหรือ False Positive?
- ระบุ incident type:
  - Ransomware
  - Data Breach / Exfiltration
  - Unauthorized Access
  - Phishing / Malware
  - DDoS

## Phase 2: Containment
**Short-term:** หยุด spread ก่อน
- Isolate infected host (network level)
- Block attacker IP ที่ firewall
- Disable compromised account

**Long-term:** ป้องกัน reinfection
- Patch vulnerability
- Reset all credentials

## Phase 3: Eradication
- ลบ malware และ persistence (cron, registry, startup)
- Verify clean ด้วย AV + manual check

## Phase 4: Recovery
- Restore จาก verified clean backup
- Monitor อย่างใกล้ชิด 72h

## Phase 5: Lessons Learned
- Root cause analysis
- Timeline reconstruction
- Gap ที่ต้องแก้ไข (detection / prevention)
- Update playbook
