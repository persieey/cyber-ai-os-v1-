# Incident Response Entry Point

Arguments: $ARGUMENTS
(Expected: `start <incident-type> <hostname>` | `resume` | `report`)

---

## Your job as Coordinator

อ่าน `workspace/active/session.md` แล้ว **spawn `defensive-security` agent** ด้วย prompt ต่อไปนี้:

```
## Request
IR command: /ir $ARGUMENTS

## Mode
Walkthrough (default สำหรับ IR)

## Date
<today's date>

## Session Context
<สรุปจาก workspace/active/session.md หรือ "No active session">

## Notes
- Role: incident-responder
- Workflow: department/defensive-security/workflows/incident-response.md
- Incident types: ransomware | breach | intrusion | phishing | malware | ddos
- If action is "start <type> <hostname>": สร้าง session.md (type: IR, incident_type, hostname, phase: Identification)
  เริ่ม Phase 1: Identification → ถาม user หา alerts/logs/screenshots เพิ่มเติม
- If action is "resume": อ่าน session.md → สรุปความคืบหน้า → ทำต่อ
- If action is "report": สร้าง IR report (Timeline | Root Cause | Impact | Remediation | Lessons) → ถามก่อน save
```

Relay ผลที่ได้กลับให้ user ทันที
