<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/local-development.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Local development

## One-time setup (Windows, the maintainer's laptop)

| Tool | Version | Check |
|---|---|---|
| Rust (rustup) | stable, ≥ 1.89 | `cargo --version` (if not found: `$env:PATH = "$env:USERPROFILE\.cargo\bin;$env:PATH"`) |
| Tauri CLI | 2.12.1 | `cargo tauri --version` · install: `cargo install tauri-cli --version "2.12.1" --locked` |
| Conda env **`eda-env`** | Python 3.11 | `conda activate eda-env`. **Never create another environment.** Missing packages go into `eda-env`. |
| Node.js | any | `node --version` (only to syntax-check the UI JavaScript) |
| GitHub CLI | ≥ 2.x, logged in as `Devbysahilsingh` | `gh auth status` |
| Npcap | latest | `.\target\release\netpulse.exe interfaces` ends with `Live capture: READY` |
| Docker Desktop | running | only to build the inference image ([Updating AWS](updating-aws.md)) or run Airflow |
| Terraform | ≥ 1.6, **on `PATH`** (winget installs it under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Hashicorp.Terraform_*`; add that folder to your user `PATH`) | only for AWS ([Updating AWS](updating-aws.md)) |
| AWS CLI v2 | profile `default` = the NetPulse-AI account | only for AWS ([Updating AWS](updating-aws.md)) |
| mkdocs-material | 9.6.x, in `eda-env` | only for the website: `pip install "mkdocs-material==9.6.*"` |

The website checkout must sit next to the private repo (`U:\Projects\netpulse-website`); on a new machine: `gh repo clone Devbysahilsingh/netpulse-website U:\Projects\netpulse-website`.

## Build and run

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

## Desktop UI debugging (WebView DevTools)
```powershell
$env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS = "--remote-debugging-port=9222"
cargo run -p netpulse-desktop       # then open edge://inspect in Edge
```

---
