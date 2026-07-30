# Pattern: Multi-Gap Corrupted RSA Prime → Multivariate Coppersmith

**Source:** How to fix corrupted key (round 2) — picoMini "corrupt-key-2" | 2026-07-30
**Category:** Crypto | RSA
**Difficulty:** Hard

## Summary

If a corrupted RSA private key's `p` has **multiple separate zero-byte gaps scattered through the middle** (not just a truncated prefix/suffix), that's a multivariate Coppersmith problem, not univariate. See [corrupted-rsa-key-factordb.md](corrupted-rsa-key-factordb.md) for the single-gap (round 1) case first.

## Trigger Signs

- `p` field has zero-runs at 2+ separate positions inside the byte array (scan the *whole* array — checking only leading/trailing zeros will miss this and make `p` look like garbage/decoy data instead)
- `gcd(p_with_gaps_zeroed, n) == 1` and it's not prime — don't conclude "decoy", check for internal gaps first
- Total missing bits comfortably under ~25% of N's bit length (N^0.25) → solvable; each extra gap costs some margin vs. a single contiguous gap, but a well-designed challenge leaves room

## Diagnose

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
# runs = [(start,end), ...] byte ranges that are zero (exclude the leading ASN.1 sign byte)
```

For each gap `(s, e)` in a stripped (no leading sign byte) N-byte value: bit-shift = `(N - e) * 8`, bit-width = `(e - s) * 8`.

## Attack

1. **Cheap tier first** (FactorDB, common-modulus vs other known n's from the same challenge set, trial division, Fermat, Pollard p-1/rho, Wiener, `RsaCtfTool --attack all`) — rule out classical weaknesses before touching Coppersmith. See [[feedback_scope_before_attack]].
2. Search for a public writeup of the exact challenge name first — named/archived CTFs (picoMini etc.) often already have the exact bit-shifts/bounds documented.
3. Build `f(x0,x1,...) = p_approx + x0*2^shift0 + x1*2^shift1 + ...` over `PolynomialRing(Zmod(N), k, 'x0,x1,...')`.
4. Use a real multivariate small-roots solver — Sage has **no built-in multivariate `small_roots`** (only univariate). Use [`TheBlupper/coppersmith`](https://github.com/TheBlupper/coppersmith) (`small_roots(polys, sizes, lat_reduce=LLL)`) or [`defund/coppersmith`](https://github.com/defund/coppersmith). Both hard-require real Sage (`from sage.all import ...`), not sympy/fpylll alone.
5. `TheBlupper/coppersmith` probes for `msolve` on import and can crash with `FeatureNotPresentError` if it's absent (the code only catches `CalledProcessError`) — patch: hardcode `msolve_available = False` instead of the probe.
6. Once a root is found: `p = p_approx + sum(xi * 2^shifti)`, verify `N % p == 0`, then standard `q = N//p`, `d = pow(e,-1,(p-1)*(q-1))`.

## Where to run Sage

- **`sagecell.sagemath.org` (free hosted, no install)** — fine for quick checks, but its free anonymous kernels get killed ~15-20s into a heavy Gröbner-basis/graph-search computation, every time, even with websocket reconnects. **Do not rely on it for real multivariate Coppersmith attacks.**
- **Local WSL2 + conda-forge (reliable, no time limit):**
  ```bash
  wsl --install                     # elevated PowerShell, needs reboot
  # inside WSL — apt's sagemath package is often missing/outdated, use conda-forge instead:
  curl -L -o ~/miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
  bash ~/miniforge.sh -b -p ~/miniforge3
  ~/miniforge3/bin/mamba create -n sage -c conda-forge sage python=3.11 fpylll -y
  ~/miniforge3/envs/sage/bin/sage script.sage
  ```
- Script must have a **`.sage`** extension, not `.py` — the Sage preparser (which provides `Zmod`, `^` as power, `x = P.gens()` sugar) only triggers on `.sage` files; `sage foo.py` runs it as plain CPython and globals like `Zmod` won't exist.

## Related
- [Corrupted RSA Key Pattern (round 1, single gap)](corrupted-rsa-key-factordb.md)
- [how-to-fix-corrupted-key-2.md writeup](../writeups/how-to-fix-corrupted-key-2.md) — full solve, this exact case
