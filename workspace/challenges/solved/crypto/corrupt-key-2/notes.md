# How to fix corrupted key (Round 2)

**Source:** picoMini — "corrupt-key-2"
**Category:** Crypto
**Difficulty:** Hard
**Status:** ✅ solved
**Started:** 2026-07-30
**Solved:** 2026-07-30

---

## ไฟล์ที่ได้รับ

| ชื่อไฟล์ | ประเภท | หมายเหตุ |
|----------|--------|---------|
| private2.key | RSA private key (PEM) | field บางตัวเป็น zero |
| msg2.enc | Ciphertext | 128 bytes = 1 RSA block |

---

## ภาพรวมโจทย์

โจทย์นี้ให้ RSA private key ที่ "เสียหาย" มาแล้วบอกให้ decrypt ข้อความที่เข้ารหัสด้วย key คู่กัน

**RSA คืออะไร (สั้นๆ):**
RSA เป็น asymmetric encryption — ใช้ key คู่: public key เข้ารหัส, private key ถอดรหัส
Private key เต็มๆ ประกอบด้วย: `n` (modulus), `e` (public exponent), `d` (private exponent), `p`, `q` (prime factors ของ n), และค่า precomputed อีกสามตัว

**ทำไม key เสียหายถึงยังมีประโยชน์:**
ถึงแม้ `d, q, dP, dQ, qInv` เป็น zero ทั้งหมด ถ้าเรายังมี `n`, `e`, และ **p บางส่วน** เราก็ยังสามารถ recover `p` เต็มๆ ได้ด้วย math — เพราะ `n = p × q` และ p เป็น prime ที่มีคุณสมบัติพิเศษที่ทำให้ค้นหาได้

---

## Phase 1: Initial Analysis

**เป้าหมายของ phase นี้:** เข้าใจว่า key เสียหายยังไง ส่วนไหนยังใช้ได้ ส่วนไหนหายไป

### Parse ASN.1/DER structure ของ key

```python
from Crypto.PublicKey import RSA

key = RSA.import_key(open("private2.key").read())
print(f"n = {key.n}")
print(f"e = {key.e}")
print(f"d = {key.d}")
print(f"p = {key.p}")
print(f"q = {key.q}")
```

**ทำไมต้อง parse ก่อน:**
PEM file ที่เห็นเป็น base64-encoded DER ซึ่งเป็น binary format ที่เก็บ field ทุกตัวของ RSA key ตาม PKCS#1 standard — เราต้อง parse ออกมาก่อนถึงจะรู้ว่าแต่ละ field มีค่าอะไร เป็น zero หรือเปล่า

**ผลลัพธ์:**
```
n = [1024-bit number — intact]
e = 65537
d = 0   ← zero
p = [ดูเหมือน nonzero ตอนแรก]
q = 0   ← zero
```

**ความหมาย:** `n` กับ `e` ยังสมบูรณ์ ส่วนค่าอื่นเกือบหมด แต่ `p` ดูเหมือนยังมีข้อมูล

### Scan zero-byte gaps ใน p

```python
p_bytes = key.p.to_bytes(key.p.bit_length() // 8 + 1, 'big')[1:]  # ตัด leading sign byte ออก

i, runs = 0, []
while i < len(p_bytes):
    if p_bytes[i] == 0:
        j = i
        while j < len(p_bytes) and p_bytes[j] == 0:
            j += 1
        runs.append((i, j))
        i = j
    else:
        i += 1

print("zero runs:", runs)
for s, e in runs:
    n_bytes = len(p_bytes)
    bit_shift = (n_bytes - e) * 8
    bit_width = (e - s) * 8
    print(f"  bytes [{s}:{e}] → bit_shift={bit_shift}, bit_width={bit_width}")
```

