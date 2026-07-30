# Workflow: RSA Partial Key Exposure

maturity: validated
last_validated: 2026-07-30
evidence: picoMini "corrupt-key-2" — solved locally in 225s after confirming sagecell limit

## Input
- RSA private key (PKCS#1 PEM) ที่มีบาง field เป็น zero
- Ciphertext ที่เข้ารหัสด้วย public key คู่กัน

## ขั้นตอน

### 0. Cheap tier ก่อนเสมอ
FactorDB, common-modulus vs other challenge keys, RsaCtfTool --attack all, Fermat, Pollard rho/p-1, Wiener — rule out classical weaknesses first

### 1. Parse + diagnose
```python
from Crypto.PublicKey import RSA
key = RSA.import_key(open("private.key").read())
n, e, d, p, q = key.n, key.e, key.d, key.p, key.q

p_bytes = p.to_bytes(p.bit_length() // 8 + 1, 'big')[1:]  # strip ASN.1 sign byte

# find ALL zero-runs in full byte array
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
print("zero runs (byte indices):", runs)
```

### 2. ตัดสินใจ: univariate หรือ multivariate?

| เงื่อนไข | Attack |
|---------|--------|
| 1 gap, อยู่ท้ายสุด (known high bits) | Univariate `p.small_roots()` ใน Sage |
| 2+ gaps หรือ gap อยู่กลาง | Multivariate Coppersmith (TheBlupper/coppersmith) |

คำนวณ bit-shift ของแต่ละ gap: `shift = (total_p_bytes - gap_end_byte) * 8`

### 3. Multivariate Coppersmith (กรณี 2+ gaps)

ต้องใช้ **WSL2 + local SageMath** (sagecell ไม่พอสำหรับงานนี้):
```bash
# activate sage env ใน WSL
conda activate sage
# รัน script (ต้องเป็น .sage extension ไม่ใช่ .py)
sage solve.sage
```

```python
# solve.sage
# 1. วาง coppersmith.py content จาก TheBlupper/coppersmith ก่อน
# 2. patch: msolve_available = False  (ถ้า msolve ไม่ถูก install)

N = <modulus from key>
e = 65537
p_approx = <p as integer, gaps already zeroed>

# สร้าง polynomial ด้วย 1 variable ต่อ 1 gap
P = PolynomialRing(Zmod(N), k, 'x0,x1,...')  # k = number of gaps
x0, x1, x2 = P.gens()
f = p_approx + x0*2^shift0 + x1*2^shift1 + x2*2^shift2

# bounds = bit-width ของแต่ละ gap
sols = small_roots([f], {'x0': bits0, 'x1': bits1, 'x2': bits2}, lat_reduce=LLL)

sol = sols[0]
p = Integer(p_approx + sol['x0']*2^shift0 + sol['x1']*2^shift1 + sol['x2']*2^shift2)
assert N % p == 0
```

### 4. Rebuild key + decrypt
```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

q = N // p
d = pow(e, -1, (p-1)*(q-1))
key = RSA.construct((n, e, d, p, q))
plaintext = PKCS1_v1_5.new(key).decrypt(open("msg.enc","rb").read(), sentinel=b"FAILED")
print(plaintext)
```

## Output
- Recovered private key (PEM)
- Decrypted plaintext / flag

## Troubleshooting

| ปัญหา | สาเหตุ | แก้ไข |
|------|--------|-------|
| `NameError: Zmod` | รัน `.py` ด้วย `sage script.py` | เปลี่ยน extension เป็น `.sage` |
| sagecell kernel killed | Free tier hard limit ~15-20s | ใช้ WSL2 + local sage แทน |
| `FeatureNotPresentError: msolve` | TheBlupper/coppersmith probe crash | hardcode `msolve_available = False` ใน coppersmith.py |
| `sols = []` ว่าง | bounds ผิด หรือ shift ผิด | ตรวจ zero-run positions อีกรอบ + ลอง bounds ±8 bits |
| computation ไม่จบ | จำนวน unknown variables มากเกินไป | ใช้ known constraints เพิ่ม (เช่น p mod small_prime) ถ้ามี |
