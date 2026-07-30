# CTF Crypto Patterns

## Identify Cipher
```python
# Classic ciphers (short key, letter substitution)
# → try CyberChef "Magic" or quipqiup.com

# Base encoding
base64.b64decode(s)           # standard base64
base64.urlsafe_b64decode(s)   # URL-safe base64
binascii.unhexlify(s)         # hex
int(s, 2).to_bytes(...)       # binary

# Modern: ดู length → AES block = 16 bytes
```

## Common CTF Crypto Patterns

### XOR
```python
# Single-byte XOR → brute force 256 keys
for key in range(256):
    pt = bytes([b ^ key for b in ct])
    if b'flag' in pt or pt.isascii(): print(key, pt)

# Known plaintext XOR key recovery
key = bytes([ct[i] ^ pt[i] for i in range(len(pt))])

# Repeating key XOR (Vigenere-like)
# → find key length with Index of Coincidence or Hamming distance
```

### RSA
```python
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

# Small e, large message → e-th root attack (no padding)
import gmpy2
m, exact = gmpy2.iroot(c, e)  # e=3

# n = p*q, factor if p close to q → Fermat's factorization
# or use factordb.com / RsaCtfTool

# RSA CTF Tool
# python RsaCtfTool.py --publickey pub.pem --uncipherfile cipher.bin
```

### AES ECB
```python
# ECB mode → same plaintext block = same ciphertext block
# CTF: อัพข้อมูลหลายๆ รูปแบบ → สังเกต block ซ้ำ
# เห็น penguin pattern ใน image → ECB mode

# Byte-at-a-time: ส่ง 'A'*n จนเห็น block เปลี่ยน → หา offset
```

### Hash Attacks
```python
# Length extension (MD5/SHA1/SHA2): ใช้ hashpump
# hashpump -s <sig> -d <data> -a <append> -k <key_len>

# MD5 collision: MD5("a") == MD5("b") อาจเป็น magic hash
# PHP: "0e..." == "0e..." (loose comparison)

# Hash crack: hashcat / john / crackstation.net
```

## Tools
- CyberChef — encode/decode/crypto online
- dcode.fr — classical ciphers
- RsaCtfTool — RSA attacks automated
- hashpump — hash length extension
- pycryptodome — Python crypto library
