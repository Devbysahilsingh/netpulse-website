<!-- Generated from Devbysahilsingh/netpulse-ai docs/MAINTAINER.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# NetPulse AI: maintainer guide

The single document for maintaining NetPulse after release. Read it top to bottom once. After that, use the [release checklist](release-checklist.md) and the [release process](release-process.md) every time you ship.

> **Where this file lives.**
> - **Source:** `docs/MAINTAINER.md` in the private repository `Devbysahilsingh/netpulse-ai`.
> - **Public copy:** the website's *Maintainers* section, copied by `python packaging/sync_website_docs.py`.
>
> Edit the source, never the copy. The guide contains no secrets and no private identifiers. Values such as the AWS account ID and bucket name are read from your local, git-ignored files with the commands shown.

**Status legend:** ✅ **AUTOMATED** = verified to run by itself · 🟠 **CURRENTLY MANUAL** = you run the command shown · 🔒 **NEEDS APPROVAL** = changes AWS or costs money.

---

## 1. Project architecture

### Two repositories

| Repository | Visibility | Contains | Builds |
|---|---|---|---|
| `Devbysahilsingh/netpulse-ai` (local: `U:\Projects\NetPulse-AI`) | **private** | All source code: the Rust core, CLI, service, desktop app, inference server, ML pipeline, Terraform, tests, `CHANGELOG.md`, this guide | `ci.yml` on every push; `release.yml` on every `v*` tag |
| `Devbysahilsingh/netpulse-website` (local: `U:\Projects\netpulse-website`) | **public** | The website (MkDocs Material), the download-page generator, the copy of this guide, **GitHub Releases with the installers** | `pages.yml` on push and on every release publish/edit/delete |

Users only ever see the public repository: the site at https://devbysahilsingh.github.io/netpulse-website/ and its Releases.

### Parts of the product

| Part | Path (private repo) | Technology | Ships as |
|---|---|---|---|
| Core engine (config, API client, engine, queue, history, alerts) | `core/netpulse-core` | Rust | inside every binary |
| Collector (capture, flows, 62 features, app/website/Wi-Fi context) | `core/netpulse-flow` | Rust (Npcap/libpcap loaded at run time) | inside every binary |
| CLI + background service | `cli` | Rust (`netpulse` binary; `cli/src/service/` = SCM/systemd/launchd) | `netpulse(.exe)` |
| Desktop app | `desktop/src-tauri` (backend), `desktop/ui` (UI) | Tauri 2 + **plain HTML/CSS/JavaScript** (no React, no Node build step) | `netpulse-desktop(.exe)` in the installers |
| Inference service | `server/` | Python FastAPI, run on AWS Lambda via `server/Dockerfile.lambda` | container image in ECR |
| ML pipeline | `ml/`, `mlops/`, `dvc.yaml`, `params.yaml` | Python, DVC, MLflow, XGBoost | model bundles in S3 |
| Infrastructure | `infrastructure/aws` | Terraform | AWS resources (§7) |
| Packaging | `packaging/` | Tauri bundler, NSIS, scripts | installers and archives |

### How a release reaches users

```
git tag vX.Y.Z ─► release.yml (private repo)
                   ├─ package (windows-x64)  → NetPulse_X.Y.Z_x64-setup.exe, CLI .zip, SHA256SUMS-windows.txt
                   ├─ package (linux-x64)    → .deb, .AppImage, CLI .tar.gz, SHA256SUMS-linux.txt
                   ├─ package (macos-arm64)  → .dmg, CLI .tar.gz, SHA256SUMS-macos.txt
                   └─ publish                → verifies files + checksums + CHANGELOG section
                                               → DRAFT GitHub Release on netpulse-website
                                                 (automatic only with the WEBSITE_RELEASE_TOKEN secret; see §8)
you: test the draft's installer, then publish it
                   └─► pages.yml (public repo) regenerates downloads.json, Download and Releases pages → site live
users: download the new installer and install it over the old one (no auto-update yet; §10)
```

