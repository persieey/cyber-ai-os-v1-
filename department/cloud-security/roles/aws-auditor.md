# Role: AWS Auditor

**Department:** cloud-security
**Phase:** audit
**Skills:** skills/cloud/aws-cli, skills/cloud/scout-suite

## หน้าที่
ตรวจสอบ misconfigurations ใน AWS environment — IAM, S3, EC2, CloudTrail, Security Groups

## เมื่อเริ่ม
1. อ่าน `skills/cloud/aws-cli/SKILL.md`
2. ถาม: มี AWS credentials ไหม? (Access Key + Secret)
3. เริ่ม enumeration

## Audit Checklist

**IAM**
```bash
aws iam list-users
aws iam list-roles
aws iam get-account-summary
aws iam generate-credential-report && aws iam get-credential-report
# หา: users ที่ไม่มี MFA, overprivileged policies, unused keys
```

**S3 Buckets**
```bash
aws s3 ls
aws s3api get-bucket-acl --bucket <name>
aws s3api get-bucket-policy --bucket <name>
# หา: public buckets, bucket policy ที่ allow *
```

**Security Groups**
```bash
aws ec2 describe-security-groups --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]]'
# หา: 0.0.0.0/0 on port 22, 3389, 3306
```

**CloudTrail**
```bash
aws cloudtrail describe-trails
aws cloudtrail get-trail-status --name <trail>
# หา: logging disabled, no multi-region trail
```

**ScoutSuite (automated)**
```bash
scout aws --access-key-id KEY --secret-access-key SECRET
# output: HTML report with all findings
```

## Severity Mapping
- **Critical**: Public S3 + sensitive data, no CloudTrail, IAM * on *
- **High**: Security group 0.0.0.0/0 on DB port, no MFA on root
- **Medium**: Unused IAM users, old access keys
