# Skill: JADX (Android Decompiler)

## Install
```bash
# Kali
sudo apt install jadx

# Manual
wget https://github.com/skylot/jadx/releases/latest/download/jadx-*.zip
unzip jadx-*.zip
```

## Decompile to Java
```bash
jadx -d output/ app.apk
# output/sources/ = Java source code
# output/resources/ = res, assets, manifest
```

## GUI Mode
```bash
jadx-gui app.apk
# คลิก class ดู decompiled Java
# Ctrl+F → search across all code
```

## Search for Secrets (CLI)
```bash
# Grep decompiled source
grep -r "api_key\|apikey\|secret\|password\|token\|AWS_" output/sources/
grep -r "http://" output/sources/
grep -r "firebase\|google" output/sources/

# Base64 strings
grep -rE "[A-Za-z0-9+/]{20,}={0,2}" output/sources/
```

## CTF Patterns
- Flag ใน `BuildConfig.java` → `DEBUG_FLAG = "flag{...}"`
- Encrypted string ใน static block → decrypt ด้วย Python
- Hidden activity ที่ไม่ได้ export → launch ด้วย adb
- Native library calls → ต้อง analyze `.so` ด้วย Ghidra
