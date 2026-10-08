# Features

## For everyone: NetPulse Home
- **One clear answer.** "Your computer looks safe", or "Something needs your attention" with the app and what to do.
- **Apps using the internet.** Every app that made connections today, with the websites it talked to. Open an app to see its sites and any problems.
- **Problems in plain words.** Each finding says what was seen, why it matters and what to do, for example: run a full virus scan, change the Wi-Fi password.
- **Two levels.** Real dangers (Bot, DoS/DDoS, password guessing, website attacks) are <span class="np-red">red</span>. Less certain findings (Infiltration) are <span class="np-amber">amber "Worth a look"</span>.
- **Wi-Fi check.** Warns when you are on a Wi-Fi network without a password; lists other devices seen on your network.
- **Calm screen.** Numbers update in place; the page rebuilds only when something you would notice changes.
- **Light and dark** themes, or follow the system.

## For experts: Technical view
- Overview with risk score (0–100), network health, threats, critical findings, flows per second, and the queue.
- **Live flows:** every analysed flow with source, destination, protocol, label, confidence and risk.
- **Alerts:** repeated identical detections folded into one alert with a count.
- **Devices:** hosts seen in the traffic (passive; NetPulse never probes).
- **Reports:** Markdown or JSON reports for any period.
- AI service state, model version and feature-schema version are always visible.

## Command line (`netpulse`)
- Every function of the app, scriptable: `start`, `stop`, `status`, `monitor`, `scan`, `threats`, `alerts`, `devices`, `flows`, `report`, `config`, `interfaces`, `service`, `version`.
- `--json` on every command; [exit codes](cli.md#exit-codes) tell scripts whether everything was analysed.
- Analyse saved captures: `netpulse scan --pcap capture.pcapng`.
- [Full CLI reference](cli.md).

## Background service
- Windows service, systemd unit or launchd daemon, all running the same monitor as `netpulse start`.
- Restarts after a failure. Stops gracefully: open flows are finished and sent.
- Flows the AI could not check before a shutdown are saved and checked first on the next start.
- [Service guide](service.md).

## Detection
- AI verdicts for 7 traffic families from the CSE-CIC-IDS2018 dataset.
- A label, a confidence (0–1) and a risk level (low, medium, high, critical) per flow; a risk score per batch.
- IPv4 and IPv6 traffic, TCP and UDP.
- The network adapter is chosen automatically: the one carrying your internet traffic, never "the first one that is up".

## Reliability and honesty
- **No AI, no verdict.** If the service is unreachable, NetPulse says "AI service unavailable" and queues the flows (up to 50,000 by default). Nothing is scored locally.
- **Wrong key, no verdict.** A rejected access key is shown plainly, and nothing is scored.
- **Tampered answers rejected.** An answer is accepted only if it matches exactly the flows that were sent, with possible values. Otherwise no verdict is stored.
- **One monitor at a time.** The app, CLI and service share one monitor, and the window attaches to whichever is running.

## Privacy
- Only the 62 anonymous measurements and an opaque reference leave the computer.
- IP addresses, app names, website names and the Wi-Fi name stay local. This is enforced by an automated test that records everything sent.
- [Security & privacy](security-privacy.md).

## Platforms

| | Windows 10/11 x64 | Linux x86_64 | macOS 11+ Apple Silicon |
|---|---|---|---|
| Desktop app | Installer (`.exe`) | `.deb`, `.AppImage` | `.dmg` |
| CLI | included + `.zip` | included + `.tar.gz` | included + `.tar.gz` |
| Capture driver | Npcap (free, installed by you) | libpcap (usually present) | built in (BPF) |
| Background service | Windows service | systemd | launchd |
