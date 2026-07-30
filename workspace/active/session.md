# Active Session

## Task
- type: CTF
- name: How to fix corrupted key
- department: offensive-security
- mode: Hint

## Progress
- phase: Analysis (Identify → done, Attack → pending mode selection)
- started: 2026-07-30

## Done
- Identify: private.key is a PEM `RSA PRIVATE KEY` (PKCS#1) with several ASN.1 INTEGER fields zeroed out
- Parsed DER structure field-by-field (version, n, e, d, p, q, dP, dQ, qInv)

## Findings
- `n` (modulus): 1024-bit, intact ✅
- `e` (public exponent): 65537 (0x010001), intact ✅
- `d` (private exponent): 128 bytes, **fully zeroed** ❌
- `p` (prime1): 512-bit prime, **top 256 bits known**, bottom 256 bits zeroed ⚠️ (exactly N^0.25 unknown — classic Coppersmith bound)
- `q` (prime2): **fully zeroed** ❌
- `dP`, `dQ`, `qInv` (CRT params): **fully zeroed** ❌ (these are derivable once p, q, d are known — not independent unknowns)
- `msg.enc`: 128 bytes = exactly one RSA block for this 1024-bit modulus (raw/PKCS1 single-block ciphertext, not chunked)

## Pending
- Confirm challenge classification with user: this is a **partial key exposure / "factoring with high bits known" (Coppersmith) attack** on p
- Recover missing low 256 bits of p via lattice-based small-roots method (needs sage or fpylll)
- Derive q = n / p, then d = e^-1 mod (p-1)(q-1)
- Reconstruct valid PEM private key
- Decrypt msg.enc with recovered key

## Notes
- Waiting on user to choose mode: Hint (default) / Guided / Walkthrough / Full Solution
