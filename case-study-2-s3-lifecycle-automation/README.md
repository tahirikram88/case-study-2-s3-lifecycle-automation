
# Case Study 2 – Automated S3 Lifecycle Enforcement (Lab)

This repository provides a complete lab environment for testing an automated, serverless S3 lifecycle enforcement solution.

## Features
- Nightly EventBridge trigger (2 AM US/Eastern, DST safe)
- Lambda-based audit and remediation
- DRY_RUN safe testing mode
- Least privilege IAM

## Local Testing
```bash
export DRY_RUN=true
python lambda/main.py
```

## Deployment
```bash
cd terraform
terraform init
terraform apply
```
