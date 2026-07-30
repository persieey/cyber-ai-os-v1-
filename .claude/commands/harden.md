# Security Hardening Entry Point

Arguments: $ARGUMENTS
(Expected: `linux` | `windows` | `web <server>` | `network` | `cloud <provider>`)

---

## Your job as Coordinator

ตรวจ argument ก่อน:
- ถ้า argument มีคำว่า `cloud` → **spawn `cloud-security` agent**
- อื่นๆ ทั้งหมด → **spawn `defensive-security` agent**

Spawn ด้วย prompt ต่อไปนี้:

```
## Request
Hardening command: /harden $ARGUMENTS

## Mode
Walkthrough (default สำหรับ hardening)

## Date
<today's date>

## Session Context
No active session required for hardening

## Notes
- Role: hardening-specialist
- Targets: linux | windows | web (nginx/apache/iis) | network | cloud (aws/azure/gcp)
- Output format:
  ## [Target] Hardening Report
  ### Critical (แก้ทันที) — [ ] item: ปัญหา → วิธีแก้
  ### High — [ ] ...
  ### Passed ✅ — [x] ...
- cloud target → ใช้ CIS Benchmark + run audit checks ตาม provider
```

Relay ผลที่ได้กลับให้ user ทันที
