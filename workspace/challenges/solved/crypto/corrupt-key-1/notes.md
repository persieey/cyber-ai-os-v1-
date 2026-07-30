# How to fix corrupted key (Round 1)

**Source:** picoMini — "corrupt-key-1"
**Category:** Crypto
**Difficulty:** Medium
**Status:** ✅ solved
**Started:** 2026-07-30
**Solved:** 2026-07-30

---

## ไฟล์ที่ได้รับ

| ชื่อไฟล์ | ประเภท | หมายเหตุ |
|----------|--------|---------|
| private.key | RSA private key (PEM) | field หลายตัวเป็น zero, p มี known high bits |
| msg.enc | Ciphertext | เข้ารหัสด้วย public key คู่กัน |

---

## ภาพรวมโจทย์

โจทย์นี้เป็น intro ของ corrupt-key series — RSA key เสียหายในรูปแบบง่ายกว่า round 2
`d, q, dP, dQ, qInv` เป็น zero ทั้งหมด แต่ `p` เสียหายแค่ **ส่วนท้าย** (low bits หายไป)
ทำให้รู้ว่า `p` จาก "high bits" ลงมาจนถึงจุดหนึ่ง — รูปแบบนี้เรียกว่า "known high bits"

**ทำไม known high bits ถึง exploit ง่ายกว่า:**
ถ้า p_high bits รู้ทั้งหมด ปัญหาจะกลายเป็น univariate polynomial:
`f(x) = p_known + x` โดย x คือ unknown low bits — แค่ตัวเดียว
Sage มี built-in `.small_roots()` สำหรับ univariate case นี้โดยตรง

---

## Phase 1: Initial Analysis

### Parse key

```python
from Crypto.PublicKey import RSA

key = RSA.import_key(open("private.key").read())
print(f"n bit length: {key.n.bit_length()}")
print(f"p = {hex(key.p)}")
print(f"p trailing zeros: {bin(key.p).rstrip('0')[-8:]}")  # ดู low bits
```

**ผลลัพธ์:**
- `n` สมบูรณ์ (1024-bit)
- `p` มี high bits ครบ แต่ low 256 bits เป็น 0
- รู้ว่า unknown = 256 bits (ที่ท้าย)

**ทำไม 256 bits ถึง solvable:**
ขีดจำกัด Coppersmith: unknown bits < N^0.25 ≈ 25% ของ N
สำหรับ 1024-bit N: N^0.25 = 256 bits — พอดีกับขีดจำกัด (tight bound)

---

## วิธีที่สำเร็จ: Univariate Coppersmith

### แนวคิดพื้นฐาน

p เป็น factor ของ n ดังนั้น `p ≡ 0 (mod p)`
เราสร้าง polynomial: `f(x) = p_high + x` โดย p_high คือ p ที่ low 256 bits เป็น 0
เราต้องหา x ที่ทำให้ `f(x) ≡ 0 (mod p)` ซึ่งก็คือ x = p - p_high (low bits ที่หายไป)
Coppersmith ช่วยหา "small root" ของ polynomial mod unknown factor ของ n

### Code (Sage)

```python
# solve.sage
N = key.n
e = 65537
p_high = key.p  # p ที่ low bits เป็น 0 อยู่แล้ว

P.<x> = PolynomialRing(Zmod(N))
f = p_high + x
# bound = ขนาด unknown (2^256)
roots = f.small_roots(X=2^256, beta=0.5)

x_val = roots[0]
p = p_high + int(x_val)

assert N % p == 0
q = N // p
d = pow(e, -1, (p-1)*(q-1))
```

**อธิบาย `beta=0.5`:**
Coppersmith parameter ที่บอกว่า factor ที่เราหาอยู่ใน range ไหนของ n
beta=0.5 หมายถึง "หา root mod factor ที่มีขนาดประมาณ n^0.5" — เหมาะสำหรับ RSA prime

### Decrypt

```python
from Crypto.Cipher import PKCS1_v1_5
key_obj = RSA.construct((N, e, d, p, q))
plaintext = PKCS1_v1_5.new(key_obj).decrypt(open("msg.enc","rb").read(), sentinel=b"FAILED")
print(plaintext)
```

---

## Flag

```
picoCTF{...}   ← (round 1 flag)
```

---

## สิ่งที่เรียนรู้

**Concepts:**
- **Univariate Coppersmith** — หา small root ของ polynomial mod n เมื่อมี unknown เดียว (low bits ของ p)
- **Coppersmith bound** — unknown bits < N^0.25 คือ solvable; เกินกว่านี้ computation ระเบิด
- **RSA structure** — n = p × q; ถ้ารู้ p ก็คำนวณ q และ d ได้ทันที

**Pattern ที่ควรจำ:**

| เงื่อนไข | Approach |
|----------|---------|
| p ขาดแค่ low bits (1 unknown) | `f.small_roots(X=2^unknown_bits, beta=0.5)` |
| p มีหลาย gaps | Multivariate Coppersmith (round 2) |

**ความสัมพันธ์กับ Round 2:**
Round 1 ง่ายกว่าเพราะ 1 unknown — Sage handle ได้เอง
Round 2 ยากกว่าเพราะ 3 unknowns — ต้องใช้ external library + local Sage (ดู notes ของ corrupt-key-2)

---

## References

- Writeup: `knowledge/writeups/how-to-fix-corrupted-key.md`
- Round 2 (harder): `workspace/challenges/solved/crypto/corrupt-key-2/notes.md`
