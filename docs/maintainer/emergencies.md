<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/emergencies.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Emergencies and recovery

| Emergency | Do this now |
|---|---|
| **An access key leaked** | Revoke it ([Updating AWS](updating-aws.md) *Access keys*). Issue a new one. |
| **An AWS credential leaked** | In the AWS console (personal account), IAM → deactivate and delete the access key immediately. Create a new one; `aws configure --profile default`. Check CloudTrail and the bill. |
| **A secret was committed** | Revoke or rotate it **first**. Then remove it from history (`git filter-repo`, force push) and re-check with gitleaks ([Secrets: where they belong](secrets.md)). If it reached the **public** repo, assume it is compromised, even after deletion. |
| **Costs spike** (budget e-mail) | `aws ce get-cost-and-usage --profile default --time-period Start=<yyyy-mm-01>,End=<tomorrow> --granularity DAILY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE`. Lower the API throttling in `terraform.tfvars` (`api_rate_limit_rps`) and apply. As a last resort, `terraform destroy` stops all charges, but the endpoint URL is then gone for good. |
| **Abusive traffic** on the API | Revoke the agent's key. Lower throttling. Check the logs for the `agent`. |
| **Terraform state lost** | Do not run `apply` (it would try to create duplicates). Restore the backup of `terraform.tfstate`. Without one, re-import each resource (`terraform import <address> <id>`) until `plan` shows no changes. |
| **Laptop lost** | Rotate the AWS keys (console, from another device), revoke `WEBSITE_RELEASE_TOKEN` (GitHub settings), and check the key list in SSM. Code is safe on GitHub, but local secrets (`server\.secrets`, `terraform.tfstate`) must come from your backup. |
| **A release was published broken** | See *Rollback* (app release) and [release-process.md](release-process.md) → *Failed release recovery*. |

---
