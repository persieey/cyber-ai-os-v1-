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
```python
# Small e attack (e=3, small message)
from gmpy2 import iroot
m, exact = iroot(c, e)
if exact:
    print(long_to_bytes(m))

# Factorization → factordb.com
# Wiener attack → small d
# n=p*q, p,q ใกล้กัน → Fermat factorization
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
