# Lab Session — Boot2Root Entry Point

Arguments: $ARGUMENTS
(Expected format: `start <IP> <lab-name>` | `resume` | `report`)

---

## Your job as Coordinator

อ่าน `workspace/active/session.md` แล้ว **spawn `offensive-security` agent** ด้วย prompt ต่อไปนี้:

```
## Request
Lab command: /lab $ARGUMENTS

## Mode
Hint (default สำหรับ Lab — ยกระดับถ้าผู้ใช้ติดนาน)

## Date
<today's date>

## Session Context
<สรุปจาก workspace/active/session.md หรือ "No active session">

## Notes
- Workflow: department/offensive-security/workflows/boot2root.md
- If action is "start <IP> <lab-name>": สร้าง session.md (type: Lab, target_ip, phase: Recon)
  แล้วเริ่ม Phase 1 Recon — ให้ nmap command แก่ user รอ output
- If action is "resume": อ่าน session.md → สรุปความคืบหน้า → ทำต่อจาก phase ปัจจุบัน
- If action is "report": อ่าน session.md → ใช้ templates/lab-report.md → ถามก่อน save
```

Relay ผลที่ได้กลับให้ user ทันที
