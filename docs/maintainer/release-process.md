<!-- Generated from Devbysahilsingh/netpulse-ai docs/release-process.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Release process

The exact procedure for every kind of update. Background and the *why* behind each step are in the [maintainer guide](index.md); the one-page tick list is the [release checklist](release-checklist.md).

**Legend:** ✅ **AUTOMATED** (verified) · 🟠 **CURRENTLY MANUAL** · 🔒 **NEEDS APPROVAL** (AWS / cost).
All commands are PowerShell, run from `U:\Projects\NetPulse-AI` unless stated. `$W = "Devbysahilsingh/netpulse-website"` is used below:

```powershell
$W = "Devbysahilsingh/netpulse-website"; $P = "Devbysahilsingh/netpulse-ai"
$env:PATH = "$env:USERPROFILE\.cargo\bin;$env:PATH"; conda activate eda-env
```

---

## The standard app release (used by scenarios A, B, C)

### 1. Prepare
```powershell
git switch main; git pull
git status                                   # clean
```

### 2. Quality gate (all must pass)
```powershell
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
node --check desktop\ui\home.js; node --check desktop\ui\app.js
python -m pytest --ignore=tests/e2e -q -p no:cacheprovider
cargo build --release -p netpulse-cli; python -m pytest tests/e2e -q -p no:cacheprovider
```

### 3. Release notes and version
1. In `CHANGELOG.md` add, at the top under the intro, `## [X.Y.Z] - YYYY-MM-DD` with *Added / Changed / Fixed / Known limitations*. Write it for users. This text becomes the GitHub Release and the website's Releases page.
2. Bump the version everywhere (Cargo.toml, tauri.conf.json, Cargo.lock):
   ```powershell
   python packaging/bump_version.py X.Y.Z
   cargo build --release -p netpulse-cli; .\target\release\netpulse.exe version     # shows X.Y.Z
   ```

### 4. Commit, push, wait for CI ✅
```powershell
git add -A; git commit -m "Release X.Y.Z"; git push origin main
gh run list --repo $P --limit 3                       # the "ci" run for this commit
gh run watch <ci-run-id> --repo $P --exit-status      # must end green
```

### 5. Tag: builds every package ✅
```powershell
git tag vX.Y.Z; git push origin vX.Y.Z
gh run list --repo $P --workflow release.yml --limit 1
gh run watch <release-run-id> --repo $P --exit-status
```
The `release` workflow:
1. **Builds** (jobs `package (windows-x64)`, `package (linux-x64)`, `package (macos-arm64)`):
   - `NetPulse_X.Y.Z_x64-setup.exe`, `netpulse-cli_X.Y.Z_windows_x86_64.zip`
   - `NetPulse_X.Y.Z_amd64.deb`, `NetPulse_X.Y.Z_amd64.AppImage`, `netpulse-cli_X.Y.Z_linux_x86_64.tar.gz`
   - `NetPulse_X.Y.Z_aarch64.dmg`, `netpulse-cli_X.Y.Z_macos_aarch64.tar.gz`
   - `SHA256SUMS-{windows,linux,macos}.txt`
2. **Checks** that the tag equals the version in `Cargo.toml`, and that no package contains secret-looking content.
3. **Publish job:**
   - verifies all 10 files, every checksum and the CHANGELOG section;
   - with the secret `WEBSITE_RELEASE_TOKEN`, it also creates the **draft** release (step 6 happens by itself);
   - without the secret, the run summary says *"Draft release NOT created (CURRENTLY MANUAL)"*.

The run takes 15–35 minutes (Windows is the slowest).

