# Security & privacy

## What leaves your computer
Only what the AI needs, and nothing that identifies you or what you do:

| Sent to the NetPulse AI service | Stays on your computer |
|---|---|
| 62 numeric measurements per connection (durations, packet counts and sizes, timings, TCP flags, window sizes, destination port, protocol) | IP addresses (yours and the other side's) |
| An opaque flow reference (random-looking, to match answers to flows) | App names, website names, DNS names |
| Your computer's name at the service (`agent_id`) and the access key (as a bearer token, over HTTPS) | Your Wi-Fi name, gateway, other devices |
| | Packet contents (NetPulse never reads payloads into its features) |
| | Your history, alerts and reports |

This is **enforced by an automated test**: it runs the real `netpulse` program through a recording proxy and fails if anything other than the allowed fields is sent.

## What is stored locally
In the data folder, readable by your user: a SQLite history of flows and verdicts, alerts, devices, logs, and the queue of flows waiting for the AI. You can delete it at any time ([where it is](desktop.md#where-the-app-keeps-things)).

## Your access key
- Saved in its own file (`secrets/agent.token` next to the settings), never in the settings file and never in logs. The key is never shown again after you enter it.
- Sent only to the NetPulse AI service, over HTTPS, as a bearer token.
- The service keeps only a hash of it.
- If it leaks, ask for it to be revoked and for a new one; nothing else changes.

## What the downloads contain
Every installer and archive contains only:
- the NetPulse programs (desktop app and `netpulse`)
- the public address of the AI service

They contain **no** access keys, **no** cloud credentials (no AWS keys, IAM credentials or similar), **no** model, and **no** private infrastructure information. Every release build is checked automatically for secret-looking content before it is published.

## Unsigned installers
NetPulse is not code-signed yet, so Windows SmartScreen and macOS Gatekeeper warn on first launch ([what you will see](install/index.md#why-do-i-see-a-security-warning)). To make sure your file is the published one, compare its SHA-256 checksum:

=== "Windows (PowerShell)"
    ```powershell
    Get-FileHash .\{{ windows_installer }} -Algorithm SHA256
    ```
=== "Linux"
    ```bash
    sha256sum {{ linux_deb }}
    ```
=== "macOS"
    ```bash
    shasum -a 256 {{ macos_dmg }}
    ```

The value must equal the one in `SHA256SUMS-*.txt` on the [release page](https://github.com/Devbysahilsingh/netpulse-website/releases) and on the [Download page](download.md).

## How NetPulse handles capture
- **Read-only.** It never blocks, changes or injects traffic, and never probes other devices.
- **Safe driver loading on Windows.** Npcap is loaded only from its official system folder, never from `PATH` or the current folder (protection against DLL planting). The legacy WinPcap is never used.
- **Npcap is never bundled or silently installed.** Its licence does not allow it, and installing a network driver should be your decision.
- **Least privilege for the service.** On Linux the service gets only the two capture capabilities and a read-only system.

## Honest results
- **No AI, no verdict.** If the service is unreachable, connections wait; nothing is marked safe or unsafe by guessing.
- **Wrong key, no verdict.** A rejected key is shown plainly.
- **Bad or tampered answers are rejected.** See [AI service](ai-service.md#how-netpulse-protects-you-from-bad-answers).

## Reporting a security problem
Please do not open a public issue for security problems. Contact the maintainer privately through GitHub ([@Devbysahilsingh](https://github.com/Devbysahilsingh)) first.
