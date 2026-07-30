# Workflow: Cloud Security Audit

## Process
```
Scope → Enumerate → Find Misconfigs → Exploit (if pentest) → Report
```

## Phase 1: Scope
- Cloud provider: AWS / Azure / GCP / Multi-cloud?
- Account type: Root/Admin access หรือ limited?
- Objective: Audit only หรือ Pentest?

## Phase 2: Automated Scan
```bash
# AWS
scout aws --access-key-id KEY --secret-access-key SECRET -o report/

# Azure
scout azure --cli -o report/

# Multi-cloud
trivy cloud --provider aws
```

## Phase 3: Manual Enumeration
โหลด role ตาม provider:
- AWS → `roles/aws-auditor.md`
- Azure → `roles/azure-auditor.md`

## Phase 4: Exploitation (Pentest mode only)
โหลด `roles/cloud-pentester.md`

## Phase 5: Report
สร้างรายงานตาม severity:
- Critical → แก้ทันที
- High → แก้ใน 1 สัปดาห์
- Medium → แก้ใน 1 เดือน
- Low → ใส่ backlog