### 6. Create the draft release on the public repo 🟠 CURRENTLY MANUAL
(Automatic once `WEBSITE_RELEASE_TOKEN` is set: [maintainer guide §8](index.md#8-creating-a-new-release-and-publishing-the-installer).)
```powershell
python packaging/publish_release.py vX.Y.Z
```
It downloads the artifacts of the successful release run and verifies names, checksums and secrets. Then it creates the release on `netpulse-website` as a **draft**, which only you can see, with the CHANGELOG section as its text. Running it again refreshes a draft. It refuses to touch a release that is already published.

### 7. Test the draft (this is the real downloadable installer)
```powershell
$T = "$env:TEMP\netpulse-vX.Y.Z"; New-Item -ItemType Directory -Force $T | Out-Null
gh release download vX.Y.Z --repo $W --dir $T --clobber
cd $T; Get-FileHash NetPulse_X.Y.Z_x64-setup.exe -Algorithm SHA256       # equals the line in SHA256SUMS-windows.txt
Select-String SHA256SUMS-windows.txt -Pattern "setup.exe"
```
- **Upgrade test.** With the previous version installed and open, run `NetPulse_X.Y.Z_x64-setup.exe` and click through it, SmartScreen included. Afterwards:
  - the footer shows `NetPulse X.Y.Z · Connected to NetPulse AI · model N`
  - the settings and history are still there
  - `& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" version` prints X.Y.Z
- **Fresh-install test** (when the installer, the first run or Npcap handling changed): on another PC or a fresh Windows user account, go through download → install → first run → key → Start protection.
- **AI test:** `& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" config check` must show all OK, and Home must list apps within a minute.
- Linux/macOS packages: at least check that the files exist and the checksums match. Install them on a real machine when packaging or capture code changed.

If anything fails: fix it, then follow **H. Failed release recovery** (nothing is public yet, so this is cheap).

### 8. Publish ✅ (the site updates itself)
```powershell
gh release edit vX.Y.Z --repo $W --draft=false --latest
gh run list --repo $W --limit 1                       # "pages", triggered by event "release"
gh run watch <pages-run-id> --repo $W --exit-status
curl.exe -s https://devbysahilsingh.github.io/netpulse-website/assets/downloads.json   # "version": "X.Y.Z"
```
Open https://devbysahilsingh.github.io/netpulse-website/download/:
- the version, date and sizes are new
- click the Windows button: the download is the new file

### 9. Afterwards
- `python packaging/sync_website_docs.py`, only if `docs/MAINTAINER.md`, this file or the checklist changed (🟠 CURRENTLY MANUAL).
- Users are **not notified automatically.** If the update matters (security fix), add a notice to the home page of the website (`docs/index.md` in the public repo).

---

## A. Desktop / CLI code update
1. Change the code ([maintainer guide §3–5](index.md#3-making-code-changes)).
2. Steps 2 → 9 above. PATCH if it only fixes things; MINOR if users get something new.
3. If a CLI command or option changed: update `docs/cli.md` in the public repo in the same release (website: scenario F).

## B. Bug-fix release (PATCH, e.g. 0.1.0 → 0.1.1)
1. Fix, plus a test that fails without the fix.
2. `CHANGELOG.md`: `## [0.1.1] - …` with a *Fixed* section.
3. `python packaging/bump_version.py 0.1.1`, then steps 4 → 9.

## C. New feature release (MINOR, e.g. 0.1.1 → 0.2.0)
Same as A, with the version `0.2.0`. Before tagging:
- update the user docs on the website for the feature (scenario F; push the docs **after** publishing, so the site never documents an unreleased feature)
- if the feature needs something new from the API, deploy the **additive** API change first (scenario E), then the app

## D. AI model update only (no app release) 🔒
No version bump and no tag: the installed apps pick up the model by themselves.
```powershell
git status                                                     # clean
dvc repro evaluate
Get-Content reports\metrics\quality_gate.json                  # "passed": true, otherwise STOP
python -m ml.tracking.registry promote --version N --gate reports/metrics/quality_gate.json
python -m ml.export.bundle export --alias production
python -m ml.common.aws preflight
$env:NETPULSE_AWS_ACCOUNT_ID = (Select-String infrastructure\aws\terraform.tfvars -Pattern 'allowed_account_ids\s*=\s*\["(\d{12})"\]').Matches[0].Groups[1].Value
$bucket = terraform -chdir=infrastructure\aws output -raw artifacts_bucket
python -m ml.export.s3_publish publish --version N --bucket $bucket --profile default
$api = terraform -chdir=infrastructure\aws output -raw api_endpoint
curl.exe -s "$api/v1/health"                                   # model_version "N" within ~60 s
```
Afterwards:
- Check the app's footer: *model N*.
- Mention notable model changes on the website (model numbers in `ai-service.md` and `what-is-netpulse.md`).
- Roll back with `python -m ml.export.s3_publish rollback --bucket $bucket --profile default`.

## E. AWS inference / API update 🔒
**Infrastructure** (Terraform settings, throttling, memory):
```powershell
python -m ml.common.aws preflight
terraform -chdir=infrastructure\aws plan -out=change.tfplan    # read it: 0 to destroy; no NAT/ALB/RDS/EC2
terraform -chdir=infrastructure\aws apply change.tfplan
```

**Server code** (`server/`): run its tests, commit, then build and push the image and point the Lambda at it:
```powershell
python -m pytest server -q -p no:cacheprovider
git add -A; git commit -m "Server: …"; git push origin main
python -m ml.common.aws preflight
$ECR = terraform -chdir=infrastructure\aws output -raw ecr_repository_url; $TAG = git rev-parse --short HEAD
aws ecr get-login-password --profile default --region ap-south-1 | docker login --username AWS --password-stdin $ECR.Split('/')[0]
docker build -f server/Dockerfile.lambda -t "${ECR}:${TAG}" .
docker push "${ECR}:${TAG}"
# edit infrastructure\aws\terraform.tfvars: image_tag = "<TAG>"
terraform -chdir=infrastructure\aws plan -out=image.tfplan       # 1 to change
terraform -chdir=infrastructure\aws apply image.tfplan
```

**Verify:** run [maintainer guide §7](index.md#verify-the-api-after-any-aws-change) (`/v1/health`, 401 without a key, `config check`, a Bot capture scan).

**Rules:**
- `/v1` stays backward-compatible: only add optional fields.
- A breaking change needs `/v2` plus an app release.
- Never change the API Gateway (its URL is built into every installed app).

## F. Website / documentation update (no release)
User docs live in the **public** repo:
```powershell
cd U:\Projects\netpulse-website; git pull
# edit docs\*.md. Use {{ version }}, {{ windows_installer }} etc. instead of literal versions or file names
python scripts/gen_downloads.py; mkdocs build --strict        # or: mkdocs serve
git add -A; git commit -m "Docs: …"; git push origin main     # ✅ pages.yml deploys
gh run list --repo $W --limit 1
```
- The **maintainer docs** (this file, the guide, the checklist) live in the **private** repo. Edit them there, commit, then run `python packaging/sync_website_docs.py` (🟠 CURRENTLY MANUAL).
- **Release notes** are edited only in `CHANGELOG.md`. To correct a published release's text: `gh release edit vX.Y.Z --repo $W --notes-file <file>`. The site rebuilds by itself, because the `edited` event triggers `pages.yml`.

## G. Emergency rollback

| What | Command | Effect |
|---|---|---|
| Bad app release is live | `gh release edit vPREVIOUS --repo $W --latest` | the site offers the previous version again within ~1 min (the `edited` event rebuilds it); then fix with a PATCH (B) |
| … and hide the bad one | `gh release edit vBAD --repo $W --prerelease` | it disappears from the Download page; its files stay for anyone already using them |
| Bad model | `python -m ml.export.s3_publish rollback --bucket $bucket --profile default` | the previous model is live within 60 s (needs a `previous` in `active.json`; check with `status`) |
| Bad inference image | `image_tag` = previous tag in `terraform.tfvars` → `plan -out` → `apply` | old server within ~1 min |
| Bad website commit | `git revert <sha>; git push` in `netpulse-website` | the old site within ~1 min |

**Never** delete a published release or re-upload different files under the same version. Checksums, links and users' trust depend on them.

## H. Failed release recovery

| Where it failed | What to do |
|---|---|
| CI (`ci.yml`) red after the release commit | Fix, commit, push. Do not tag until it is green. |
| `release.yml`: version check (tag ≠ Cargo.toml) | Nothing is published. Delete the tag: `git push origin :refs/tags/vX.Y.Z; git tag -d vX.Y.Z`. Bump, commit, tag again. |
| `release.yml`: one package job failed (flaky download, runner issue) | `gh run rerun <run-id> --failed --repo $P` |
| `release.yml`: a real build error | Fix on `main`. Delete the tag (as above) and re-tag the fixed commit. Allowed **only while nothing is published**. |
| Draft created, testing found a bug | Fix, then delete the draft: `gh release delete vX.Y.Z --repo $W --yes --cleanup-tag`. Delete and re-create the private tag on the fixed commit, wait for `release.yml`, then run `publish_release.py vX.Y.Z` again. |
| Published, then a bug was found | Do **not** delete or replace it. Release `vX.Y.Z+1` (B). If the bug is serious, first make the previous release `--latest` (G). |
| `pages.yml` failed after publishing | Read the log (`gh run view <id> --repo $W --log-failed`). Usually a missing checksum line or a broken link. Fix the cause, then `gh workflow run pages.yml --repo $W`. |
| `publish_release.py` says *already PUBLISHED* | Intended: published files are never replaced. Release a new PATCH version. |
