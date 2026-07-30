# Security Hardening Entry Point

Read these files in order:
1. `department/defensive-security/roles/hardening-specialist.md` — your role

Arguments: $ARGUMENTS
(Expected: `linux` | `windows` | `web <server>` | `network` | `cloud <provider>`)

---

## If target is "linux"
Run the Linux hardening checklist from `roles/hardening-specialist.md`
Focus areas: SSH, users, services, filesystem, firewall, logging

## If target is "windows"
Run Windows hardening checklist
Focus areas: SMB, RDP, Defender, audit policy, local accounts, PowerShell logging

## If target is "web <nginx|apache|iis>"
Web server hardening:
- HTTP security headers (CSP, HSTS, X-Frame-Options)
- TLS configuration (disable TLS 1.0/1.1, weak ciphers)
- Directory listing disabled
- Server version hidden
- Rate limiting

## If target is "network"
Network device hardening:
- Default credentials changed
- Unused services/ports closed
- Management plane restricted
- NTP, Syslog configured
- SNMP v3 only

## If target is "cloud <aws|azure|gcp>"
Route to cloud-security department:
- Load appropriate auditor role
- Run CIS Benchmark checks

---

## Output Format
```
## [Target] Hardening Report

### Critical (แก้ทันที)
- [ ] item: ปัญหา → วิธีแก้

### High
- [ ] ...

### Passed ✅
- [x] ...
```

Start response with:
**[Hardening] [Target: <target>]**
