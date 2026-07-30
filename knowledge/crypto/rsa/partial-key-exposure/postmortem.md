# Postmortem: How to fix corrupted key (round 2)

## Challenge
**ชื่อ:** corrupt-key-2 / "How to fix corrupted key (round 2)" — picoMini
**Category:** Crypto
**Difficulty:** Hard
**Solved:** 2026-07-30

## Goal
Decrypt `msg2.enc` จาก RSA private key ที่ `d, q, dP, dQ, qInv` เป็น zero ทั้งหมด และ `p` มี zero-byte gaps ซ่อนอยู่

## What Worked

- **Scan full byte array for zero-runs** — เมื่อเปลี่ยนจาก boundary-check เป็น full-scan พบ 3 gaps: 5+4+5 bytes (112 bits) ที่ shift 352, 240, 16
- **Multivariate Coppersmith** ด้วย TheBlupper/coppersmith — สร้าง polynomial 3 unknowns, `small_roots([f], sizes, lat_reduce=LLL)`
- **WSL2 + conda-forge SageMath** — รันได้ 225s โดยไม่มี time limit
- **patch `msolve_available = False`** — แก้ crash จาก `FeatureNotPresentError`
- **`.sage` extension** — ทำให้ Sage preparser ทำงาน (`Zmod`, `^`, etc.)
- ค้นหา public writeup ก่อน — Connor McCartney และ CyLab Medium writeup ยืนยัน bit-shift และ bounds ตรงกัน

## What Failed

1. **Boundary-only zero check บน `p`** — ดูแค่ first/last bytes บอกว่า p ดูปกติ → สรุปผิดว่าเป็น decoy
2. **`sagecell.sagemath.org`** — kernel ถูก kill ~15-20s เข้า Gröbner-basis step ทุกครั้ง แม้ reconnect 50+ ครั้ง
3. **`sudo apt install sagemath` บน Ubuntu 25.04** — package ไม่มีใน apt repos ของ Ubuntu Resolute
4. **รัน `.sage` script ด้วย extension `.py`** — `NameError: Zmod` เพราะ preparser ไม่ทำงาน
5. **ปล่อย `msolve_available` เป็น auto-detect** — probe crash ด้วย `FeatureNotPresentError` แทนที่จะ fallback gracefully

## Root Cause

**Primary:** ไม่ทำ full zero-run scan บน `p` ตั้งแต่แรก → ใช้เวลานานกว่าจำเป็นในการ identify attack vector

**Secondary:** พยายามใช้ sagecell สำหรับ computation ที่หนักกว่า free tier limit → เสียเวลา 50+ reconnect ก่อนจะ confirm ว่าไม่ใช่ network issue แต่เป็น server-side resource limit

## Lessons Learned

1. **Zero-run scan ต้อง full byte array เสมอ** — boundary check ไม่พอ; ทำ `if p_bytes[i] == 0` scan ทุก byte
2. **`gcd(p_partial, n) == 1` + not prime ≠ decoy** — อาจเป็น multi-gap corruption; ตรวจ zero-runs ก่อนสรุป
3. **sagecell = light checks only** — ไม่เหมาะสำหรับ Coppersmith/Gröbner ที่ใช้เวลา >15s; ใช้ WSL2 + local sage
4. **TheBlupper/coppersmith ต้อง patch msolve** — `msolve_available = False` ถ้า msolve ไม่ install
5. **Extension `.sage` ไม่ใช่ `.py`** — preparser requirement เป็น hard requirement
6. **ค้นหา public writeup ก่อน** สำหรับ named/archived CTF — บ่อยครั้งมีแล้ว

## Workflow Changes

- เพิ่ม "full zero-run scan" เป็น step แรกใน RSA partial key exposure workflow
- เพิ่มคำเตือน sagecell limit ใน cryptography.md workflow
- แยก univariate vs multivariate decision tree ชัดเจน

## Skill Updates

- `knowledge/crypto/rsa/partial-key-exposure/workflow.md` → maturity: **validated**
- `knowledge/ctf/multivariate-coppersmith-corrupted-p.md` — pattern ใหม่

## References

- TheBlupper/coppersmith: https://github.com/TheBlupper/coppersmith
- Connor McCartney writeup: https://connor-mccartney.github.io/cryptography/small-roots/corrupt-key-2-picoMini
- CyLab Medium writeup: https://medium.com/@jenishb2006/cylab-corrupt-key-2-writeup-rsa-private-key-recovery-using-multivariate-coppersmiths-method-051e1d9567e3
