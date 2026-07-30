# Writeup: Jitlada Banking (Day 29)

**Platform:** Aegis CTF
**Date:** 2026-07-30
**Points:** 50 + 25 FB
**Category:** Web
**Difficulty:** Medium
**Flag:** `aegis{kKX6THlWVlF7IFhoqRnFdF1ZXHUSkYqT}`

---

## Summary

Banking web app ที่ใช้ `md5(loan_id)` เป็น document identifier ทำให้ IDOR ได้
เข้าถึง loan document ของ admin ที่มี flag ซ่อนอยู่ใน Notes field

---

## Attack Path

### 1. Recon
- Register account ปกติ
- สำรวจทุก page: dashboard, deposit, transfer, loan, credit-card, transactions

### 2. Discovery
- Apply for loan → ได้ URL: `/loan/download?id=c9f0f895fb98ab9159f51fd0297e236d`
- สังเกตว่า `c9f0f895...` = `md5("8")` → เราเป็น Loan #8

### 3. IDOR
- ลอง `md5("1")` ถึง `md5("7")` ทีละตัว
- Loan #6 (`md5("6") = 1679091c...`) = Jitlada Admin → มี flag

### 4. Flag
```
GET /loan/download?id=1679091c5a880faf6fb5e6087eb1b2dc
→ Notes: Confidential Admin Token: aegis{kKX6THlWVlF7IFhoqRnFdF1ZXHUSkYqT}
```

---

## Lessons Learned

- MD5 ใน URL parameter → ลอง IDOR ก่อนเสมอ
- ไม่ต้อง crack หรือ bypass login — attack surface อยู่ที่ document download
- Prompt Injection ใน HTML (`display:none`) ที่ Aegis ใส่ไว้ เป็น anti-AI measure ไม่ใช่ part ของ challenge

---

## Tools Used

- Browser DevTools
- JavaScript fetch() ใน console

## Related Knowledge

- [[ctf/md5-idor]]
