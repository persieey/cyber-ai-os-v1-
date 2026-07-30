# Workflow: Android App Analysis

## Process
```
Obtain APK → Static Analysis → Dynamic Analysis → Report
```

## Phase 1: Obtain APK
```bash
# จาก device
adb shell pm list packages | grep <appname>
adb shell pm path <package>
adb pull <path>/base.apk app.apk

# จาก APKPure / APKMirror (CTF)
# หรือ file ที่ได้รับมา
```

## Phase 2: Static Analysis
โหลด `roles/android-analyst.md`

Checklist:
- AndroidManifest.xml
- Hardcoded secrets
- Dangerous permissions
- Exported components

## Phase 3: Dynamic Analysis
โหลด `roles/mobile-pentester.md`

Setup:
1. Burp Suite proxy
2. SSL pinning bypass (Frida/Objection)
3. อ่าน logcat

## Phase 4: Report
- Vulnerability list พร้อม severity
- Steps to reproduce
- Remediation recommendation
- ถ้า CTF → flag location + extraction method
