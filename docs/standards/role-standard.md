# Role Standard

Template และ rules สำหรับสร้าง role file ใหม่

## Location
```
department/<dept-name>/roles/<role-id>.md
```

## Template
```markdown
# Role: <Role Name>

**Department:** <dept-name>
**Phase:** <recon|enumeration|exploitation|post-exploitation|analysis|audit|response|reporting>
**Skills:** skills/<category>/<tool> [, skills/<category>/<tool>]
**Workflow:** department/<dept>/workflows/<workflow>.md  [ถ้ามี]

## หน้าที่
[1-2 ประโยค อธิบายว่า role นี้ทำอะไร]

## เมื่อเริ่ม
1. อ่าน `skills/<category>/<tool>/SKILL.md`  [ถ้ามี]
2. อ่าน `workspace/active/session.md` → รู้ context ปัจจุบัน
3. [ขั้นตอนเริ่มต้น]

## [Section หลัก — checklist หรือ workflow]
[commands, steps, decision tables]

## Output → session.md
- [สิ่งที่ต้องบันทึกลง session.md หลังทำเสร็จ]

## Next Role  [ถ้ามี]
→ <next-role-id>
```

## Rules
- ชื่อไฟล์: `kebab-case.md` เช่น `recon-analyst.md`
- Phase ต้องตรงกับที่ระบุใน `manifest.yaml`
- Skills path ต้องเป็น full path จาก project root
- ทุก role ต้องมี **Output → session.md** section
- ภาษาไทย narration, English technical terms
- ไม่เขียน comment อธิบาย what — เขียนเฉพาะ why ถ้าจำเป็น
