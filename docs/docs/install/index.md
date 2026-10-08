# Installation

Every package contains the **desktop app** and the **`netpulse` command line**. The background service is the same `netpulse` program, so there is nothing extra to install for it.

| | Windows | Linux | macOS |
|---|---|---|---|
| Guide | [Windows](windows.md) | [Linux](linux.md) | [macOS](macos.md) |
| Package | `{{ windows_installer }}` | `.deb` or `.AppImage` | `.dmg` |
| Needs | Windows 10/11 64-bit, [Npcap](https://npcap.com/#download) | x86_64, WebKitGTK 4.1, libpcap | macOS 11+, Apple Silicon |
| Admin rights | Only for Npcap and the optional service | `sudo` for the `.deb`, capture rights | Capture rights (BPF) |

All downloads, with sizes and SHA-256 checksums, are on the [Download page](../../download.md).

## Before you start: your access key
NetPulse is **invite-only** for now. AI analysis needs a personal **access key** (it starts with `np_`). No installer contains a key; you paste yours the first time you open the app.

--8<-- "request-access.md"

## The same four steps everywhere
1. **Download** the package for your system.
2. **Install** it (and, on Windows, Npcap).
3. **Launch** NetPulse and paste your access key.
4. **Start monitoring.** NetPulse picks the adapter that carries your internet traffic.

## Why do I see a security warning?
NetPulse is **not code-signed** yet. Code-signing certificates are paid, and the current releases do not have one. So:
- **Windows** shows *"Windows protected your PC"* (Microsoft Defender SmartScreen) and *Unknown publisher*.
- **macOS** says the app *"cannot be opened because the developer cannot be verified"*.

This is expected for unsigned software. It does not mean the file is harmful, but you should only continue if you downloaded it from the official [GitHub Release](https://github.com/Devbysahilsingh/netpulse-website/releases). If you want to be sure the file was not altered, [compare its SHA-256 checksum](../../download.md#verify-your-download) with the published one. Each guide shows exactly how to continue.
