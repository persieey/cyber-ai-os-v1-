# CTF Writeup Template

**CTF:** picoCTF / picoMini
**Challenge:** How to fix corrupted key (round 2) — picoMini "corrupt-key-2"
**Category:** Crypto
**Difficulty:** Hard
**Points:** —
**Solved:** 2026-07-30

---

## TL;DR
`private2.key` is a PEM RSA private key where `d, q, dP, dQ, qInv` are fully zeroed and `p` has **3 separate internal zero-byte gaps** (112 bits missing total, not just a truncated suffix like round 1). This needs **multivariate Coppersmith** (3 simultaneous unknowns) — a univariate attack or a decoy-value assumption both fail. Solved with SageMath's `small_roots`-style multivariate solver (`TheBlupper/coppersmith`, Gröbner-basis rootfinding) run **locally via WSL2 + conda-forge SageMath**, since the free hosted `sagecell.sagemath.org` cannot finish a computation this heavy (hard kernel-kill limit, ~15-20s into the expensive step, no matter how many times you retry or reconnect).

---

## Reconnaissance
Same starting point as round 1: `private2.key` (PKCS#1 RSA private key, PEM) + `msg2.enc` (128 bytes = 1 RSA block for a 1024-bit modulus).

Parsed ASN.1/DER field-by-field (see [corrupted-rsa-key-factordb.md](../ctf/corrupted-rsa-key-factordb.md) for the parser script):

| Field | Status |
|---|---|
| `n` (1024-bit), `e` (65537) | intact |
| `d`, `q`, `dP`, `dQ`, `qInv` | fully zeroed |
| `p` (512-bit) | **looked nonzero everywhere at first glance** |

**Critical mistake made initially:** checking only leading/trailing zero bytes of `p` said "no corruption" — but `p` actually had 3 zero-byte runs *in the middle*. Always scan the *entire* byte array for zero runs, not just the boundary:

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

This revealed 3 gaps (excluding the leading ASN.1 sign byte): 5 bytes, 4 bytes, 5 bytes = **112 bits missing total**, at bit-shifts 352, 240, 16 from the LSB of the 512-bit prime.

## Analysis
`gcd(p_with_gaps_zeroed, n) == 1` and the value isn't prime — this can look like a "decoy" (as in a naive read), but it's actually the expected shape for a **multi-gap corrupted prime**, which is a documented picoMini pattern (see [Connor McCartney's writeup](https://connor-mccartney.github.io/cryptography/small-roots/corrupt-key-2-picoMini) and the [CyLab Medium writeup](https://medium.com/@jenishb2006/cylab-corrupt-key-2-writeup-rsa-private-key-recovery-using-multivariate-coppersmiths-method-051e1d9567e3) — both confirm the exact same gap structure and parameters).

112 unknown bits out of 1024-bit N (≈11%) is well inside the theoretical Coppersmith bound (N^0.25 = 25% for a single block; multi-block linear relations mod an unknown factor have a somewhat tighter but still comfortable margin here), so this is solvable — it just needs the **multivariate** construction (Jochemsz-May / Herrmann-May style shift polynomials + Gröbner basis rootfinding), not the simpler univariate one from round 1.

## Exploitation

### Step 1 — cheap tier first (per [[feedback_scope_before_attack]])
Before touching Coppersmith: FactorDB (`status: C`, not factored), common-modulus check against round 1's `n` (no shared factor), trial division, Fermat, Pollard p-1/rho, Wiener, and a full `RsaCtfTool --attack all` pass (~40 attacks, none requiring sage/yafu) — **all failed**. This confirmed the modulus itself has no classical weakness; the corruption in `p` is the only way in.

### Step 2 — get a real multivariate Coppersmith solver
Sage has no built-in `.small_roots()` for multivariate polynomials over `Zmod(N)` (only univariate). Used [`TheBlupper/coppersmith`](https://github.com/TheBlupper/coppersmith) — a from-scratch multivariate small-roots implementation (shift polynomials + graph-search dense-sublattice selection + Gröbner-basis rootfinding). It hard-requires `sage.all`, so it cannot run outside a real Sage environment.

### Step 3 — where to run Sage
**Tried and failed:** `sagecell.sagemath.org`'s public JSON/WebSocket kernel API (no local install needed) — got real Sage execution working (confirmed via `factor()`), but the free anonymous kernel gets **killed by the server** roughly 15-20 seconds into the Gröbner-basis/graph-search step, every single time, even after reconnecting the websocket up to 50 times. This is a hard resource limit on the free tier, not a network fluke — **do not rely on sagecell for genuinely heavy lattice/Gröbner computations.**

**What worked:** local WSL2 + conda-forge SageMath (`sage` isn't in Ubuntu 26.04's apt repos yet — use conda-forge instead):
```bash
wsl --install                                    # from an elevated Windows PowerShell, needs reboot
# inside WSL:
curl -L -o ~/miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash ~/miniforge.sh -b -p ~/miniforge3
~/miniforge3/bin/mamba create -n sage -c conda-forge sage python=3.11 fpylll -y
```

### Step 4 — the attack itself
```python
# paste TheBlupper/coppersmith's coppersmith.py content first (defines small_roots, LLL, etc.)
# then, IMPORTANT: msolve isn't installed — hardcode msolve_available = False
# instead of letting the msolve-detection probe crash with FeatureNotPresentError

N = <modulus>
e = 65537
p_approx = <p with the 3 gaps already zeroed, as read straight from the file>

P = PolynomialRing(Zmod(N), 3, 'x,y,z')
x, y, z = P.gens()
f = p_approx + x*2^352 + y*2^240 + z*2^16   # shifts = bit position of each gap's LSB
sols = small_roots([f], {'x': 40, 'y': 32, 'z': 40}, lat_reduce=LLL)  # bounds = each gap's bit width

sol = sols[0]
p = Integer(p_approx + sol['x']*2^352 + sol['y']*2^240 + sol['z']*2^16)
assert N % p == 0
q = N // p
d = power_mod(e, -1, (p-1)*(q-1))
```

**Must run as a `.sage` file, not `.sage.py`** — Sage's preparser (which provides `Zmod`, `^` as power, `PolynomialRing`, etc.) only triggers on the `.sage` extension; a `.py` file is executed as plain CPython and `Zmod` etc. will be `NameError`.

Ran in **225 seconds** locally with no external time limit — proof the computation itself was never the bottleneck, only sagecell's kernel-kill policy was.

### Step 5 — decrypt
```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
key = RSA.construct((n, e, d, p, q))
PKCS1_v1_5.new(key).decrypt(open("msg2.enc","rb").read(), sentinel=b"FAILED")
```

## Flag
```
picoCTF{1d68da1447328c3f11541d076c9c613957d86566}
```

## Lessons Learned
- **Scan the whole byte array for zero-runs, not just leading/trailing** — a corrupted field that "looks nonzero at a glance" can still have internal gaps. Verify with `gcd`/primality before concluding something is a decoy.
- Known-high-bits (round 1) → univariate Coppersmith. Multiple scattered gaps (round 2) → multivariate Coppersmith with Jochemsz-May shift polynomials + Gröbner-basis rootfinding — genuinely different tooling, not just "bigger m".
- Sage has no built-in multivariate `small_roots` — need an external implementation (`TheBlupper/coppersmith` or `defund/coppersmith`), and both hard-require real Sage (`sage.all`), not just sympy/fpylll.
- **`sagecell.sagemath.org`'s free API cannot run heavy Coppersmith/Gröbner computations** — it kills the kernel after ~15-20s of heavy work regardless of reconnects. Confirmed by running the *identical* code locally afterward in 225s with no issue. Use it only for quick, light checks — not real attacks.
- For genuine Sage needs on Windows: **WSL2 + conda-forge (`mamba create -n sage -c conda-forge sage fpylll`)** is more reliable than `apt install sagemath` (often missing/outdated in Ubuntu's default repos) and avoids native compilation entirely.
- Sage files needing the preparser (`Zmod`, `^`, `PolynomialRing(...)` sugar) must have a `.sage` extension, not `.py` — `sage somefile.py` runs plain CPython.
- Public writeups for named/archived CTF challenges (picoMini, older picoCTF) are worth searching for *before* reverse-engineering the corruption pattern from scratch — the exact bit-shifts and bounds we needed were already published.
