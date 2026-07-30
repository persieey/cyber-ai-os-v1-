# Learning Department — Direct Entry

Arguments: $ARGUMENTS
(Topic to learn / question to ask)

---

## Your job as Coordinator

**spawn `learning` agent** ด้วย prompt ต่อไปนี้:

```
## Request
Learning request: $ARGUMENTS

## Mode
Guided (new topic) หรือ Adaptive ถ้าผู้ใช้แสดงความรู้เดิมในการถาม

## Date
<today's date>

## Session Context
No active session required

## Notes
- ประเมิน prior knowledge จากวิธีที่ผู้ใช้ถาม (technical vs general)
- เลือก role: learning-coach (roadmap) / concept-explainer (อธิบาย) / knowledge-builder (บันทึก)
- จบด้วย 1 check question เพื่อตรวจความเข้าใจ
```

Relay ผลที่ได้กลับให้ user ทันที
