# Threat Hunting Entry Point

Arguments: $ARGUMENTS
(Expected: `start <hypothesis>` | `ioc <indicator>` | `mitre <technique-id>` | `resume` | `report`)

---

## Your job as Coordinator

อ่าน `workspace/active/session.md` แล้ว **spawn `defensive-security` agent** ด้วย prompt ต่อไปนี้:

```
## Request
Threat hunt command: /hunt $ARGUMENTS

## Mode
Walkthrough (default สำหรับ threat hunting)

## Date
<today's date>

## Session Context
<สรุปจาก workspace/active/session.md หรือ "No active session">

## Notes
- Role: threat-hunter
- Workflow: department/defensive-security/workflows/threat-hunting.md
- If action is "start <hypothesis>": สร้าง session.md (type: Threat Hunt, hypothesis, phase: Data Collection)
  ระบุ data sources ที่ต้องการ → ให้ initial queries (Splunk/KQL/zeek-cut)
- If action is "ioc <indicator>": ระบุ IOC type → generate search queries สำหรับ Splunk/ELK/Zeek/WEL
- If action is "mitre <technique-id>": อธิบาย artifacts ที่ technique นี้ทิ้งไว้ → hunting queries
- If action is "resume": อ่าน session.md → ทำต่อจาก phase ปัจจุบัน
- If action is "report": สร้าง Hunt Report (Hypothesis | Data Sources | Queries | Findings | Verdict | New Detections)
```

Relay ผลที่ได้กลับให้ user ทันที
