# Skill: Pacu (AWS Exploitation Framework)

## Install
```bash
pip install pacu
pacu
```

## Basic Usage
```
# Import credentials
set_keys
> Key alias: lab
> Access key: AKIA...
> Secret key: ...

# Who am I
whoami

# List modules
ls

# Run module
run <module_name>
```

## Essential Modules

**Enumeration**
```
run iam__enum_users_roles_policies_groups
run ec2__enum
run s3__enum
run lambda__enum
run secretsmanager__enum
```

**Privilege Escalation**
```
run iam__privesc_scan       # scan for privesc paths
run iam__add_rollback_policy  # add policy to self
```

**Exploitation**
```
run s3__bucket_finder       # brute force bucket names
run ec2__startup_shell_script  # RCE via user data
run lambda__backdoor_new_users  # persistence
```

**Data Exfiltration**
```
run s3__download_bucket     # download all objects
run rds__explore            # RDS snapshot access
```

## Tips
- ใช้ `run <module> --help` ดู options
- Pacu เก็บ session data ใน `~/.local/share/pacu/`
- Always run `iam__enum` ก่อนเพื่อรู้ permission
