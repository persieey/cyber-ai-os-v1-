# Skill: apktool

## Install
```bash
# Kali/Debian
sudo apt install apktool

# Manual
wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
wget https://github.com/iBotPeaches/Apktool/releases/latest/download/apktool_*.jar
chmod +x apktool
```

## Decompile APK
```bash
apktool d app.apk -o output/
# ได้: smali/, res/, assets/, AndroidManifest.xml
```

## Recompile APK
```bash
apktool b output/ -o modified.apk
# Sign ก่อน install:
jarsigner -verbose -keystore my.keystore modified.apk alias_name
```

## Output Structure
```
output/
├── AndroidManifest.xml   ← permissions, activities, services
├── smali/                ← Dalvik bytecode (อ่านได้แต่ยากกว่า jadx)
├── res/
│   ├── values/strings.xml  ← hardcoded strings
│   └── layout/           ← UI layouts
└── assets/               ← raw files, config, databases
```

## Key Files to Check
```bash
cat output/AndroidManifest.xml | grep -E "permission|exported|debuggable|allowBackup"
grep -r "password\|api_key\|secret\|token" output/res/
grep -r "http://" output/res/values/
sqlite3 output/assets/*.db ".tables"  # embedded databases
```
