<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/architecture.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Project architecture

## Two repositories

| Repository | Visibility | Contains | Builds |
|---|---|---|---|
| `Devbysahilsingh/netpulse-ai` (local: `U:\Projects\NetPulse-AI`) | **private** | All source code: the Rust core, CLI, service, desktop app, inference server, ML pipeline, Terraform, tests, `CHANGELOG.md`, this guide | `ci.yml` on every push; `release.yml` on every `v*` tag |
| `Devbysahilsingh/netpulse-website` (local: `U:\Projects\netpulse-website`) | **public** | The website (MkDocs Material), the download-page generator, the copy of this guide, **GitHub Releases with the installers** | `pages.yml` on push and on every release publish/edit/delete |

Users only ever see the public repository: the site at https://devbysahilsingh.github.io/netpulse-website/ and its Releases.

## Parts of the product

| Part | Path (private repo) | Technology | Ships as |
|---|---|---|---|
| Core engine (config, API client, engine, queue, history, alerts) | `core/netpulse-core` | Rust | inside every binary |
| Collector (capture, flows, 62 features, app/website/Wi-Fi context) | `core/netpulse-flow` | Rust (Npcap/libpcap loaded at run time) | inside every binary |
| CLI + background service | `cli` | Rust (`netpulse` binary; `cli/src/service/` = SCM/systemd/launchd) | `netpulse(.exe)` |
| Desktop app | `desktop/src-tauri` (backend), `desktop/ui` (UI) | Tauri 2 + **plain HTML/CSS/JavaScript** (no React, no Node build step) | `netpulse-desktop(.exe)` in the installers |
| Inference service | `server/` | Python FastAPI, run on AWS Lambda via `server/Dockerfile.lambda` | container image in ECR |
| ML pipeline | `ml/`, `mlops/`, `dvc.yaml`, `params.yaml` | Python, DVC, MLflow, XGBoost | model bundles in S3 |
| Infrastructure | `infrastructure/aws` | Terraform | AWS resources ([Updating AWS](updating-aws.md)) |
| Packaging | `packaging/` | Tauri bundler, NSIS, scripts | installers and archives |

## How a release reaches users

```
git tag vX.Y.Z ─► release.yml (private repo)
                   ├─ package (windows-x64)  → NetPulse_X.Y.Z_x64-setup.exe, CLI .zip, SHA256SUMS-windows.txt
                   ├─ package (linux-x64)    → .deb, .AppImage, CLI .tar.gz, SHA256SUMS-linux.txt
                   ├─ package (macos-arm64)  → .dmg, CLI .tar.gz, SHA256SUMS-macos.txt
                   └─ publish                → verifies files + checksums + CHANGELOG section
                                               → DRAFT GitHub Release on netpulse-website
                                                 (automatic only with the WEBSITE_RELEASE_TOKEN secret; see [Creating a release and publishing the installer](releasing.md))
you: test the draft's installer, then publish it
                   └─► pages.yml (public repo) regenerates downloads.json, Download and Releases pages → site live
users: download the new installer and install it over the old one (no auto-update yet; [What happens to installed users](installed-users.md))
```

The client never contains the model. It sends 62 numbers per flow to `POST /v1/predict`. The model is chosen by a pointer file in S3. So **AI model updates need no app release** ([Updating the AI model](updating-ai-model.md)), and **app releases need no AWS change**, as long as the API contract (`/v1`) and the feature schema (`1.0.0`) stay the same.

---
