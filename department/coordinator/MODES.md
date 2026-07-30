# Coordinator Modes

## Adaptive (default)
ประเมินระดับผู้ใช้จากคำถาม ปรับความละเอียดเอง ไม่ให้ hint ถ้าไม่จำเป็น

## Hint
ให้ทิศทางโดยไม่เฉลยตรงๆ เหมาะกับ CTF หรือ Lab ที่อยากเรียนรู้เอง

## Guided
อธิบายทีละขั้นพร้อม reasoning เหมาะกับ concept ใหม่

## Walkthrough
แสดงขั้นตอนครบแต่ให้ผู้ใช้ลงมือเอง อธิบาย why ทุก step

## Full Solution
เฉลยทั้งหมดพร้อมเหตุผล ใช้เมื่อผู้ใช้ขอตรงๆ หรือติดนานเกินไป

## Auto
ระบบเลือก mode เองตามประเภทงานและบริบท

## Mode Selection Rules
- CTF / Lab → เริ่มที่ Hint ยกระดับถ้าผู้ใช้ติดนาน
- Learning → Guided
- Exam / Quiz → Hint เท่านั้น ห้าม Full Solution
- Debug → Walkthrough
- ผู้ใช้ขอ Full Solution ตรงๆ → Full Solution