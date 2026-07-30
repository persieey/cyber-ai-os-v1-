# Pattern: MD5-based IDOR

**Source:** Jitlada Banking — Aegis CTF Day 29 | 2026-07-30
**Category:** Web | IDOR
**Difficulty:** Medium

## Summary

MD5 hash (32 hex chars) ใน URL parameter มักหมายถึง IDOR
เพราะ input จริงๆ คือ sequential integer ที่ predict ได้

## Trigger Signs

- 32 hex chars ใน parameter: `?id=`, `?token=`, `?doc=`, `?file=`
- Hint keywords: "MD5 not secure", "hash", "predictable"
- App ที่มี document/file download

## Attack

```
1. หา hash ของเรา → ตรงกับ md5(integer ไหน)
2. brute force md5(1), md5(2), ... ไปเรื่อยๆ
3. access record admin
```

## Quick Reference — md5(1-10)

| n | md5(n) |
|---|--------|
| 1 | c4ca4238a0b923820dcc509a6f75849b |
| 2 | c81e728d9d4c2f636f067f89cc14862c |
| 3 | eccbc87e4b5ce2fe28308fd9f2a7baf3 |
| 4 | a87ff679a2f3e71d9181a67b7542122c |
| 5 | e4da3b7fbbce2345d7772b0674a318d5 |
| 6 | 1679091c5a880faf6fb5e6087eb1b2dc |
| 7 | 8f14e45fceea167a5a36dedd4bea2543 |
| 8 | c9f0f895fb98ab9159f51fd0297e236d |
| 9 | 45c48cce2e2d7fbdea1afc51c7c6ad26 |
| 10 | d3d9446802a44259755d38e6d163e820 |
