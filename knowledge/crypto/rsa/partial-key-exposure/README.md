# RSA Partial Key Exposure

## แนวคิด

RSA private key ที่มีบาง field เป็น zero หรือมี zero-byte gaps อยู่ใน `p` — แต่ `n` และ `e` ยังสมบูรณ์ — สามารถ recover prime factor ได้ด้วย Coppersmith's method ซึ่งหา "small roots" ของ polynomial mod N

มีสองรูปแบบหลัก:

| รูปแบบ | Known Part | Method |
|-------|-----------|--------|
| **Single gap / known high bits** | p บน 256 bits ของ 512-bit prime | Univariate Coppersmith (`p.small_roots()` ใน Sage) |
| **Multiple scattered gaps** | p มีหลาย zero-run กลางตัว | Multivariate Coppersmith (TheBlupper/coppersmith หรือ defund/coppersmith) |

## ใช้เมื่อไร

- ได้ RSA private key (PEM/DER) ที่ `d, q, dP, dQ, qInv` เป็น zero แต่ `p` มีข้อมูลบางส่วน
- `gcd(p_partial, n) == 1` — แสดงว่า p ไม่สมบูรณ์ ไม่ใช่ decoy
- Total unknown bits < ~25% ของ N's bit length (N^0.25 boundary)

**สำคัญ:** scan ทั้ง byte array ของ `p` เพื่อหา zero-run ทุกจุด — อย่าดูแค่ leading/trailing:

```python
i = 0
runs = []
while i < len(p_bytes):
    if p_bytes[i] == 0:
        j = i
        while j < len(p_bytes) and p_bytes[j] == 0:
            j += 1
        runs.append((i, j))
        i = j
    else:
        i += 1
```

## ข้อจำกัด

- Sage ไม่มี built-in multivariate `small_roots()` — ต้องใช้ external library (TheBlupper/coppersmith)
- `sagecell.sagemath.org` ถูก kernel-kill หลัง ~15-20s สำหรับ heavy Gröbner-basis computation — ใช้ได้แค่ quick checks
- สำหรับ Windows: ต้องรันผ่าน **WSL2 + conda-forge** (`apt install sagemath` มักหา package ไม่เจอใน Ubuntu 25.04+)
- Script ต้องใช้ extension `.sage` ไม่ใช่ `.py` เพื่อให้ Sage preparser ทำงาน (`Zmod`, `^`, `PolynomialRing` sugar)

## อ้างอิง

- TheBlupper/coppersmith — multivariate small roots implementation
- defund/coppersmith — อีก implementation หนึ่ง
- Coppersmith (1996) — Finding Small Solutions to Small Degree Polynomials
- Herrmann & May (2010) — Maximizing Small Root Bounds by Linearization and Applications to Coppersmith's Method
- [picoCTF corrupt-key-2 writeup (Connor McCartney)](https://connor-mccartney.github.io/cryptography/small-roots/corrupt-key-2-picoMini)