The client never contains the model. It sends 62 numbers per flow to `POST /v1/predict`. The model is chosen by a pointer file in S3. So **AI model updates need no app release** (§6), and **app releases need no AWS change**, as long as the API contract (`/v1`) and the feature schema (`1.0.0`) stay the same.

---

## 2. Local development

### One-time setup (Windows, the maintainer's laptop)

| Tool | Version | Check |
|---|---|---|
| Rust (rustup) | stable, ≥ 1.89 | `cargo --version` (if not found: `$env:PATH = "$env:USERPROFILE\.cargo\bin;$env:PATH"`) |
| Tauri CLI | 2.12.1 | `cargo tauri --version` · install: `cargo install tauri-cli --version "2.12.1" --locked` |
| Conda env **`eda-env`** | Python 3.11 | `conda activate eda-env`. **Never create another environment.** Missing packages go into `eda-env`. |
| Node.js | any | `node --version` (only to syntax-check the UI JavaScript) |
| GitHub CLI | ≥ 2.x, logged in as `Devbysahilsingh` | `gh auth status` |
| Npcap | latest | `.\target\release\netpulse.exe interfaces` ends with `Live capture: READY` |
| Docker Desktop | running | only to build the inference image (§7) or run Airflow |
| Terraform | ≥ 1.6, **on `PATH`** (winget installs it under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Hashicorp.Terraform_*`; add that folder to your user `PATH`) | only for AWS (§7) |
| AWS CLI v2 | profile `default` = the NetPulse-AI account | only for AWS (§7) |
| mkdocs-material | 9.6.x, in `eda-env` | only for the website: `pip install "mkdocs-material==9.6.*"` |

The website build pages are at `U:\Projects\netpulse-website`; clone it next to the private repo: `gh repo clone Devbysahilsingh/netpulse-website U:\Projects\netpulse-website`.

### Build and run

```powershell
cd U:\Projects\NetPulse-AI
cargo build --release -p netpulse-cli          # target\release\netpulse.exe
cargo build -p netpulse-desktop                # target\debug\netpulse-desktop.exe
```

Run against the **real AWS service** with your own key (no local server needed):
```powershell
$env:NETPULSE_CONFIG = "$env:APPDATA\NetPulse\netpulse.toml"      # the config the installed app wrote
.\target\release\netpulse.exe config check
cargo run -p netpulse-desktop
```

Run against a **local** inference service (offline development, or when changing `server/`):
```powershell
conda activate eda-env
$env:NETPULSE_AGENT_TOKENS_FILE = "server\.secrets\agent_tokens.json"
uvicorn server.api.app:factory --factory --host 127.0.0.1 --port 8765
# in another window: a netpulse.toml with url = "http://127.0.0.1:8765" and a token from
#   python -m server.api.security new-token --agent my-laptop --out server\.secrets\my-laptop.token
```

### Desktop UI debugging (WebView DevTools)
```powershell
$env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS = "--remote-debugging-port=9222"
cargo run -p netpulse-desktop       # then open edge://inspect in Edge
```

---

## 3. Making code changes

1. **Branch** (optional for a one-person project, recommended for big changes): `git switch -c fix/short-name`.
2. **Change the code.** Keep one Core: the CLI, the service and the desktop app must share logic through `core/` or `cli/src/commands/` (the desktop links `netpulse_cli`), never duplicate it.
3. **Run the quality gate.** Every command must pass:
   ```powershell
   cargo fmt --all
   cargo clippy --workspace --all-targets -- -D warnings
   cargo test --workspace
   node --check desktop\ui\home.js; node --check desktop\ui\app.js
   conda activate eda-env
   python -m pytest --ignore=tests/e2e -q -p no:cacheprovider
   cargo build --release -p netpulse-cli; python -m pytest tests/e2e -q -p no:cacheprovider
   ```
4. **Commit and push to `main`.** ✅ **AUTOMATED:** `.github/workflows/ci.yml` runs Python tests, end-to-end tests, Rust on Linux/macOS/Windows, the service lifecycle on Linux and macOS, and the desktop build on all three OSes.
   ```powershell
   git add -A; git commit -m "Short summary of the change"; git push origin main
   gh run list --repo Devbysahilsingh/netpulse-ai --limit 3          # find the run id
   gh run watch <run-id> --repo Devbysahilsingh/netpulse-ai --exit-status   # wait for green
   ```
5. **Decide whether it needs a release** (§9 *Versioning*). If yes, follow [the release process](release-process.md).

What must **never** be committed: anything in `server/.secrets/`, `*.token`, `infrastructure/aws/terraform.tfvars`, `*.tfstate*`, `*.tfplan`, `.env`. All of these are already in `.gitignore` (§11).

---

## 4. Updating the desktop app

| What you change | Where | Test |
|---|---|---|
| NetPulse Home screens, wording, colours | `desktop/ui/home.js`, `home.css`, `index.html` | `node --check desktop\ui\home.js`; run the app; check light **and** dark theme |
| Technical view | `desktop/ui/app.js`, `technical.html`, `app.css` | `node --check desktop\ui\app.js`; run the app |
| Data shown on Home (problems, explanations, red/amber levels) | `desktop/src-tauri/src/home.rs` | `cargo test -p netpulse-desktop` |
| Tauri commands, first-run setup | `desktop/src-tauri/src/main.rs` | run the app with no config: `$env:NETPULSE_CONFIG="C:\nonexistent.toml"` shows the first-run screen |
| App name, identifier, window, CSP | `desktop/src-tauri/tauri.conf.json` | **Never change `identifier` (`ai.netpulse.desktop`)**: installers use it to recognise an existing install for upgrades |
| Installer behaviour, metadata | `packaging/tauri.release.json` | build the installer locally (below) and install it |
| Icons | `desktop/src-tauri/icons/` (regenerate: `cargo tauri icon icons\icon.png -o <tmp>` then copy `32x32.png`, `128x128*.png`, `icon.icns`, `icon.ico`) | the macOS build needs `icon.icns` |

Build and test the Windows installer locally before tagging (the same script CI runs):
```powershell
powershell -ExecutionPolicy Bypass -File packaging\build-release.ps1      # → dist\<version>\
Start-Process "dist\<version>\NetPulse_<version>_x64-setup.exe" -ArgumentList "/S" -Wait   # silent per-user install over the old one
& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" version
```

The UI is plain JavaScript loaded from `desktop/ui` by Tauri. There is no `npm install` and no bundler. The CSP forbids inline scripts, so put code in the `.js` files.

---

## 5. Updating the CLI and the service

- **Commands:** `cli/src/commands/*.rs`; argument definitions in `cli/src/main.rs` (clap). After adding or changing a command or option:
  1. `cargo test -p netpulse-cli` (the integration tests in `cli/tests/cli.rs` run the real binary against a mock API)
  2. update the website's `docs/cli.md` (public repo) with the new `--help` text and an example; the help text is the source of truth
  3. if the JSON output changes, note it in `CHANGELOG.md` under *Changed* (scripts depend on it)
- **Service:** `cli/src/service/{windows,systemd,launchd,units}.rs`. Lifecycle tests: Linux and macOS run in CI. Windows needs an elevated shell:
  ```powershell
  powershell -ExecutionPolicy Bypass -File tools\windows-service-test.ps1 -Out svc.log -Python C:\Users\Sahil\.conda\envs\eda-env\python.exe
  ```
- **Exit codes** (0, 1, 2, 3, 4) are a public contract: never renumber them.

---

## 6. Updating the AI model

The model is **not** in any installer. Changing it needs no app release. Model versions are MLflow registry versions (`NetPulse-IDS` v1, v2, …), not app versions.

🔒 Publishing to S3 changes what every user gets: do it deliberately. Cost is negligible (a ~10 MB upload).

```powershell
cd U:\Projects\NetPulse-AI
conda activate eda-env
git status                                   # must be clean: training refuses uncommitted code
dvc repro evaluate                           # data → train → register (@challenger) → evaluate + quality gate
Get-Content reports\metrics\quality_gate.json   # "passed": true ?  If false: STOP. Never loosen a threshold.
python -m ml.tracking.registry promote --version N --gate reports/metrics/quality_gate.json
python -m ml.export.bundle export --alias production        # verified bundle in artifacts\bundles\N
python -m ml.export.bundle activate --version N             # serve it locally first; test with the local server (§2)
```

Publish to AWS (the Lambda picks it up within 60 s; no redeploy):
```powershell
python -m ml.common.aws preflight                           # must print OK for the NetPulse-AI account
$env:NETPULSE_AWS_ACCOUNT_ID = (Select-String infrastructure\aws\terraform.tfvars -Pattern 'allowed_account_ids\s*=\s*\["(\d{12})"\]').Matches[0].Groups[1].Value
$bucket = terraform -chdir=infrastructure\aws output -raw artifacts_bucket
python -m ml.export.s3_publish status  --bucket $bucket --profile default      # what is live now
python -m ml.export.s3_publish publish --version N --bucket $bucket --profile default
```

Verify (§7, *Verify the API*): `/v1/health` must report `"model_version":"N"` within about a minute, and a `netpulse scan --pcap` of a known capture must give sensible labels.

**Rollback a model:** `python -m ml.export.s3_publish rollback --bucket $bucket --profile default` swaps `active` and `previous` in `active.json`. Note that **today `previous` is empty**: v2 is the only model ever published, because v1 failed the gate. So rollback becomes possible after the next publish. The local registry has its own rollback: `python -m ml.tracking.registry rollback`.

**Schema rule:** if a new model needs different features, that is a new feature schema version and needs a client release first (§9, MAJOR or MINOR). Never publish a model trained on a schema the released clients do not send.

---

## 7. Updating AWS

### Safety first: never the company account
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

### What exists (23 Terraform resources, region ap-south-1)
Get the real names with `terraform -chdir=infrastructure\aws output`.

| Resource | Terraform name / output | Purpose | Safe to change? | Delete? |
|---|---|---|---|---|
| S3 bucket (+ encryption, versioning, lifecycle, TLS-only policy, public-access block) | `aws_s3_bucket.artifacts` / `artifacts_bucket` | model bundles `models/NetPulse-IDS/<N>/` and the pointer `active.json` | contents: yes, via `s3_publish` only | **NO**: the live model disappears and every client gets 503 |
| ECR repository (+ lifecycle: keeps last 3 images, immutable tags) | `aws_ecr_repository.inference` / `ecr_repository_url` | inference container images | push new tags: yes | **NO**: the Lambda cannot start |
| Lambda function (1024 MB, 15 s, x86_64, no VPC) | `aws_lambda_function.inference` / `lambda_function` | runs the FastAPI server | `image_tag`, memory, timeout: via Terraform | **NO** |
| API Gateway HTTP API + stage + 3 routes (10 req/s, burst 20) | `aws_apigatewayv2_api.http` / `api_endpoint` | the public HTTPS endpoint baked into the apps | throttling: yes | **NEVER**: the endpoint URL is in every installed client; a new API gets a new URL |
| SSM parameter (SecureString) | `aws_ssm_parameter.agent_tokens` / `agent_tokens_parameter` | **hashes** of access keys | its value: yes (adding/revoking keys, §7 below) | **NO**: every user gets 401 |
| IAM role + policy | `netpulse-dev-inference-lambda` | least-privilege Lambda role | only via Terraform | **NO** |
| CloudWatch log groups (7-day retention) | `/aws/lambda/<lambda_function>`, `/aws/apigateway/netpulse-dev` | logs | retention: yes | harmless but pointless |
| AWS Budget (USD 5/month, email alerts) | `netpulse-dev-monthly` | cost alarm | amount/email: yes | **keep it** |

**Deliberately absent** (they cost money even when idle): NAT gateway, load balancer, RDS, EC2/ECS, WAF, VPC, customer-managed KMS keys, Secrets Manager. **Do not add any of them** without a measured need. The architecture costs about USD 0.05 per month idle (`docs/reports/aws-deployment.md`).

### Deploy or change infrastructure (Terraform) 🔒
```powershell
cd U:\Projects\NetPulse-AI
python -m ml.common.aws preflight
terraform -chdir=infrastructure\aws init
terraform -chdir=infrastructure\aws plan -out=change.tfplan      # READ IT: no NAT/ALB/RDS/EC2; destroy count should be 0
terraform -chdir=infrastructure\aws apply change.tfplan          # applies exactly what you reviewed
terraform -chdir=infrastructure\aws plan                         # afterwards: "No changes"
```
Keep `terraform.tfstate` safe. It is local and git-ignored. Back it up (for example to a private cloud drive) after every apply. If the state is lost, Terraform no longer knows the resources (§13).

### Deploy a new inference service version (code in `server/`) 🔒
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

### Inspect logs
```powershell
$fn = terraform -chdir=infrastructure\aws output -raw lambda_function
aws logs tail "/aws/lambda/$fn" --since 30m --follow --profile default --region ap-south-1
aws logs tail "/aws/lambda/$fn" --since 24h --filter-pattern '"status": 401' --profile default --region ap-south-1   # rejected keys
aws logs tail "/aws/lambda/$fn" --since 24h --filter-pattern agent_tokens_unavailable --profile default --region ap-south-1
```
Each request logs one JSON line: `{"event":"request","path":…,"status":…,"ms":…,"agent":…}`. Tokens are never logged.

### Verify the API after any AWS change
```powershell
$api = terraform -chdir=infrastructure\aws output -raw api_endpoint
curl.exe -s "$api/v1/health"                                         # {"status":"ok","model_loaded":true,"model_version":"2",...}
curl.exe -s -o NUL -w "%{http_code}`n" "$api/v1/model"               # 401 (no key) = auth works
& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" config check             # [ OK ] AWS AI service … model vN (uses your key)
& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" scan --pcap data\parity\pcap-bot\capEC2AMAZ-O4EL3NG-172.31.69.29.pcap --config <a scratch config>
```
The Bot capture must give mostly `Bot`, with risk about 90/100. Use a scratch config with its own `data_dir`, so test verdicts don't mix with your real history.

### Access keys (invite-only) 🔒
- **Issue a key:**
  ```powershell
  conda activate eda-env
  python -m ml.common.aws preflight
  $env:NETPULSE_AGENT_TOKENS_FILE = "server\.secrets\aws_agent_tokens.json"        # the AWS hash list (git-ignored)
  python -m server.api.security new-token --agent <their-computer-name> --out server\.secrets\<their-computer-name>.token
  $param = terraform -chdir=infrastructure\aws output -raw agent_tokens_parameter
  aws ssm put-parameter --profile default --region ap-south-1 --name $param --type SecureString --overwrite --value file://server/.secrets/aws_agent_tokens.json
  ```
- **Deliver it** privately (not by public issue or e-mail in clear if avoidable). The user pastes the key on first run, and their *computer name* must equal `<their-computer-name>`.
- **Revoke a key:** remove the agent from `server\.secrets\aws_agent_tokens.json`, then run `put-parameter` again. The Lambda re-reads the list within 5 minutes.
- **Never** put a key in the repo, an installer, the website, a GitHub secret or a log.

---

## 8. Creating a new release and publishing the installer

Follow [docs/release-process.md](release-process.md); it is the exact procedure. In short:
```powershell
python packaging/bump_version.py X.Y.Z            # Cargo.toml + tauri.conf.json + Cargo.lock
# write the "## [X.Y.Z] - YYYY-MM-DD" section in CHANGELOG.md
git commit -am "Release X.Y.Z"; git push origin main
git tag vX.Y.Z; git push origin vX.Y.Z            # ✅ AUTOMATED: builds every package
python packaging/publish_release.py vX.Y.Z        # 🟠 CURRENTLY MANUAL (until WEBSITE_RELEASE_TOKEN exists): draft release
# test the draft's installer, then:
gh release edit vX.Y.Z --repo Devbysahilsingh/netpulse-website --draft=false --latest   # ✅ site updates itself
```

### Making the draft step automatic (one-time, optional)
`release.yml` already contains the `publish` job. It creates the draft by itself once the private repository has the secret **`WEBSITE_RELEASE_TOKEN`**:
1. GitHub → *Settings → Developer settings → Fine-grained personal access tokens → Generate new token*.
   - **Repository access:** only `Devbysahilsingh/netpulse-website`.
   - **Permissions:** *Contents: Read and write*. Nothing else.
   - **Expiration:** 1 year (put a reminder in your calendar).
2. Store it in the **private** repository (it prompts for the value; never paste it into a file):
   ```powershell
   gh secret set WEBSITE_RELEASE_TOKEN --repo Devbysahilsingh/netpulse-ai
   ```
3. The next tag push creates the draft without `publish_release.py`. Until you have seen that happen once, treat the step as manual.

The token only lets CI write releases on the public repository. It is not a code-signing key or an AWS credential.

---

## 9. Versioning

Semantic versioning, `MAJOR.MINOR.PATCH`, tags `v0.1.0`, `v0.1.1`, `v0.2.0`, `v1.0.0`. The version is **one number for the whole product**: CLI, desktop app, installers, tag. `bump_version.py` keeps them identical; `release.yml` refuses a tag that differs from `Cargo.toml`.

| Increment | When | Examples |
|---|---|---|
| **PATCH** `0.1.0 → 0.1.1` | Bug fixes and wording; no new feature; config, CLI output and JSON stay compatible | fix a crash, fix a typo on Home, dependency security update |
| **MINOR** `0.1.1 → 0.2.0` | New features, still compatible with existing configs, scripts and the `/v1` API | a new CLI command, a new Home screen, a new option with a default |
| **MAJOR** `0.x → 1.0.0`, `1.x → 2.0.0` | Breaking changes: config keys renamed/removed, CLI JSON fields removed, exit codes changed, a new feature schema (needs a new API version), dropping an OS | `1.0.0` = the first release you promise to keep stable |

While the version is `0.x`, a MINOR may contain small breaking changes, but list them under *Changed* in the CHANGELOG. **AI model versions (v1, v2, …) are independent** of app versions. A new model alone is not an app release (§6).

---

## 10. What happens to users who already installed NetPulse

**There is no automatic updater today.** It is not implemented. NetPulse does not check for, download or announce new versions.

When you publish `v0.1.1`:

| Installed users… | What happens |
|---|---|
| keep running 0.1.0 | Nothing changes for them. 0.1.0 keeps working against the same `/v1` API and model, **as long as the API stays backward-compatible** (§7). That is why `/v1` must never break. |
| visit the website | The Download page offers 0.1.1, and the Releases page lists what changed. |
| install 0.1.1 over 0.1.0 (Windows) | The installer recognises the existing install (same `identifier`) and replaces the program files in `%LOCALAPPDATA%\NetPulse`. **Settings, access key and history are kept**, because they live in `%APPDATA%\NetPulse`, which the installer never touches. **If NetPulse is open, the installer closes it** (the monitor saves its last flows) and does not restart it after a silent install; the normal installer offers to run NetPulse on its last page. Verified 2026-10-08 with a real 0.1.0 → 0.1.1 upgrade while monitoring: config and key byte-identical, history kept, footer showed 0.1.1. |
| install a new `.deb` / `.dmg` | Same: program files are replaced, and `~/.config/netpulse` or `~/Library/Application Support/NetPulse` is kept. On Linux, re-run `setcap` on `/usr/bin/netpulse`. |
| use the background service | They must stop it before upgrading (`netpulse service stop`, admin), because Windows cannot replace a running `netpulse.exe`. The service definition points at the same path, so it keeps working after the upgrade: `netpulse service start`. |

Users learn about updates only from the website. If an update is important (security fix, or an API change is coming), announce it on the website's home page (an admonition in `docs/index.md` of the public repo).

### Adding automatic updates later (designed for, not built)
The release layout already fits the Tauri updater:
- stable file names
- one public GitHub Release per version
- a `releases/latest` URL
- one workflow that builds all platforms

Steps, when you decide to build it (a MINOR release):
1. Generate an **updater signing key** (free; this is not code signing): `cargo tauri signer generate -w %USERPROFILE%\.tauri\netpulse-updater.key`.
   - Store the **private key** and its password as private-repo secrets `TAURI_SIGNING_PRIVATE_KEY` / `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`, plus an offline backup.
   - **Never commit the private key.**
2. Add `tauri-plugin-updater` to `desktop/src-tauri`. Put the **public** key and the endpoint `https://github.com/Devbysahilsingh/netpulse-website/releases/latest/download/latest.json` into `tauri.conf.json`. Add an "Update available" banner to Home.
3. In `packaging/tauri.release.json` set `"createUpdaterArtifacts": true`. Make `release.yml` pass the two secrets, and make `publish_release.py` upload the `.sig` files plus a generated `latest.json`.
4. **Test a real update** from the previous version before announcing it. Users of versions without the updater still update manually once.

---

## 11. Secrets: where they belong

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

## 12. Updating the website and documentation

| What | Where | How it goes live |
|---|---|---|
| User docs (install guides, CLI reference, FAQ, …) | public repo `netpulse-website`, `docs/*.md` | push to `main` → ✅ **AUTOMATED** `pages.yml` builds with `--strict` and deploys (~1 min) |
| Download page, Releases page, `downloads.json` | **generated**, never edited: `scripts/gen_downloads.py` reads the latest published release | ✅ **AUTOMATED** on every release publish/edit/delete and every push |
| Version numbers and file names inside pages | placeholders such as `{{ version }}`, `{{ windows_installer }}`, `{{ linux_deb }}`, `{{ macos_dmg }}` (filled by `hooks/release_vars.py`) | automatic: no page edits per release |
| Release notes | private repo `CHANGELOG.md` → the GitHub Release text → the Releases page | with each release |
| This maintainer guide, release process, checklist | private repo `docs/MAINTAINER.md`, `docs/release-process.md`, `docs/release-checklist.md` | 🟠 **CURRENTLY MANUAL:** `python packaging/sync_website_docs.py` (copies, commits and pushes to the public repo) |

Preview locally before pushing:
```powershell
cd U:\Projects\netpulse-website
conda activate eda-env
python scripts/gen_downloads.py          # needs at least one published release
mkdocs serve                             # http://127.0.0.1:8000, live reload
mkdocs build --strict                    # what CI runs: must have no warnings
git add -A; git commit -m "Docs: …"; git push origin main
gh run list --repo Devbysahilsingh/netpulse-website --limit 2        # pages run: success?
```

Rules:
- Never write a private identifier on the public site: no account ID, no bucket or parameter names, no e-mail addresses, no keys.
- Example outputs use the public CSE-CIC-IDS2018 captures, never your own traffic.

---

## 13. Rollback, troubleshooting and emergencies

### Rollback procedures

| What went wrong | Rollback | Time |
|---|---|---|
| A new **app release** is broken | **Never delete or replace a published release's files.** Users and checksums depend on them. Release a fixed PATCH (`vX.Y.Z+1`) the normal way. If users must not download the broken one meanwhile, mark the previous release as latest: `gh release edit vPREVIOUS --repo Devbysahilsingh/netpulse-website --latest`. The site rebuilds and offers it. Optionally change the broken one to a pre-release: `gh release edit vBROKEN --repo Devbysahilsingh/netpulse-website --prerelease`. | minutes |
| A new **model** misbehaves | `python -m ml.export.s3_publish rollback --bucket $bucket --profile default` (needs a `previous`; see §6). Live within 60 s; no client change | 1 minute |
| A new **inference image** fails | Set `image_tag` back to the previous ECR tag, then `terraform plan -out` / `apply` | 5 minutes |
| A **Terraform** change broke something | Revert the `.tf` change in git, then `plan -out` / `apply` | 5–10 minutes |
| **Website** broken | `git revert <commit>` in `netpulse-website`, push. Or re-run the last good deploy: `gh run rerun <run-id> --repo Devbysahilsingh/netpulse-website` | 2 minutes |

### Troubleshooting (maintainer side)

| Symptom | Cause / fix |
|---|---|
| `release.yml` fails at *tag matches the app version* | You tagged without bumping. Delete the tag (`git push origin :refs/tags/vX.Y.Z; git tag -d vX.Y.Z`), bump, commit, re-tag. Allowed only while nothing has been published for that tag. |
| macOS job: `No matching IconType` | `icon.icns` missing from `tauri.conf.json` `bundle.icon` |
| `publish_release.py`: `missing release files` | A package job failed or was skipped; re-run it: `gh run rerun <run-id> --failed --repo Devbysahilsingh/netpulse-ai` |
| `publish_release.py`: `no '## [X.Y.Z]' section` | Write the CHANGELOG section, commit, push. The tag does not need to move, because the script reads the CHANGELOG from your working copy. |
| Pages build fails at `gen_downloads.py` | No published release yet, a missing SHA256SUMS entry, or a broken asset link. The error names it. |
| Pages build fails in `mkdocs build --strict` | A broken link or anchor in `docs/`. The log names the file. |
| Users get 401 | SSM token list wrong or missing: check `aws logs tail … --filter-pattern agent_tokens_unavailable`; restore with `put-parameter` from `server\.secrets\aws_agent_tokens.json` |
| Users get "AI service unavailable" | `curl $api/v1/health`. `503`: no verified model, so check `s3_publish status`. Timeout: check the Lambda logs and the AWS Health Dashboard. |
| Windows build is slow (~35 min) on a fresh cache | It compiles the Tauri CLI once; later runs reuse the cache |

### Emergency and recovery procedures

| Emergency | Do this now |
|---|---|
| **An access key leaked** | Revoke it (§7 *Access keys*). Issue a new one. |
| **An AWS credential leaked** | In the AWS console (personal account), IAM → deactivate and delete the access key immediately. Create a new one; `aws configure --profile default`. Check CloudTrail and the bill. |
| **A secret was committed** | Revoke or rotate it **first**. Then remove it from history (`git filter-repo`, force push) and re-check with gitleaks (§11). If it reached the **public** repo, assume it is compromised, even after deletion. |
| **Costs spike** (budget e-mail) | `aws ce get-cost-and-usage --profile default --time-period Start=<yyyy-mm-01>,End=<tomorrow> --granularity DAILY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE`. Lower the API throttling in `terraform.tfvars` (`api_rate_limit_rps`) and apply. As a last resort, `terraform destroy` stops all charges, but the endpoint URL is then gone for good. |
| **Abusive traffic** on the API | Revoke the agent's key. Lower throttling. Check the logs for the `agent`. |
| **Terraform state lost** | Do not run `apply` (it would try to create duplicates). Restore the backup of `terraform.tfstate`. Without one, re-import each resource (`terraform import <address> <id>`) until `plan` shows no changes. |
| **Laptop lost** | Rotate the AWS keys (console, from another device), revoke `WEBSITE_RELEASE_TOKEN` (GitHub settings), and check the key list in SSM. Code is safe on GitHub, but local secrets (`server\.secrets`, `terraform.tfstate`) must come from your backup. |
| **A release was published broken** | See *Rollback* (app release) and [release-process.md](release-process.md) → *Failed release recovery*. |

---

## 14. Update scenarios at a glance

The exact steps for each are in [release-process.md](release-process.md).

| | Scenario | App release? | AWS change? | Version bump |
|---|---|---|---|---|
| **A** | Desktop/CLI code change | yes | no | PATCH or MINOR |
| **B** | Bug-fix release | yes | no | PATCH |
| **C** | New feature release | yes | only if it needs a new API field (additive) | MINOR |
| **D** | AI model update only | **no** | S3 model publish only | none (model vN) |
| **E** | Inference/API update | only if clients must use something new | image + Terraform | none, unless the clients change |
| **F** | Website/documentation update | no | no | none |
| **G** | Emergency rollback | depends | depends | none, or PATCH |
| **H** | Failed release recovery | yes | no | PATCH if anything was published |
