# Skill: ScoutSuite (Multi-cloud Security Audit)

## Install
```bash
pip install scoutsuite
```

## Run

**AWS**
```bash
scout aws --access-key-id KEY --secret-access-key SECRET
scout aws  # ถ้ามี ~/.aws/credentials แล้ว
```

**Azure**
```bash
az login
scout azure --cli
```

**GCP**
```bash
gcloud auth application-default login
scout gcp --user-account
```

## Output
```
scoutsuite_results/
└── scoutsuite-report.html   # เปิดใน browser
```

## Report Structure
- **Dashboard** — findings summary by severity
- **Services** — IAM, S3, EC2, RDS, etc.
- **Findings** — specific misconfigurations with evidence
- **Rules** — ดู/แก้ rules ที่ใช้ detect

## Key Findings to Look For
- IAM: Overprivileged users, root usage, no MFA
- S3: Public buckets, no encryption, no versioning
- EC2: Security groups open to 0.0.0.0/0
- RDS: Public instance, no encryption, no backup
- CloudTrail: Logging disabled
- Config: AWS Config not enabled
