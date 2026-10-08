<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/secrets.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Secrets: where they belong

| Secret | Lives | Never in |
|---|---|---|
| AWS credentials (profile `default`) | `%USERPROFILE%\.aws\credentials` on the maintainer's laptop only | the repos, CI, installers, docs, Terraform files |
| Access keys (`np_…`) | the user's own `secrets/agent.token`; yours in `server\.secrets\*.token` (git-ignored) | anywhere else; only their **hashes** go to SSM |
| Access-key hash lists | `server\.secrets\agent_tokens.json` (local), `server\.secrets\aws_agent_tokens.json` → SSM SecureString | git |
| Terraform variables and state | `infrastructure\aws\terraform.tfvars`, `terraform.tfstate*` (git-ignored, local) | git, the website |
| `WEBSITE_RELEASE_TOKEN` (optional) | GitHub → private repo → Settings → Secrets → Actions | files, logs, the public repo |
| Future updater signing key | private-repo Actions secrets + an offline backup | git |
| MLflow / DVC | local only (`mlops/mlflow`, local DVC cache); no credentials exist | – |

Checks:
- **`.gitignore`** covers `server/.secrets/`, `*.token`, `secrets/`, `*.tfvars`, `*.tfstate*`, `*.tfplan`, `.env`.
- **Before every release,** `release.yml` and `publish_release.py` scan every package for key patterns, private keys and Terraform state.
- **Optional history scan:** `& (Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Gitleaks*\gitleaks.exe").FullName git --no-banner --redact .` should end with `no leaks found`.

---