**ทำไมต้อง scan ทั้ง array ไม่ใช่แค่ขอบ:**
ความผิดพลาดที่เกิดขึ้นจริงในการ solve ครั้งนี้คือดูแค่ leading/trailing bytes ของ `p` แล้วไม่เห็น zero → สรุปผิดว่า p ดูดี ทั้งที่จริงๆ มี zero gaps ซ่อนอยู่ **ข้างใน** เป็นสิ่งที่ต้องระวังเสมอ

**ผลลัพธ์:**
```
zero runs: [(s1,e1), (s2,e2), (s3,e3)]
  → gap 1: bit_shift=352, bit_width=40  (5 bytes ที่หายไป)
  → gap 2: bit_shift=240, bit_width=32  (4 bytes ที่หายไป)
  → gap 3: bit_shift=16,  bit_width=40  (5 bytes ที่หายไป)
```

**ความหมาย:** มี **3 ช่อง** ที่ข้อมูลหายไป รวม 112 bits — นี่คือสิ่งที่ต้อง recover

---

## ทำความเข้าใจปัญหา

**112 bits ออกจาก 512-bit prime — มากไปไหม?**

Coppersmith's theorem บอกว่าถ้าเรารู้ approximately 75% ของ p (หรือในทางกลับกัน ไม่รู้แค่ N^0.25 = 25%) เราหา p เต็มๆ ได้ด้วย lattice methods
- 112/512 ≈ 22% ที่ไม่รู้ → ยังอยู่ใน theoretical bound ✓

**Round 1 vs Round 2 — ต่างกันยังไง:**
- Round 1: p ขาดแค่ส่วนท้าย → มีแค่ **1 unknown** → ใช้ univariate Coppersmith (`small_roots()` ใน Sage)
- Round 2: p มี **3 gaps** กระจายอยู่กลาง → มี **3 unknowns** → ต้องใช้ **multivariate** Coppersmith — เป็น technique ที่ซับซ้อนกว่า แต่หลักการเดียวกัน

**Multivariate Coppersmith ทำงานยังไง (ภาพรวม):**
สร้าง polynomial `f(x,y,z) = p_known + x·2^352 + y·2^240 + z·2^16`
โดยที่ `p_known` คือ p ที่ zero-gaps ยังเป็น 0 อยู่
เราต้องหา x, y, z ที่ทำให้ `f(x,y,z) ≡ 0 (mod p)` โดยที่ p หาร n ลงตัว
Lattice reduction (LLL algorithm) + Gröbner basis ช่วยหา root ที่ "เล็ก" พอให้เจอในเวลาอันสมเหตุสมผล

---

## สิ่งที่ลอง

### FactorDB + RsaCtfTool — ❌ ไม่สำเร็จ

**ทำไมลองก่อน:**
เป็น "cheap tier" — ถ้า n ถูก factor ไปแล้วใน database หรือมี classical weakness เช่น small d (Wiener), small e, common factor กับ key อื่น ก็ไม่ต้องใช้ Coppersmith เลย ประหยัดเวลามาก

```bash
# RsaCtfTool ลอง ~40 attacks
python3 RsaCtfTool.py --publickey pub.pem --attack all
```

**ล้มเหลวเพราะ:**
n ของโจทย์นี้ถูกออกแบบมาให้ไม่มี classical weakness — ความท้าทายอยู่ที่ corrupt p เท่านั้น

### sagecell.sagemath.org — ❌ ไม่สำเร็จ

**ทำไมลองก่อน:**
SageMath มี `small_roots()` สำหรับ Coppersmith attacks และ sagecell เปิดให้ใช้ฟรีผ่าน browser — ดูเหมือนสะดวกกว่าติดตั้ง Sage ทั้งหมด

**ล้มเหลวเพราะ:**
Free tier ของ sagecell มี hard limit ประมาณ 15-20 วินาที สำหรับ computation ต่อ kernel
Gröbner basis calculation ที่ต้องใช้กับ 3-variable polynomial นี้ใช้เวลา ~225 วินาที — มากกว่า limit เกือบ 15 เท่า
Server จะ kill kernel ทันทีที่ถึง limit ไม่ว่าจะ reconnect กี่ครั้งก็ตาม

