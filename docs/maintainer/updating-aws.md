<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/updating-aws.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Updating AWS

## Safety first: never the company account
- **Use only the AWS profile `default`.** It is the personal NetPulse-AI account in `ap-south-1`. **Never use `bold`, `bold*`, `zokkaverse*`** or any company profile.
- Before **every** AWS command:
  ```powershell
  Remove-Item Env:AWS_PROFILE -ErrorAction SilentlyContinue      # nothing may silently redirect the CLI
  python -m ml.common.aws preflight                              # prints "OK: profile 'default' is the NetPulse-AI account <id>"
  aws sts get-caller-identity --profile default --query Account --output text   # same ID as allowed_account_ids in terraform.tfvars
  ```
- **Built-in guards:**
  - Terraform refuses any account other than `allowed_account_ids` in `infrastructure/aws/terraform.tfvars` (git-ignored), and refuses `bold*` / `zokkaverse*` profiles.
  - The Python tools refuse those profiles before loading any credential.

## What exists (23 Terraform resources, region ap-south-1)
Get the real names with `terraform -chdir=infrastructure\aws output`.

| Resource | Terraform name / output | Purpose | Safe to change? | Delete? |
|---|---|---|---|---|
| S3 bucket (+ encryption, versioning, lifecycle, TLS-only policy, public-access block) | `aws_s3_bucket.artifacts` / `artifacts_bucket` | model bundles `models/NetPulse-IDS/<N>/` and the pointer `active.json` | contents: yes, via `s3_publish` only | **NO**: the live model disappears and every client gets 503 |
| ECR repository (+ lifecycle: keeps last 3 images, immutable tags) | `aws_ecr_repository.inference` / `ecr_repository_url` | inference container images | push new tags: yes | **NO**: the Lambda cannot start |
| Lambda function (1024 MB, 15 s, x86_64, no VPC) | `aws_lambda_function.inference` / `lambda_function` | runs the FastAPI server | `image_tag`, memory, timeout: via Terraform | **NO** |
| API Gateway HTTP API + stage + 3 routes (10 req/s, burst 20) | `aws_apigatewayv2_api.http` / `api_endpoint` | the public HTTPS endpoint baked into the apps | throttling: yes | **NEVER**: the endpoint URL is in every installed client; a new API gets a new URL |
| SSM parameter (SecureString) | `aws_ssm_parameter.agent_tokens` / `agent_tokens_parameter` | **hashes** of access keys | its value: yes (adding/revoking keys, [Updating AWS](updating-aws.md) below) | **NO**: every user gets 401 |
| IAM role + policy | `netpulse-dev-inference-lambda` | least-privilege Lambda role | only via Terraform | **NO** |
| CloudWatch log groups (7-day retention) | `/aws/lambda/<lambda_function>`, `/aws/apigateway/netpulse-dev` | logs | retention: yes | harmless but pointless |
| AWS Budget (USD 5/month, email alerts) | `netpulse-dev-monthly` | cost alarm | amount/email: yes | **keep it** |

**Deliberately absent** (they cost money even when idle): NAT gateway, load balancer, RDS, EC2/ECS, WAF, VPC, customer-managed KMS keys, Secrets Manager. **Do not add any of them** without a measured need. The architecture costs about USD 0.05 per month idle (`docs/reports/aws-deployment.md`).

## Deploy or change infrastructure (Terraform) 🔒
```powershell
cd U:\Projects\NetPulse-AI
python -m ml.common.aws preflight
terraform -chdir=infrastructure\aws init
terraform -chdir=infrastructure\aws plan -out=change.tfplan      # READ IT: no NAT/ALB/RDS/EC2; destroy count should be 0
terraform -chdir=infrastructure\aws apply change.tfplan          # applies exactly what you reviewed
terraform -chdir=infrastructure\aws plan                         # afterwards: "No changes"
```
Keep `terraform.tfstate` safe. It is local and git-ignored. Back it up (for example to a private cloud drive) after every apply. If the state is lost, Terraform no longer knows the resources ([Rollback](rollback.md)).

