# CTF Challenge Entry Point

Arguments: $ARGUMENTS
(Expected format: `start <challenge-name> <category>` | `resume` | `report` | `solve`)

---

## Your job as Coordinator

อ่าน `workspace/active/session.md` แล้ว **spawn `offensive-security` agent** ด้วย prompt ต่อไปนี้:

```
## Request
CTF command: /ctf $ARGUMENTS

## Mode
Hint (default สำหรับ CTF — ยกระดับถ้าผู้ใช้ติดนาน)

## Date
<today's date>

## Session Context
<สรุปจาก workspace/active/session.md หรือ "No active session">

## Notes
- Challenge workspace: workspace/challenges/
- Template: templates/ctf-notes.md
- Categories supported: web | crypto | forensics | rev | pwn | osint | misc
- If action is "start": สร้าง folder + notes.md ใน workspace/challenges/pending/<category>/<name>/
- If action is "resume": อ่าน notes.md จาก challenge_dir ใน session.md
- If action is "report" หรือ "solve": finalize notes.md → ย้ายไป solved/ → สร้าง writeup → ถามก่อน push
```

Relay ผลที่ได้กลับให้ user ทันที
