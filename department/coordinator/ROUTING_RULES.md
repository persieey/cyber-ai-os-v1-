# Routing Rules

## Department Agents (v2 — active)

| Task | Department Agent |
|------|-----------------|
| CTF / Lab / Pentest / Exploit / PrivEsc / Rev | `offensive-security` |
| Learning / Concept / สอน / อธิบาย | `learning` |
| Report / Writeup / Documentation | `reporting` |
| Unknown | ถาม 1 คำถาม |

## วิธี Route

1. ส่ง task ไปยัง **Department Agent** (ใน `.claude/agents/<dept>.md`)
2. Department Agent อ่าน manifest → เลือก Role → ดำเนินการ
3. Coordinator ไม่ route ตรงไปยัง Role หรือ Skill

## Legacy Agents (deprecated — Sprint 11)

agents เดิมใน `.claude/agents/` ที่ชื่อ: recon, enumeration, web-pentest,
linux-privesc, windows-ad, reverse-engineering, report, lab-manager ฯลฯ
→ **status: legacy** — ยังใช้งานได้แต่จะถูกลบเมื่อ migration ครบทุก dept

## Priority
1. user ระบุ department ตรงๆ → route ตามนั้น
2. ไม่ระบุ → TASK_CLASSIFIER → routing table ด้านบน
3. classify ไม่ได้ → ถาม 1 คำถาม
