# Context Engine

## Purpose
ทำให้ AI รู้บริบทงานปัจจุบันจริงๆ แทนการเดาหรือแต่งขึ้นมาเอง

## How It Works
ทุก session ที่เริ่มงานใหม่จะสร้าง/อัปเดตไฟล์ `workspace/active/session.md`
Commands ทุกตัว (pentest, learn, cyber) อ่านไฟล์นี้ก่อนตอบเสมอ

## Session Lifecycle

```
/ctx new    → สร้าง session ใหม่
/pentest    → อ่าน session → ทำงาน → อัปเดต session
/ctx show   → แสดง session ปัจจุบัน
/ctx clear  → ล้าง session
```

## Files
- `src/context-engine/SCHEMA.md` — โครงสร้างของ session file
- `workspace/active/session.md`  — session ที่กำลังทำงานอยู่
