<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/index.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Maintainer guide

The single document for maintaining NetPulse after release. Read it top to bottom once. After that, use the [release checklist](release-checklist.md) and the [release process](release-process.md) every time you ship.

> **Where these pages live.**
> - **Source:** `docs/maintainer/` in the private repository `Devbysahilsingh/netpulse-ai`.
> - **Public copy:** the website's *Maintainers* section, copied by `python packaging/sync_website_docs.py`.
>
> Edit the source, never the copy. The pages contain no secrets and no private identifiers.

**Status legend:** ✅ **AUTOMATED** = verified to run by itself · 🟠 **CURRENTLY MANUAL** = you run the command shown · 🔒 **NEEDS APPROVAL** = changes AWS or costs money.

> **Verified end to end with v0.1.0 (2026-10-08).** Each step below was run for real:
> 1. Quality gate green.
> 2. `ci.yml` green.
> 3. Tag push → `release.yml`: 3 package jobs + publish check, all green.
> 4. `publish_release.py v0.1.0` → draft with 10 files.
> 5. `gh release download` from the draft → SHA-256 matched → fresh install as a new user → first run OK → monitoring scored by AWS.
> 6. `gh release edit --draft=false --latest` → `pages.yml` started by the release event → live `downloads.json` showed 0.1.0.
> 7. An anonymous public download was byte-identical.
>
> Also verified: a 0.1.0 → 0.1.1 upgrade over a running install, `bump_version.py` and `sync_website_docs.py`.
>
> **Not yet exercised:**
> - the CI-side draft creation (needs your `WEBSITE_RELEASE_TOKEN`, [Creating a release and publishing the installer](releasing.md))
> - model publishing/rollback on AWS (no second gated model yet)
> - an inference-image redeploy with these exact steps; the same steps were used for the 2026-10-08 deployment

---

## Pages

| Topic | Page |
|---|---|
| How the product and the two repositories fit together | [Architecture](architecture.md) |
| Tools, building, running against AWS or a local service | [Local development](local-development.md) |
| The quality gate and where code goes | [Making code changes](making-changes.md) |
| Desktop UI and backend, installer settings, icons | [Updating the desktop app](updating-desktop.md) |
| Commands, the service, exit codes | [Updating the CLI and the service](updating-cli.md) |
| Train, gate, publish, roll back a model | [Updating the AI model](updating-ai-model.md) |
| Account safety, resources, Terraform, image, logs, verification, access keys | [Updating AWS](updating-aws.md) |
| Tag → build → draft → publish | [Creating a release](releasing.md) · [Release process](release-process.md) · [Release checklist](release-checklist.md) |
| PATCH / MINOR / MAJOR | [Versioning](versioning.md) |
| Upgrades, no auto-updater, future updater | [What happens to installed users](installed-users.md) |
| Where every secret belongs | [Secrets](secrets.md) |
| Site, docs, CLI reference, this guide | [Updating the website](updating-website.md) |
| When something breaks | [Rollback](rollback.md) · [Troubleshooting](troubleshooting.md) · [Emergencies](emergencies.md) |

## Update scenarios at a glance

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
