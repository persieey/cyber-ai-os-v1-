# Prompt Standard

Rules สำหรับเขียน agent prompts และ command files

## Department Agent (`/.claude/agents/<dept>.md`)

### Frontmatter
```yaml
---
name: <dept-name>
description: <1 sentence — triggers when this agent is relevant>
model: claude-sonnet-5
tools:
  - Read
  - Write    # ถ้าต้องสร้างไฟล์
  - Edit
  - Bash     # ถ้า dept ต้องรัน command
  - Glob
  - Grep
---
```

### Body Structure
```
# <Dept Name> Department Agent v2

## Startup
1. อ่าน manifest
2. วิเคราะห์ task → เลือก role

## Role Selection
[table: task → full path ของ role file]

## Response Format
**[<Dept>] [Role: <role>] [Phase: <phase>]**

## ภาษา
ภาษาไทย narration, English technical terms
```

### Rules
- description ต้อง specific — Claude ใช้ตัดสินว่าจะ spawn agent ไหน
- Role table ต้องใช้ **full path** จาก project root (ไม่ใช่ relative)
- ถ้าไม่แน่ใจ → ถาม 1 คำถาม ไม่เดา

## Command File (`/.claude/commands/<cmd>.md`)

### Structure
```markdown
# <Command Name>

Read these files in order:
1. `workspace/active/session.md`
2. `department/<dept>/workflows/<workflow>.md`
3. `department/<dept>/roles/<role>.md`

Arguments: $ARGUMENTS
(Expected: `<action> <args>` | `resume` | `report`)

---

## If action is "<action>"
[steps]

## If action is "resume"
[steps]

## If action is "report"
[steps]

Start response with:
**[<Label>] [<field>: <value>] ...**
```

### Rules
- ทุก command ต้องรองรับ `resume` และ `report` actions
- Response header format ต้องสอดคล้องกับ department agent format
- อ่าน session.md เสมอเป็นขั้นแรก
