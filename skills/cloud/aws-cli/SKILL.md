# Skill: AWS CLI

## Setup
```bash
aws configure
# AWS Access Key ID: [key]
# AWS Secret Access Key: [secret]
# Default region: ap-southeast-1
# Default output format: json
```

## Essential Commands

**Identity**
```bash
aws sts get-caller-identity   # who am I?
aws iam get-user              # current user details
```

**IAM Enumeration**
```bash
aws iam list-users
aws iam list-groups
aws iam list-roles
aws iam list-policies --scope Local
aws iam get-user-policy --user-name <user> --policy-name <policy>
aws iam list-attached-user-policies --user-name <user>
```

**S3**
```bash
aws s3 ls                              # list buckets
aws s3 ls s3://<bucket>/               # list objects
aws s3 cp s3://<bucket>/file.txt .     # download
aws s3api get-bucket-acl --bucket <b>  # bucket ACL
aws s3api get-bucket-policy --bucket <b>
```

**EC2**
```bash
aws ec2 describe-instances
aws ec2 describe-security-groups
aws ec2 describe-vpcs
```

**Secrets / SSM**
```bash
aws secretsmanager list-secrets
aws secretsmanager get-secret-value --secret-id <name>
aws ssm get-parameters-by-path --path / --recursive --with-decryption
```

**CloudTrail**
```bash
aws cloudtrail describe-trails
aws cloudtrail lookup-events --max-results 50
```

## Output Formatting
```bash
aws <cmd> --query 'Users[].UserName' --output table
aws <cmd> --output json | jq '.[]'
```
