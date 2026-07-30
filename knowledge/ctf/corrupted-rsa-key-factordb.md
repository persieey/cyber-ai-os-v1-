# Pattern: Corrupted RSA Private Key → FactorDB Shortcut

**Source:** How to fix corrupted key — picoCTF | 2026-07-30
**Category:** Crypto | RSA
**Difficulty:** Medium

## Summary

โจทย์ให้ PEM `RSA PRIVATE KEY` ที่ field บางตัวถูก zero ทับ (corrupt) จน `RSA.import_key()` พังทันที
ให้ diagnose ด้วยการ parse ASN.1/DER field-by-field ก่อนเสมอ แทนที่จะเดาว่าพังตรงไหน
แล้วเช็ค modulus `n` กับ FactorDB.com ก่อนไปรัน local factorization/lattice attack เอง

## Trigger Signs

- ไฟล์ `.key` / `.pem` ที่ error ทันทีตอน `RSA.import_key()` (`ZeroDivisionError`, `ValueError`)
- Challenge name/hint พูดถึง "corrupted", "broken", "fix the key"
- ให้ private key + ciphertext มาคู่กัน (ไม่ใช่ public key ธรรมดา)

## Diagnose (ASN.1/DER field-by-field)

PKCS#1 `RSA PRIVATE KEY` DER structure = `SEQUENCE` ของ 9 INTEGER field ตามลำดับ:
`version, n, e, d, p, q, dP, dQ, qInv`

```python
import base64

with open("private.key") as f:
    pem = f.read()
lines = [l.strip() for l in pem.splitlines() if l and not l.startswith("-----")]
der = base64.b64decode("".join(lines))

def parse_tlv(data, offset):
    tag = data[offset]
    length_byte = data[offset + 1]
    if length_byte & 0x80:
        num_len_bytes = length_byte & 0x7F
        length = int.from_bytes(data[offset + 2:offset + 2 + num_len_bytes], "big")
        header_len = 2 + num_len_bytes
    else:
        length = length_byte
        header_len = 2
    content = data[offset + header_len:offset + header_len + length]
    return content, offset + header_len + length

hl = 2 + (der[1] & 0x7F) if der[1] & 0x80 else 2
off = hl
for name in ["version", "n", "e", "d", "p", "q", "dP", "dQ", "qInv"]:
    content, off = parse_tlv(der, off)
    nz = [i for i, b in enumerate(content) if b != 0]
    print(name, "len=", len(content), "all_zero=" if not nz else "known_prefix_bytes=", (nz[-1]+1 if nz else 0))
```

ดูว่า field ไหน `all_zero` (corrupt เต็ม) vs field ไหนยังมีบาง byte ที่ไม่ใช่ 0 (corrupt บางส่วน — อาจเป็น partial key exposure / Coppersmith case)

**⚠️ ระวัง offset:** ต้องนับ content หลัง TLV header (tag+length bytes) ให้ถูก ห้าม hardcode ตำแหน่งแบบเดา — offset ผิดแม้ 2-3 ไบต์ ได้เลขคนละตัวทันที ให้ verify ด้วย `bit_length()` ว่าตรงกับขนาด modulus จริงเสมอ (เช่น RSA-1024 ต้องได้ 1024, ไม่ใช่ 2050)

## Attack

```
1. ถ้า n, e ยัง intact → เอา n ไปเช็ค FactorDB.com ก่อนเสมอ (เร็วที่สุด)
   GET http://factordb.com/api?query=<n>
   status "FF"/"F" = fully factored → ได้ p, q ฟรี

2. ถ้า FactorDB ไม่มี (status "C" หรือ "N") → ค่อยพิจารณาวิธีอื่นตามลักษณะ corruption:
   - p/q ใกล้กัน → Fermat's factorization
   - รู้ high bits ของ p พอดี ~N^0.25 ของ N → Coppersmith "factoring with known high bits" (ต้อง sage/fpylll)
   - e เล็ก (e=3) + ไม่มี padding → e-th root attack

3. เมื่อได้ p, q แล้ว:
   phi = (p-1)*(q-1)
   d = inverse(e, phi)
   key = RSA.construct((n, e, d, p, q))

4. ถอดรหัส ciphertext ด้วย PKCS1_v1_5 หรือ PKCS1_OAEP (ลองทั้งคู่ตาม padding ที่โจทย์ใช้)
```

## Related
- [crypto-patterns.md](crypto-patterns.md) — RSA quick reference ทั่วไป
- [how-to-fix-corrupted-key.md writeup](../writeups/how-to-fix-corrupted-key.md) — full solve เคสจริง
