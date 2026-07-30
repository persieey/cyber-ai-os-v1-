#!/usr/bin/env python3
"""
hash-identify.py — Identify hash type and suggest hashcat mode
Usage: python3 hash-identify.py <hash>
"""

import sys
import re

PATTERNS = [
    # Format: (name, hashcat_mode, regex_or_check_fn)
    ("bcrypt",              3200, r"^\$2[ayb]\$.{56}$"),
    ("sha512crypt (Linux)", 1800, r"^\$6\$.{0,16}\$[A-Za-z0-9./]{86}$"),
    ("sha256crypt (Linux)", 7400, r"^\$5\$.{0,16}\$[A-Za-z0-9./]{43}$"),
    ("md5crypt (Linux)",    500,  r"^\$1\$.{0,8}\$[A-Za-z0-9./]{22}$"),
    ("NTLM",               1000, r"^[0-9a-fA-F]{32}$"),        # same len as MD5
    ("MD5",                0,    r"^[0-9a-fA-F]{32}$"),
    ("SHA-1",              100,  r"^[0-9a-fA-F]{40}$"),
    ("SHA-256",            1400, r"^[0-9a-fA-F]{64}$"),
    ("SHA-512",            1700, r"^[0-9a-fA-F]{128}$"),
    ("MySQL4.1+",          300,  r"^\*[0-9A-F]{40}$"),
    ("MySQL3.x",           200,  r"^[0-9a-fA-F]{16}$"),
    ("NetNTLMv2",          5600, r"^[^:]+:[^:]+:[0-9A-F]{32}:[0-9A-F]{32}:[0-9A-F]+$"),
    ("NetNTLMv1",          5500, r"^[^:]+:[^:]+:[0-9A-F]{48}:[0-9A-F]{48}:[0-9A-F]{16}$"),
    ("Kerberos TGS",       13100, r"^\$krb5tgs\$"),
    ("Kerberos AS-REP",    18200, r"^\$krb5asrep\$"),
    ("WPA Handshake",      2500, None),  # file-based
    ("Argon2",             None, r"^\$argon2"),
    ("MD5($salt.$pass)",   20,   r"^[0-9a-fA-F]{32}:[^:]{1,32}$"),
    ("SHA1($salt.$pass)",  110,  r"^[0-9a-fA-F]{40}:[^:]{1,32}$"),
    ("Base64 encoded",     None, r"^[A-Za-z0-9+/]{20,}={0,2}$"),
]

def identify(h: str):
    matches = []
    for name, mode, pattern in PATTERNS:
        if pattern and re.match(pattern, h.strip()):
            matches.append((name, mode))
    return matches

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    h = sys.argv[1].strip()
    print(f"\n[*] Hash: {h}")
    print(f"    Length: {len(h)} chars\n")

    matches = identify(h)

    if not matches:
        print("[-] Unknown hash type")
        print("    Try: https://hashes.com/en/tools/hash_identifier")
        return

    print(f"[+] Possible types:\n")
    for name, mode in matches:
        mode_str = f"-m {mode}" if mode is not None else "(see docs)"
        print(f"    {name}")
        print(f"      hashcat {mode_str} hash.txt rockyou.txt")
        print(f"      john --wordlist=rockyou.txt hash.txt")
        print()

    print("[*] Quick crack commands:")
    for name, mode in matches[:1]:
        if mode is not None:
            print(f"    hashcat -m {mode} '{h}' /usr/share/wordlists/rockyou.txt --force")
            print(f"    python3 tools/exploitation/hash-crack.sh '{h}'")

if __name__ == "__main__":
    main()
