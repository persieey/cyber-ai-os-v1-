# Session Schema

ทุก session.md ต้องมีโครงสร้างนี้:

```markdown
# Active Session

## Task
- type: [CTF / Lab / Learning / Pentest]
- name: ชื่อ challenge หรืองาน
- department: [offensive-security / learning / reporting]
- mode: [Hint / Guided / Walkthrough / Full Solution / Adaptive]

## Progress
- phase: [Recon / Enum / Exploit / Post-Exploit / Reporting / Done]
- started: YYYY-MM-DD

## Done
- รายการที่ทำเสร็จแล้ว (bullet list)

## Findings
- สิ่งที่ค้นพบ เช่น open ports, endpoints, vulnerabilities

## Pending
- ขั้นตอนถัดไปที่ยังไม่ได้ทำ

## Notes
- อะไรก็ตามที่ควรจำ เช่น payload ที่ลองแล้ว, ที่ติด
```

## Rules
- ถ้าไม่มี session.md → AI ถามว่างานใหม่หรือต่อจากเดิม
- ถ้ามี session.md → AI อ่านก่อนตอบทุกครั้ง
- หลังแต่ละ step → AI อัปเดต Done, Findings, Pending ให้ล่าสุด
