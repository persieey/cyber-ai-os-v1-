# Skill: Trivy (Container & Cloud Security Scanner)

## Install
```bash
# Linux
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Windows (scoop)
scoop install trivy
```

## Container Scanning
```bash
# Scan image
trivy image nginx:latest
trivy image --severity HIGH,CRITICAL myapp:1.0

# Scan local Dockerfile
trivy config Dockerfile

# Scan running container
trivy image --input container.tar
```

## Cloud Scanning
```bash
# AWS
trivy cloud --provider aws --region ap-southeast-1

# Azure
trivy cloud --provider azure

# GCP
trivy cloud --provider gcp
```

## IaC Scanning (Terraform, K8s)
```bash
trivy config ./terraform/
trivy config k8s-manifests/
trivy k8s --report summary cluster
```

## Output Formats
```bash
trivy image nginx --format json -o results.json
trivy image nginx --format table   # default
trivy image nginx --format sarif   # GitHub integration
```
