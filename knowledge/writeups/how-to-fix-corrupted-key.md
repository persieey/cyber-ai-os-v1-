# CTF Writeup Template

**CTF:** picoCTF
**Challenge:** How to fix corrupted key
**Category:** Crypto
**Difficulty:** Medium
**Points:** —
**Solved:** 2026-07-30

---

## TL;DR
`private.key` เป็น RSA private key ที่ถูก corrupt (field `d`, `q`, `dP`, `dQ`, `qInv` ถูก zero ทับทั้งหมด, `p` เหลือแค่ครึ่งบน) แต่ `n` และ `e` ยังสมบูรณ์ — ส่ง `n` ไปเช็คกับ FactorDB.com พบว่าเคยถูกแฟกทอไรซ์ไว้แล้ว ดึง `p, q` มาคำนวณ `d` ใหม่ สร้าง RSA key ที่สมบูรณ์ แล้วถอดรหัส `msg.enc` ได้ flag ตรงๆ

---

## Reconnaissance
ไฟล์ที่ให้มา: `private.key` (PEM, `RSA PRIVATE KEY`) และ `msg.enc` (128 bytes ciphertext = 1 RSA block พอดีสำหรับ modulus 1024-bit)

ลอง `RSA.import_key()` ตรงๆ จะพังทันที (`ZeroDivisionError` / `ValueError`) เพราะหลาย field ถูกเขียนทับด้วย 0

Parse โครงสร้าง ASN.1/DER ของ private key ทีละ field เพื่อดูว่า field ไหนยัง intact:

```python
import base64
from Crypto.Util.number import bytes_to_long

with open("private.key") as f:
    pem = f.read()
lines = [l.strip() for l in pem.splitlines() if l and not l.startswith("-----")]
der_bytes = base64.b64decode("".join(lines))

# n's ASN.1 TLV header (tag + long-form length) is 3 bytes at offset 7
# → content starts at offset 10, length 129 bytes → ends at 139
n_bytes = der_bytes[10:139]
n = bytes_to_long(n_bytes)
```

ผลการ parse ทุก field:

| Field | สถานะ |
|---|---|
| `n` (1024-bit modulus) | ✅ ปกติ |
| `e` (65537) | ✅ ปกติ |
| `d` | ❌ zero ทั้งหมด |
| `p` (512-bit prime) | ⚠️ รู้แค่ high 256 bits, low 256 bits ถูก zero |
| `q`, `dP`, `dQ`, `qInv` | ❌ zero ทั้งหมด |

**⚠️ ข้อควรระวัง:** offset ของ `n` ต้องนับจาก content หลัง ASN.1 header ให้ถูก (`der_bytes[10:139]`) — ถ้า slice ผิดตำแหน่ง (เช่น `der_bytes[7:264]` ที่รวม header/field อื่นเข้าไปด้วย) จะได้เลขคนละตัว ยิงไป FactorDB จะได้ status `"C"` (ยังไม่ถูกแฟกทอไรซ์) ไม่มีทาง solve ต่อได้ — ต้อง verify ว่า bit-length ของ `n` ที่ได้ตรงกับขนาด modulus จริง (1024-bit) ก่อนเสมอ

---

## Analysis
`p` ที่เหลือความรู้แค่ high bits พอดี 256/1024 = N^0.25 บิต ตรงกับ signature ของโจทย์ประเภท **partial key exposure** ที่ในทางทฤษฎีแก้ได้ด้วย Coppersmith's "factoring with high bits known" lattice attack — แต่วิธีนี้ต้องพึ่ง sage/fpylll (ไม่มีในเครื่องนี้) และช้า/ซับซ้อนกว่ามาก

ทางลัดที่เร็วกว่าและใช้ได้จริงสำหรับโจทย์ CTF สาธารณะ: **เช็ค `n` กับ FactorDB.com ก่อนเสมอ** เพราะ modulus จำนวนมากถูก submit ไว้ในฐานข้อมูลนี้แล้วจากคนที่เคย solve/brute-force มาก่อน กรณีนี้ `n` ของโจทย์นี้มี status `"FF"` (Fully Factored) พอดี เลยได้ `p, q` มาฟรีๆ โดยไม่ต้องรัน lattice attack เอง

---

## Exploitation
```python
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Util.number import inverse

def get_factors_from_factordb(n):
    res = requests.get(f"http://factordb.com/api?query={n}", timeout=10).json()
    if res.get("status") in ["FF", "F"]:
        factors = [int(f) for f, c in res.get("factors", []) for _ in range(c)]
        if len(factors) >= 2:
            return factors[0], factors[1]
    return None, None

p, q = get_factors_from_factordb(n)          # n = 1024-bit modulus จาก private.key
phi = (p - 1) * (q - 1)
d = inverse(e, phi)                          # e = 65537
fixed_key = RSA.construct((n, e, d, p, q))

with open("msg.enc", "rb") as f:
    ciphertext = f.read()

decrypted = PKCS1_v1_5.new(fixed_key).decrypt(ciphertext, sentinel=b"FAILED")
print(decrypted.decode())
```

---

## Flag
```
picoCTF{d741543f172970457e6a9aaa890935b8}
```

---

## Lessons Learned
- Diagnose corrupted RSA key ด้วยการ parse ASN.1/DER field-by-field (version, n, e, d, p, q, dP, dQ, qInv) แทนการเดา — เห็นชัดว่า field ไหน intact/zeroed
- ต้องนับ offset ของแต่ละ field จาก TLV header จริง (tag + length bytes) ไม่ใช่ hardcode ตำแหน่งมั่ว ๆ — offset ผิดแม้แค่ 3 ไบต์ ก็ได้เลขคนละตัวทันที และ verify ผลลัพธ์ด้วย bit-length เสมอ
- "รู้ high bits ของ p พอดี N^0.25" = signature ของ Coppersmith partial-key-exposure attack ในทางทฤษฎี
- **เช็ค FactorDB.com ก่อนเสมอ** ก่อนจะไปรัน local factorization/lattice attack เอง — ถ้า n เคยถูกแฟกทอไรซ์แล้ว (พบได้บ่อยกับโจทย์ CTF สาธารณะ) จะเร็วกว่ามาก
- Pattern การ rebuild+decrypt: `RSA.construct((n,e,d,p,q))` แล้วลอง `PKCS1_v1_5` (หรือ `PKCS1_OAEP`) decrypt ตามชนิด padding ที่โจทย์ใช้
