# Git Standard

Commit message format และ branching rules

## Commit Message Format
```
<type>(<scope>): <summary>

[body — ถ้าจำเป็น]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

## Types
| Type | ใช้เมื่อ |
|------|---------|
| `feat` | เพิ่ม feature ใหม่ (dept, role, skill, command) |
| `fix` | แก้ bug หรือ broken reference |
| `refactor` | ปรับโครงสร้างโดยไม่เปลี่ยน behavior |
| `docs` | แก้ documentation เท่านั้น |
| `chore` | cleanup, rename, delete unused files |
| `sprint` | milestone commit ครอบคลุมหลาย changes |

## Scope ตัวอย่าง
```
feat(offensive-security): add linux-privesc-specialist role
fix(routing): update paths in learning agent role table
chore(skills): remove old flat skill folders
sprint(15): cybersecurity department complete
```

## Rules
- Summary: imperative mood, lowercase, ไม่มี period
- Body: อธิบาย **why** ไม่ใช่ **what**
- Snapshot commit ก่อนทุก sprint ใหม่: `chore: snapshot pre-sprint-N`
- ไม่ force push ไป main
- ไม่ skip hooks (--no-verify)
