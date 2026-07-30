#!/usr/bin/env python3
"""
decode.py — Swiss-army decoder for CTF
Usage: python3 decode.py <input> [--all]

Auto-detects and tries: base64, base32, hex, url, rot13, binary, morse
"""

import sys
import base64
import binascii
import urllib.parse
import re

MORSE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9',
}

def try_b64(s):
    try:
        padded = s + "=" * (-len(s) % 4)
        return base64.b64decode(padded).decode(errors="replace")
    except:
        return None

def try_b64url(s):
    try:
        return base64.urlsafe_b64decode(s + "==").decode(errors="replace")
    except:
        return None

def try_b32(s):
    try:
        return base64.b32decode(s.upper()).decode(errors="replace")
    except:
        return None

def try_hex(s):
    clean = s.replace(" ", "").replace("0x", "").replace("\\x", "")
    try:
        return bytes.fromhex(clean).decode(errors="replace")
    except:
        return None

def try_url(s):
    try:
        decoded = urllib.parse.unquote(s)
        if decoded != s:
            return decoded
    except:
        pass
    return None

def try_rot13(s):
    return s.translate(str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
    ))

def try_binary(s):
    clean = s.replace(" ", "")
    if not re.fullmatch(r'[01]+', clean):
        return None
    if len(clean) % 8 != 0:
        return None
    try:
        chars = [chr(int(clean[i:i+8], 2)) for i in range(0, len(clean), 8)]
        return "".join(chars)
    except:
        return None

def try_morse(s):
    words = s.strip().split("   ")
    try:
        result = " ".join(
            "".join(MORSE.get(ch, "?") for ch in word.split())
            for word in words
        )
        if "?" not in result:
            return result
    except:
        pass
    return None

def try_decimal(s):
    nums = s.strip().split()
    try:
        return "".join(chr(int(n)) for n in nums if n.isdigit())
    except:
        return None

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    data = sys.argv[1]
    show_all = "--all" in sys.argv

    print(f"[*] Input: {data[:80]}{'...' if len(data) > 80 else ''}\n")

    decoders = [
        ("Base64",        try_b64),
        ("Base64 URL",    try_b64url),
        ("Base32",        try_b32),
        ("Hex",           try_hex),
        ("URL encode",    try_url),
        ("ROT13",         try_rot13),
        ("Binary",        try_binary),
        ("Morse",         try_morse),
        ("Decimal ASCII", try_decimal),
    ]

    found = False
    for name, fn in decoders:
        result = fn(data)
        if result and result != data:
            printable = sum(c.isprintable() for c in result) / max(len(result), 1)
            if show_all or printable > 0.8:
                flag_hint = " ← FLAG?" if re.search(r'flag|ctf|\{.*\}', result, re.I) else ""
                print(f"[{name}]{flag_hint}")
                print(f"  {result[:200]}\n")
                found = True

    if not found:
        print("[-] No successful decoding found")
        print("    Try: CyberChef Magic, or specify encoding manually")

if __name__ == "__main__":
    main()
