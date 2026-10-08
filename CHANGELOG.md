# Changelog

All notable changes to NetPulse AI releases. Installers are attached to the [GitHub Releases](https://github.com/Devbysahilsingh/netpulse-website/releases) of this repository.

## [0.1.0] - 2026-10-08
First public release.

### Added
- Desktop app (Windows, Linux, macOS):
    - NetPulse Home in plain words (red dangers, amber *Worth a look*)
    - Technical view: overview, live flows, alerts, devices, reports, settings
- First-run setup with a personal access key (invite-only) and Npcap detection with the official download link.
- `netpulse` command line: `version`, `status`, `interfaces`, `start`, `stop`, `monitor`, `scan`, `threats`, `alerts`, `devices`, `flows`, `report`, `config`, `service`; `--json` everywhere.
- Background service: Windows SCM, systemd, launchd. Graceful stop, crash recovery, durable queue.
- NetPulse AI service on AWS (ap-south-1), model v2 (XGBoost, CSE-CIC-IDS2018).
- Verdict safety:
    - no AI, no verdict
    - rejected access keys reported plainly
    - tampered or broken service answers refused
- Packages:
    - Windows NSIS installer (per-user)
    - Linux `.deb` and `.AppImage`
    - macOS `.dmg` (Apple Silicon)
    - CLI archives
    - SHA-256 checksums

### Known limitations
- Installers are not code-signed.
- macOS: Apple Silicon only.
- Infiltration verdicts are low-confidence and shown as *Worth a look*.

[0.1.0]: https://github.com/Devbysahilsingh/netpulse-website/releases/tag/v0.1.0
