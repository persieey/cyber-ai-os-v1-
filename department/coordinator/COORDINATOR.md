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

## 3. How to Spawn

1. เลือก dept + mode จากตาราง Routing ด้านบน
2. อ่าน `workspace/active/session.md` ถ้ามี active session → สรุปเอาเฉพาะที่เกี่ยวข้อง
3. Spawn ด้วย Agent tool โดยใช้ Spawn Prompt Template ด้านล่าง
4. Relay ผลที่ได้กลับให้ user

Coordinator ไม่ route ตรงไปยัง Role หรือ Skill — spawn dept agent เท่านั้น

## 4. Spawn Prompt Template

ส่ง prompt ในรูปแบบนี้ทุกครั้ง — agent เริ่มด้วย fresh context จึงต้องได้รับ context ครบจาก Coordinator:

```
## Request
<user's exact request verbatim>

## Mode
<Hint | Guided | Walkthrough | Full Solution>

## Date
<today's date>

## Environment
<คัดลอก environment section จาก config/ai.yaml มาทั้งหมด>

## Session Context
<สรุปจาก workspace/active/session.md: challenge name, phase, findings สำคัญ>
หรือ "No active session"

## Notes
<ข้อมูลเพิ่มเติมที่เกี่ยวข้อง เช่น ไฟล์ที่ user แนบมา, mode preference ที่ user พูดถึงก่อนหน้า>
```

## 5. Parallel vs Sequential Spawning

**Parallel** — งานที่ไม่มี dependency ต่อกัน → spawn พร้อมกันได้:
```
ตัวอย่าง: "จำลองการโจมตีพร้อมกับตรวจ log"
→ spawn offensive-security  ─┐ พร้อมกัน (ไม่ขึ้นกัน)
→ spawn defensive-security  ─┘
```

**Sequential** — งานที่ต้องรอผลก่อน → spawn ทีละอัน:
```
ตัวอย่าง: "วิเคราะห์ malware แล้วเขียน IOC report"
→ spawn malware-analysis ก่อน (รอให้เสร็จ เขียน output ลง workspace/)
→ จากนั้น spawn reporting (prompt บอกให้อ่าน output จาก workspace/)
```

กฎง่ายๆ: ถาม "agent B ต้องการผลจาก agent A ไหม?" → ถ้าใช่ = sequential