**บทเรียน:** sagecell = quick checks เท่านั้น ถ้า computation หนักต้องใช้ local

### Ubuntu apt install sagemath — ❌ ไม่สำเร็จ

```bash
sudo apt install -y sagemath
# ERROR: Package 'sagemath' has no installation candidate
```

**ล้มเหลวเพราะ:**
Ubuntu 25.04 (Resolute) ตัด SageMath ออกจาก official repos แล้ว — ต้องใช้วิธีอื่น

### WSL2 + conda-forge (Miniforge) — ✅ สำเร็จ

**ทำไมวิธีนี้ได้ผล:**
conda-forge เป็น community-maintained package repository ที่ build SageMath แยกจาก distro — ไม่ขึ้นกับว่า Ubuntu version ไหนจะ include sage หรือเปล่า และไม่ต้อง compile เองซึ่งใช้เวลาหลายชั่วโมง

```bash
# ใน WSL:
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh
conda install sage -c conda-forge -y
```

---

## วิธีที่สำเร็จ: Multivariate Coppersmith

### ขั้นที่ 1 — เตรียม library

ใช้ [`TheBlupper/coppersmith`](https://github.com/TheBlupper/coppersmith) ซึ่งเป็น implementation ของ multivariate small roots
เหตุผลที่ต้องใช้ library นี้แทน built-in Sage: Sage มี `.small_roots()` แต่ **ใช้ได้เฉพาะ univariate** (1 unknown เท่านั้น) — สำหรับ 3 unknowns ต้องใช้ implementation นี้

**Patch ที่ต้องทำก่อนใช้:**
```python
# ใน coppersmith.py บรรทัดที่ probe msolve:
msolve_available = False  # แทนที่ auto-detect ที่ crash ด้วย FeatureNotPresentError
```

**ทำไม msolve crash:**
Library ลอง detect ว่ามี `msolve` (external solver) install อยู่ไหม แต่วิธีที่ detect ทำให้เกิด exception ที่ไม่ถูก catch — การ hardcode `False` ทำให้ใช้ fallback Gröbner basis แทน

### ขั้นที่ 2 — สร้าง polynomial

```python
# solve.sage  ← ต้องเป็น .sage ไม่ใช่ .py!
N = <modulus>
e = 65537
p_approx = <p as integer with zeros still in gaps>

P = PolynomialRing(Zmod(N), 3, 'x,y,z')
x, y, z = P.gens()

# f คือ polynomial ที่ถ้าเราหาค่า x,y,z ที่ถูกต้อง
# f(x,y,z) จะ divisible by p ซึ่ง divide n ได้
f = p_approx + x*2^352 + y*2^240 + z*2^16
```

**อธิบาย polynomial:**
- `p_approx` คือ p ที่เรารู้ — โดยที่ gap positions ยังเป็น 0 อยู่
- `x*2^352` หมายถึง "x คือค่าที่ถูกต้องสำหรับ gap ที่ bit position 352"
- เมื่อ x, y, z เป็นค่าที่ถูกต้อง: `f(x,y,z) = p` นั่นเอง

**ทำไม extension ต้องเป็น `.sage`:**
Sage มี "preparser" ที่แปลง Sage syntax (`^` แทน `**`, `Zmod(N)`, `PolynomialRing(...)` ฯลฯ) ให้เป็น Python ก่อน execute — preparser นี้ทำงานเฉพาะกับไฟล์ `.sage` เท่านั้น ถ้าเป็น `.py` จะ run เป็น plain Python และ `NameError: Zmod` ทันที

### ขั้นที่ 3 — หา roots

```python
sols = small_roots([f], {'x': 40, 'y': 32, 'z': 40}, lat_reduce=LLL)
```

**อธิบาย parameters:**
- `{'x': 40, 'y': 32, 'z': 40}` = bounds — บอก algorithm ว่าแต่ละ unknown มีค่าไม่เกิน 2^40, 2^32, 2^40 ตามลำดับ (= bit width ของแต่ละ gap)
- `lat_reduce=LLL` = ใช้ LLL algorithm สำหรับ lattice reduction ซึ่งเป็น step แรกก่อน Gröbner basis

**ใช้เวลา: ~225 วินาที** บน local WSL (sagecell killed ใน 15-20s)

### ขั้นที่ 4 — Reconstruct p และ decrypt

```python
sol = sols[0]
p = Integer(p_approx + sol['x']*2^352 + sol['y']*2^240 + sol['z']*2^16)

# ตรวจสอบ
assert N % p == 0, "p ไม่ใช่ factor ของ n — ลอง bounds อื่น"

q = N // p
d = power_mod(e, -1, (p-1)*(q-1))

# Decrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
key = RSA.construct((N, e, d, p, q))
plaintext = PKCS1_v1_5.new(key).decrypt(open("msg2.enc","rb").read(), sentinel=b"FAILED")
print(plaintext)
```

**ทำไม assert สำคัญ:**
ถ้า `N % p != 0` แปลว่า root ที่หาได้ไม่ใช่ p จริงๆ — อาจเกิดจาก bounds ผิด หรือ gap positions คำนวณผิด ให้กลับไปตรวจ step 1

---

## Flag

```
picoCTF{1d68da1447328c3f11541d076c9c613957d86566}
```

---

## สิ่งที่เรียนรู้

**Concepts ใหม่ที่ได้เรียน:**
- **Multivariate Coppersmith** — extension ของ univariate สำหรับกรณีที่มีหลาย unknown ใน polynomial เดียวกัน
- **LLL + Gröbner basis pipeline** — วิธีที่ multivariate solver ทำงาน: LLL หา short vectors ใน lattice → Gröbner basis หา actual roots
- **Zero-run scan ทั้ง byte array** — boundary check ไม่พอ ต้อง scan ทุก byte เพื่อหา internal gaps

**Tools ที่ได้ใช้:**
- `TheBlupper/coppersmith` — multivariate small roots (ต้อง patch msolve probe)
- `WSL2 + conda-forge` — วิธีติดตั้ง SageMath บน Windows ที่น่าเชื่อถือที่สุด
- `Crypto.PublicKey.RSA.construct()` — rebuild key จาก (n, e, d, p, q) ที่คำนวณเอง

**Pattern ที่ควรจำสำหรับครั้งต่อไป:**

| ถ้าเห็น... | แปลว่า... | ใช้... |
|-----------|----------|--------|
| p มี zero แค่ท้าย | known high bits, 1 unknown | univariate `p.small_roots()` |
| p มี zero หลายจุดกระจาย | multi-gap, หลาย unknown | multivariate Coppersmith |
| gcd(p_partial, n) == 1 | ไม่ได้แปลว่า decoy | scan internal zero-runs ก่อนสรุป |

**สิ่งที่จะทำต่างออกไปถ้าเจอโจทย์แบบนี้อีก:**
1. Scan full byte array หา zero-runs ทันที (ไม่ดูแค่ขอบ)
2. ค้นหา public writeup ของชื่อโจทย์ก่อน — named CTF มักมีแล้ว
3. ใช้ local sage ทันทีสำหรับ heavy computation (ไม่เสียเวลากับ sagecell)

---

## References

- [TheBlupper/coppersmith](https://github.com/TheBlupper/coppersmith)
- [Connor McCartney writeup](https://connor-mccartney.github.io/cryptography/small-roots/corrupt-key-2-picoMini)
- Full writeup: `knowledge/writeups/how-to-fix-corrupted-key-2.md`
- KB pattern: `knowledge/ctf/multivariate-coppersmith-corrupted-p.md`
