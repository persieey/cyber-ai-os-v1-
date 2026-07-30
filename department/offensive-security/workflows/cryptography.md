# Cryptography CTF Workflow

## Purpose
แนวทางทำ Crypto CTF challenge อย่างมีระบบ ตั้งแต่ identify cipher จนถึง decrypt plaintext

## Phases

---

### Phase 1: Identify
**Goal:** รู้ว่าใช้ cipher หรือ encoding อะไร

Indicators:

| สัญญาณ | Type |
|--------|------|
| เฉพาะ hex (0-9a-f) | Hex encoding |
| มี `=` หรือ `==` ท้าย | Base64 |
| เฉพาะ A-Z (ไม่มีเลข) | Classical cipher (Vigenere, Caesar, Playfair) |
| มี `/+.,:;!-` | Morse code |
| เฉพาะ 0 และ 1 | Binary |
| ตัวเลขขนาดใหญ่ (n, e, c) | RSA |
| Key + ciphertext ให้มา | XOR / AES / Stream cipher |

Tools ระบุ:
```bash
# CyberChef → Magic wand (auto-detect)
# dcode.fr/cipher-identifier
# gchq.github.io/CyberChef
```

Done when: รู้ cipher type

---

### Phase 2: Gather Information
**Goal:** รวบรวม information ทั้งหมดที่ให้มา

Checklist:
- [ ] Ciphertext ทั้งหมด
- [ ] Key (ถ้าให้มา)
- [ ] Plaintext บางส่วน (known-plaintext attack?)
- [ ] Source code ของ encryption
- [ ] ข้อมูลเพิ่มเติมจาก challenge description

Done when: รู้ทุกอย่างที่ให้มา

---

### Phase 3: Attack
**Goal:** Decrypt ciphertext

**หลักการ: scope ก่อนลงมือ — เรียงจากถูก/เร็วไปหาแพง/ช้า อย่า implement ทุก attack พร้อมกัน**
ลองวิธี "เช็คของสำเร็จรูป" (online DB, automated tool) ก่อนเขียน custom script เสมอ
ถ้าวิธีถูกไม่เจอค่อยขยับไปวิธีที่ซับซ้อนขึ้นทีละสเต็ป — ประหยัดทั้งเวลาและ token

#### Classical Ciphers
```python
# Caesar / ROT-n → brute force ทุก rotation
for n in range(26):
    print(f"ROT-{n}: {rot_n(ciphertext, n)}")

# Vigenere → Kasiski + Frequency analysis
# dcode.fr/vigenere-cipher (online)

# XOR → ลอง single-byte XOR
for key in range(256):
    pt = bytes([c ^ key for c in ct])
    if all(32 <= b <= 126 for b in pt):
        print(f"Key {key}: {pt}")
```

#### Encoding
```python
import base64

base64.b64decode(ciphertext)
bytes.fromhex(ciphertext)
int(ciphertext, 2).to_bytes(...)  # binary

# Multiple layers → ลอง decode ซ้ำ
```

#### RSA

**ก่อนเขียนโค้ด custom attack (Coppersmith/lattice/Wiener) ให้เช็คของถูกก่อนเสมอ — ไม่งั้นเสียเวลา/token ฟรี:**

```
1. เช็ค n กับ FactorDB ก่อนเสมอ (วินาทีเดียว, ฟรี)
   GET http://factordb.com/api?query=<n>
   status "FF"/"F" = ได้ p,q ทันที ไม่ต้องทำอะไรต่อ

2. ถ้าไม่มีใน FactorDB → ลอง RsaCtfTool อัตโนมัติก่อน (ครอบคลุมหลาย attack พร้อมกัน)
   python RsaCtfTool.py --publickey pub.pem --uncipherfile cipher.bin --attack all

3. ต่อเมื่อ 1-2 ไม่เจอ ค่อยพิจารณา manual/custom attack ตาม signature ที่เจอจริง
   (ดู bit ที่รู้/ไม่รู้ของ p,q,d,e ก่อนเลือกว่าจะ implement อะไร — อย่า implement ทุกอย่างไล่ตาม)
```

```python
# Small e attack (e=3, small message)
from gmpy2 import iroot
m, exact = iroot(c, e)
if exact:
    print(long_to_bytes(m))

# Wiener attack → small d
# n=p*q, p,q ใกล้กัน → Fermat factorization
# รู้ high/low bits บางส่วนของ p → Coppersmith (ต้อง sage/fpylll — หนักสุด ทำเป็นตัวเลือกสุดท้าย)
#   - รู้ต่อเนื่องเป็นก้อนเดียว (prefix/suffix) → univariate Coppersmith
#   - รู้เป็นหลายช่วงกระจัดกระจาย (multiple zero-byte gaps ใน p) → multivariate Coppersmith
#     ต้อง Sage จริง (sage.all) ไม่ใช่แค่ sympy/fpylll — ดู knowledge/ctf/multivariate-coppersmith-corrupted-p.md
#     sagecell.sagemath.org (free) ฆ่า kernel ทิ้งหลังรันหนักไม่กี่วิ — ใช้ WSL2 + conda-forge sage แทนถ้างานหนักจริง
```

#### Hash Cracking
```bash
hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt   # MD5
john --wordlist=rockyou.txt hash.txt
# Online: crackstation.net
```

Done when: ได้ plaintext หรือ flag

---

### Phase 4: Documentation
1. อัพเดต `workspace/active/session.md` → Findings
2. บันทึก technique ใน `/kb add ctf <cipher-name>`
3. รัน Report Agent

---

## Quick Reference

```
Identify → CyberChef Magic / dcode.fr
Classical → Brute force / frequency analysis
RSA → Small e, factor n, Wiener
XOR → Known-plaintext / brute force
Hash → hashcat / john / crackstation
```
