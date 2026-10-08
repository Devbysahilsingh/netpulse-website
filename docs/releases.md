# Releases

## 0.1.0 (first public release)
**Released:** 2026-10-08 · [Download](download.md) · [GitHub Release](https://github.com/Devbysahilsingh/netpulse-website/releases/tag/v0.1.0)

The first public version of NetPulse AI: one Rust core shared by a desktop app, a command line and a background service, with verdicts from the NetPulse AI service on AWS.

### What's in it
- **Desktop app** with NetPulse Home and the Technical view:
    - Home explains everything in plain words.
    - Real dangers are red; uncertain findings are amber *Worth a look*.
    - Shows apps using the internet, a Wi-Fi check and a Today timeline.
- **First-run setup.**
    - Paste your access key; the computer name and AI service are pre-filled.
    - Npcap is detected on Windows, with the official link and *Check again*.
- **Command line** `netpulse`: `version`, `status`, `interfaces`, `start`, `stop`, `monitor`, `scan`, `threats`, `alerts`, `devices`, `flows`, `report`, `config`, `service`, all with `--json`.
- **Background service** for Windows (SCM), Linux (systemd) and macOS (launchd), with graceful stop, crash recovery and a durable queue.
- **AI service:** model v2 (XGBoost, CSE-CIC-IDS2018), macro-F1 0.867, Bot recall 0.997.
- **Honest by design.** No AI, no verdict; a rejected key is shown plainly; tampered or broken answers are refused.
- **Private by design.** Only 62 anonymous measurements per connection leave the computer.

### Packages

| Platform | Files |
|---|---|
| Windows 10/11 x64 | `NetPulse_0.1.0_x64-setup.exe` (desktop + CLI, per-user install), `netpulse-cli_0.1.0_windows_x86_64.zip` |
| Linux x86_64 | `NetPulse_0.1.0_amd64.deb`, `NetPulse_0.1.0_amd64.AppImage`, `netpulse-cli_0.1.0_linux_x86_64.tar.gz` |
| macOS 11+ Apple Silicon | `NetPulse_0.1.0_aarch64.dmg`, `netpulse-cli_0.1.0_macos_aarch64.tar.gz` |
| Checksums | `SHA256SUMS-windows.txt`, `SHA256SUMS-linux.txt`, `SHA256SUMS-macos.txt` |

### What was tested

| | Windows | Linux | macOS |
|---|---|---|---|
| Unit, integration and end-to-end tests | ✔ | ✔ (CI) | ✔ (CI) |
| Live capture | ✔ real Wi-Fi | ✔ CI | ✔ CI |
| Service lifecycle (install → outage → restart → crash → uninstall) | ✔ real SCM | ✔ systemd (CI) | ✔ launchd (CI) |
| Installer: download → install → first run → monitoring against the AI service | ✔ | Phase 17 | Phase 17 |
| AI: real flows and attacks scored by model v2; outage, wrong key and tampered answers give no verdict | ✔ | via the same core | via the same core |

### Known limitations
- **Not code-signed:** Windows SmartScreen and macOS Gatekeeper warn on first launch ([how to continue](install/index.md#why-do-i-see-a-security-warning)).
- **Invite-only:** you need a personal access key.
- **Infiltration** findings are uncertain and shown as amber *Worth a look* ([why](desktop.md#the-infiltration-limitation)).
- **macOS:** Apple Silicon only.
- **Linux:** live capture is started from the CLI or the service; the desktop app attaches to it ([why](install/linux.md#3-allow-capture)).
- **Desktop app and service** share a monitor only when they use the same settings file.
- The Windows installer does not add `netpulse` to `PATH`.
