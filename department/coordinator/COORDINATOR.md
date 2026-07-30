# Coordinator Reference

## 1. Routing Table

| Keywords | Department | Default Mode |
|----------|------------|-------------|
| CTF, picoCTF, HTB, THM, flag, challenge | `offensive-security` | Hint |
| Lab, boot2root, Kioptrix, VulnHub, DVWA | `offensive-security` | Hint |
| Pentest, exploit, privesc, rev, PWN | `offensive-security` | Walkthrough |
| SOC, SIEM, alert, log, incident, IR, threat hunt, hardening, blue team | `defensive-security` | Walkthrough |
| Malware, sample, PE, sandbox, IOC, YARA, Sigma, static analysis, dynamic | `malware-analysis` | Walkthrough |
| AWS, Azure, GCP, S3, IAM, CloudTrail, cloud, EC2, bucket, terraform | `cloud-security` | Walkthrough |
| APK, Android, iOS, IPA, Frida, Objection, ADB, mobile, apktool, jadx | `mobile-security` | Walkthrough |
| สอน, อธิบาย, คืออะไร, ทำงานยังไง, เรียน, learning path | `learning` | Guided |
| report, writeup, สรุป, บันทึก, documentation | `reporting` | Auto |
| Unknown | ถาม 1 คำถาม — ห้ามเดา | — |

**Priority:** user ระบุ dept ตรงๆ → ทำตามทันที / ไม่ระบุ → ใช้ตารางด้านบน

## 2. Modes

| Mode | พฤติกรรม |
|------|----------|
| **Hint** | ให้ทิศทางโดยไม่เฉลย เหมาะกับ CTF/Lab ที่อยากเรียนรู้เอง |
| **Guided** | อธิบายทีละขั้นพร้อม reasoning เหมาะกับ concept ใหม่ |
| **Walkthrough** | แสดงขั้นตอนครบ อธิบาย why ทุก step ให้ผู้ใช้ลงมือเอง |
| **Full Solution** | เฉลยทั้งหมดพร้อมเหตุผล ใช้เมื่อผู้ใช้ขอตรงๆ หรือติดนานเกิน |
| **Auto** | เลือก mode เองตาม context |

**Mode Selection Rules**
- CTF / Lab → เริ่มที่ Hint ยกระดับถ้าผู้ใช้ติดนาน
- Debug / error → Walkthrough
- Exam / Quiz → Hint เท่านั้น ห้าม Full Solution
- ผู้ใช้ขอ Full Solution ตรงๆ → Full Solution

## 3. How to Route

1. อ่านตาราง Routing → เลือก Department Agent ใน `.claude/agents/<dept>.md`
2. Department Agent อ่าน manifest → เลือก Role → ดำเนินการ
3. Coordinator ไม่ route ตรงไปยัง Role หรือ Skill
