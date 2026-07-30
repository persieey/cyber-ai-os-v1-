# IR Playbooks

## Ransomware
1. **Isolate** — ตัด network ทันที (ไม่ shutdown)
2. **Preserve** — memory dump, disk image ก่อนทำอะไร
3. **Identify** — ransomware family (ID Ransomware website), encryption extension
4. **Check backup** — offline/cloud backup ถูก encrypt ไหม?
5. **Eradicate** — ลบ ransomware + persistence (registry, scheduled task)
6. **Recover** — restore จาก backup, scan ก่อน bring online

**อย่าทำ:** จ่าย ransom โดยไม่ปรึกษา legal / cyber insurance ก่อน

## Data Breach / Exfiltration
1. **Identify scope** — data อะไรถูก access? กี่ records?
2. **Preserve logs** — CloudTrail, proxy logs, DLP alerts
3. **Revoke access** — token, API key, credentials ที่ถูก compromise
4. **Notify** — legal team, PDPA obligation (72h notification ถ้า EU data)
5. **Patch vector** — close the hole ที่ถูก exploit

## Phishing / BEC
1. **Quarantine email** — delete from all mailboxes
2. **Check clicks** — ใครคลิก link? รัน payload ไหม?
3. **Reset credentials** — ทุก account ที่อาจถูก compromise
4. **Enable MFA** — ถ้ายังไม่มี
5. **Block IOC** — domain, IP, attachment hash

## Unauthorized Access
1. **Identify entry point** — VPN? RDP? Web shell? Phishing?
2. **Check lateral movement** — host อื่นถูก compromise ไหม?
3. **Collect artifacts** — bash_history, auth.log, Windows Event 4624
4. **Evict attacker** — เปลี่ยน password ทุก account, kill sessions
5. **Patch** — close initial access vector
