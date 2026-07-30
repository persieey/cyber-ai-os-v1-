#!/usr/bin/env python3
"""
crypto-solver.py — CTF crypto quick-solve toolkit
Usage:
  python3 crypto-solver.py xor <hex_ciphertext> <key_byte>
  python3 crypto-solver.py xor-brute <hex_ciphertext>
  python3 crypto-solver.py caesar <text>
  python3 crypto-solver.py rot13 <text>
  python3 crypto-solver.py b64 <text>
  python3 crypto-solver.py hex <hex>
  python3 crypto-solver.py vigenere <text> <key>
  python3 crypto-solver.py rsa-small-e <n> <e> <c>
"""

import sys
import base64
import binascii
import string
import math

def xor_single(ct_hex: str, key: int) -> str:
    ct = bytes.fromhex(ct_hex.replace(" ", ""))
    pt = bytes([b ^ key for b in ct])
    try:
        return pt.decode("utf-8")
    except:
        return pt.decode("latin-1")

def xor_brute(ct_hex: str):
    ct = bytes.fromhex(ct_hex.replace(" ", ""))
    print("[*] XOR single-byte brute force:\n")
    for key in range(256):
        pt = bytes([b ^ key for b in ct])
        try:
            decoded = pt.decode("utf-8")
            printable = sum(c in string.printable for c in decoded) / len(decoded)
            if printable > 0.85:
                print(f"  key=0x{key:02x} ({key:3d}): {decoded[:80]}")
        except:
            pass

def caesar_all(text: str):
    print("[*] Caesar all 26 shifts:\n")
    for shift in range(26):
        result = ""
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                result += chr((ord(c) - base - shift) % 26 + base)
            else:
                result += c
        if any(w in result.lower() for w in ["flag", "the", "ctf", "key", "password"]):
            print(f"  >>> shift={shift:2d}: {result}")
        else:
            print(f"      shift={shift:2d}: {result}")

def vigenere_decrypt(text: str, key: str) -> str:
    key = key.lower()
    result = ""
    ki = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[ki % len(key)]) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c) - base - shift) % 26 + base)
            ki += 1
        else:
            result += c
    return result

def rsa_small_e(n: int, e: int, c: int):
    print(f"[*] RSA small-e attack (e={e})")
    import gmpy2
    m, exact = gmpy2.iroot(c, e)
    if exact:
        print(f"[+] Direct e-th root succeeded!")
        try:
            print(f"    m (int) = {m}")
            print(f"    m (hex) = {hex(m)}")
            print(f"    m (str) = {bytes.fromhex(hex(m)[2:]).decode(errors='replace')}")
        except:
            print(f"    m = {m}")
    else:
        print("[-] Direct root failed (padding present or n is small)")
        print("    Try RsaCtfTool: python RsaCtfTool.py -n <n> -e <e> --uncipher <c>")

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0].lower()

    if cmd == "xor" and len(args) >= 3:
        print(xor_single(args[1], int(args[2], 0)))

    elif cmd == "xor-brute" and len(args) >= 2:
        xor_brute(args[1])

    elif cmd == "caesar" and len(args) >= 2:
        caesar_all(" ".join(args[1:]))

    elif cmd == "rot13" and len(args) >= 2:
        text = " ".join(args[1:])
        print(text.translate(str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        )))

    elif cmd == "b64" and len(args) >= 2:
        text = args[1]
        try:
            decoded = base64.b64decode(text + "==").decode(errors="replace")
            print(f"Standard b64: {decoded}")
        except:
            pass
        try:
            decoded = base64.urlsafe_b64decode(text + "==").decode(errors="replace")
            print(f"URL-safe b64: {decoded}")
        except:
            pass

    elif cmd == "hex" and len(args) >= 2:
        hexstr = args[1].replace(" ", "").replace("0x", "")
        print(bytes.fromhex(hexstr).decode(errors="replace"))

    elif cmd == "vigenere" and len(args) >= 3:
        print(vigenere_decrypt(" ".join(args[1:-1]), args[-1]))

    elif cmd == "rsa-small-e" and len(args) >= 4:
        rsa_small_e(int(args[1]), int(args[2]), int(args[3]))

    else:
        print(__doc__)

if __name__ == "__main__":
    main()
