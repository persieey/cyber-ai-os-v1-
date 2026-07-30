# Workflow: Threat Hunting

## Process
```
Hypothesis → Data Collection → Analysis → Finding → Response
```

## Step 1: Hypothesis
สร้าง hypothesis จาก:
- Threat Intelligence (IOC, TTPs จาก threat feeds)
- MITRE ATT&CK technique ที่ relevant กับ environment
- Anomaly จาก baseline

ตัวอย่าง: "มี adversary ใช้ living-off-the-land binaries (LOLBins) เพื่อ lateral movement"

## Step 2: Data Sources
| Source | เครื่องมือ |
|--------|-----------|
| Logs | Splunk, ELK |
| Network | Wireshark, Zeek, Suricata |
| Endpoint | Sysmon, EDR |
| Memory | Volatility |
| Files | YARA |

## Step 3: Hunt Techniques

**Frequency Analysis** — หาสิ่งที่ rare/unusual
**Stacking** — เปรียบเทียบ across hosts
**Clustering** — group behavior ที่ similar
**Timeline** — reconstruct activity sequence

## Step 4: MITRE ATT&CK Mapping
ทุก finding map กับ ATT&CK technique:
- TA0001 Initial Access
- TA0003 Persistence
- TA0008 Lateral Movement
- TA0010 Exfiltration

## Step 5: Output
- Hunt report: scope, hypothesis, evidence, verdict
- New detection rules (Sigma/Splunk) สำหรับ SOC