## Deploy a new inference service version (code in `server/`) 🔒
Use this when you change the API server, its dependencies or the Dockerfile. It is not needed for model updates.
```powershell
cd U:\Projects\NetPulse-AI
conda activate eda-env; python -m pytest server -q -p no:cacheprovider      # server tests green
python -m ml.common.aws preflight
$ECR = terraform -chdir=infrastructure\aws output -raw ecr_repository_url
$TAG = git rev-parse --short HEAD                     # commit first: the tag names the code
aws ecr get-login-password --profile default --region ap-south-1 | docker login --username AWS --password-stdin $ECR.Split('/')[0]
docker build -f server/Dockerfile.lambda -t "${ECR}:${TAG}" .
docker push "${ECR}:${TAG}"
# set image_tag = "<TAG>" in infrastructure\aws\terraform.tfvars, then:
terraform -chdir=infrastructure\aws plan -out=image.tfplan            # expect: 1 to change (the Lambda), 0 to destroy
terraform -chdir=infrastructure\aws apply image.tfplan
```
In PowerShell 5.1, if `docker login` fails with error 400, run that line in Git Bash instead.

**Roll back the inference service:** set `image_tag` back to the previous tag, then `plan -out` and `apply` again. List the tags with `aws ecr describe-images --repository-name netpulse-dev-inference --profile default --region ap-south-1 --query 'imageDetails[].imageTags' --output text`. ECR keeps the last 3 images.

**API contract:** `/v1/predict` is used by every installed client and must stay backward-compatible. Add optional fields only. A breaking change needs `/v2` next to `/v1`, a client release that uses it, and `/v1` kept until old clients are gone.

## Inspect logs
```powershell
$fn = terraform -chdir=infrastructure\aws output -raw lambda_function
aws logs tail "/aws/lambda/$fn" --since 30m --follow --profile default --region ap-south-1
aws logs tail "/aws/lambda/$fn" --since 24h --filter-pattern '"status": 401' --profile default --region ap-south-1   # rejected keys
aws logs tail "/aws/lambda/$fn" --since 24h --filter-pattern agent_tokens_unavailable --profile default --region ap-south-1
```
Each request logs one JSON line: `{"event":"request","path":…,"status":…,"ms":…,"agent":…}`. Tokens are never logged.

## Verify the API after any AWS change
```powershell
$api = terraform -chdir=infrastructure\aws output -raw api_endpoint
curl.exe -s "$api/v1/health"                                         # {"status":"ok","model_loaded":true,"model_version":"2",...}
curl.exe -s -o NUL -w "%{http_code}`n" "$api/v1/model"               # 401 (no key) = auth works
& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" config check             # [ OK ] AWS AI service … model vN (uses your key)
& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" scan --pcap data\parity\pcap-bot\capEC2AMAZ-O4EL3NG-172.31.69.29.pcap --config <a scratch config>
```
The Bot capture must give mostly `Bot`, with risk about 90/100. Use a scratch config with its own `data_dir`, so test verdicts don't mix with your real history.

## Access keys (invite-only) 🔒
- **Issue a key:**
  ```powershell
  conda activate eda-env
  python -m ml.common.aws preflight
  $env:NETPULSE_AGENT_TOKENS_FILE = "server\.secrets\aws_agent_tokens.json"        # the AWS hash list (git-ignored)
  python -m server.api.security new-token --agent <their-computer-name> --out server\.secrets\<their-computer-name>.token
  $param = terraform -chdir=infrastructure\aws output -raw agent_tokens_parameter
  aws ssm put-parameter --profile default --region ap-south-1 --name $param --type SecureString --overwrite --value file://server/.secrets/aws_agent_tokens.json
  ```
- **Deliver it** privately (not by public issue or e-mail in clear if avoidable). The user pastes the key on first run. The server identifies them by the key alone; `<their-computer-name>` is only a label (the name in the key list and in the logs), and the computer name entered in the app is not checked against it.
- **Revoke a key:** remove the agent from `server\.secrets\aws_agent_tokens.json`, then run `put-parameter` again. The Lambda re-reads the list within 5 minutes.
- **Never** put a key in the repo, an installer, the website, a GitHub secret or a log.

---
