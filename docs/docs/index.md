---
title: Documentation
---

# NetPulse documentation

NetPulse AI watches the network connections of your computer and has an AI model check whether each one looks like an attack. It comes as a **desktop app** (for everyone), a **command line** (for professionals and scripts) and an optional **background service**, all in one package.

**New here?** Read **[First run](first-run.md)**: from download to protected in nine steps.

<div class="np-grid np-grid--3" markdown>
<div class="np-card np-feature" markdown>
### Get started
[First run](first-run.md) · [Request AI access](../access.md) · [Download](../download.md)
</div>
<div class="np-card np-feature" markdown>
### Install
[Windows](install/windows.md) · [macOS](install/macos.md) · [Linux](install/linux.md) · [Updating](updating.md) · [Uninstalling](uninstalling.md)
</div>
<div class="np-card np-feature" markdown>
### Use
[Desktop app](desktop.md) · [Monitoring](monitoring.md) · [Alerts & threats](alerts-threats.md) · [Service](service.md) · [Configuration](configuration.md)
</div>
<div class="np-card np-feature" markdown>
### Command line
[CLI overview](cli/index.md) · [status](cli/status.md) · [start](cli/start.md) · [scan](cli/scan.md) · [threats](cli/threats.md) · [all commands](cli/index.md#commands)
</div>
<div class="np-card np-feature" markdown>
### Understand
[How it works](how-it-works.md) · [AI service](ai-service.md) · [Security & privacy](security-privacy.md)
</div>
<div class="np-card np-feature" markdown>
### Get help
[Troubleshooting](troubleshooting.md) · [FAQ](faq.md) · [Release notes](../releases.md)
</div>
</div>

## What NetPulse does

- **Watches connections.** It reads copies of your computer's network packets and groups them into *flows*; one flow is one conversation between two programs. It never blocks or changes traffic.
- **Asks the AI.** When a flow ends, NetPulse computes 62 measurements of it (durations, packet counts and sizes, timings) and sends **only those numbers** to the NetPulse AI service. The model answers with a label (Benign, Bot, DDoS, …), a confidence and a risk level.
- **Explains the answer.** NetPulse Home says in plain words whether things look safe, which app is affected and what to do. The Technical view and the CLI show every detail.
- **Never makes things up.** Without the AI service, connections wait in a queue and are checked later. Nothing is guessed on your computer.

## What NetPulse is not

- **Not a firewall or antivirus.** It detects and explains; it does not block connections or remove programs.
- **Not a network scanner.** It never probes other devices.
- **Not offline AI.** The model runs in the NetPulse AI service, so it can be improved without updating your app. Analysis needs an [access key](../access.md).

## What it detects

| Family | Examples | NetPulse Home shows |
|---|---|---|
| Bot | A program talking to a botnet's command server | <span class="np-red">May be hacked</span> |
| DoS / DDoS | Floods of traffic | <span class="np-red">Flood of traffic</span> |
| Brute force | Many fast password attempts | <span class="np-red">Password guessing</span> |
| Web attack | SQL injection, cross-site scripting | <span class="np-red">Website attack</span> |
| Infiltration | Intruder-like movement inside a network | <span class="np-amber">Worth a look</span> |

Why Infiltration is amber: [Alerts & threats](alerts-threats.md#the-infiltration-limitation).

## The model
- **Training data:** CSE-CIC-IDS2018, a public dataset of real attack and normal traffic from the Canadian Institute for Cybersecurity (about 12 million labelled flows).
- **Feature fidelity:** NetPulse computes its measurements the same way as the tool that produced that dataset. On the dataset's own captures, 58 of 58 checked features matched.
- **Model in service:** version 2 (XGBoost). Macro-F1 0.867, Bot recall 0.997, false alarms on normal traffic 0.44 %. [More](ai-service.md).

## Platforms

| | Windows 10/11 x64 | Linux x86_64 | macOS 11+ Apple Silicon |
|---|---|---|---|
| Package | Installer (`.exe`) | `.deb`, `.AppImage` | `.dmg` |
| Command line | included, or a `.zip` | included, or a `.tar.gz` | included, or a `.tar.gz` |
| Capture | Npcap (free, installed by you) | libpcap | built in |
| Background service | Windows service | systemd | launchd |

The current version is **{{ version }}**, released {{ release_date }}. Licence: {{ license }}
