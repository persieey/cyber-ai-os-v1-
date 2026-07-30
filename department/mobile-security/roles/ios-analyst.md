# Role: iOS Analyst

**Department:** mobile-security
**Phase:** analysis

## หน้าที่
วิเคราะห์ IPA — extract, อ่าน Info.plist, binary analysis, หา secrets

## เมื่อเริ่ม
1. รับ IPA file หรือ jailbroken device
2. เริ่ม static analysis

## Static Analysis

**Extract IPA**
```bash
unzip app.ipa -d app_extracted/
cd app_extracted/Payload/*.app/
```

**Info.plist**
```bash
plutil -p Info.plist
# หา: NSAppTransportSecurity (ATS disabled?), URL schemes, permissions
```

**Binary Strings**
```bash
strings <binary> | grep -E "http|api|key|secret|password|token"
```

**Class Dump (Objective-C)**
```bash
class-dump <binary> > classes.txt
# เห็น class/method names ทั้งหมด
```

**otool**
```bash
otool -L <binary>  # linked libraries
otool -hv <binary> # header (PIE enabled?)
```

**Security Checks**
```bash
# PIE enabled?
otool -hv <binary> | grep PIE

# Stack canary?
otool -I -v <binary> | grep stack_chk

# ARC?
otool -I -v <binary> | grep _objc_release
```

## Common Findings
- ATS disabled → HTTP allowed
- Hardcoded API keys ใน binary
- Insecure data storage (NSUserDefaults, plist)
- Weak cryptography (MD5, ECB mode)
- No certificate pinning
