# Workflow Standard

Template และ rules สำหรับสร้าง workflow file ใหม่

## Location
```
department/<dept-name>/workflows/<workflow-id>.md
```

## Template
```markdown
# Workflow: <Workflow Name>

## Process
```
Phase 1 → Phase 2 → Phase 3 → Output
```

## Phase 1: <Name>
[อธิบาย goal ของ phase นี้]

### Steps
1. [step]
2. [step]

### Output
- [สิ่งที่ได้จาก phase นี้]

## Phase 2: <Name>
...

## Phase N: Report / Output
- [deliverable สุดท้าย]
- บันทึกที่: `workspace/outputs/<name>.md`
```

## Rules
- ชื่อไฟล์: `kebab-case.md` เช่น `boot2root.md`
- เริ่มด้วย Process diagram (ASCII)
- แต่ละ phase มี goal ชัดเจน
- ระบุ role ที่รับผิดชอบแต่ละ phase (ถ้า multi-role)
- ระบุ output ของแต่ละ phase
- Phase สุดท้ายต้องชี้ไปยัง output location
