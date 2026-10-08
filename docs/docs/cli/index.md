---
title: CLI reference
---

# CLI reference

`netpulse` is the command line of NetPulse AI. It uses the same engine as the desktop app and the background service, so all three share one monitor, one history and the same alerts.

## Getting the CLI

**It is included in every desktop package**: you do not need a separate download. A CLI-only archive exists for servers and scripts.

=== "Windows"
    Installed with the desktop app at `%LOCALAPPDATA%\NetPulse\netpulse.exe`. The installer does not change `PATH`, so either use the full path:
    ```powershell
    & "$env:LOCALAPPDATA\NetPulse\netpulse.exe" status
    ```
    or add the folder to your own `PATH` once (new terminals then know `netpulse`):
    ```powershell
    [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:LOCALAPPDATA\NetPulse", "User")
    ```
    CLI only: unzip `{{ windows_cli }}` from the [Download page](../../download.md#windows).

=== "macOS"
    Inside the app bundle. Put it on your `PATH` once:
    ```bash
    sudo ln -sf /Applications/NetPulse.app/Contents/MacOS/netpulse /usr/local/bin/netpulse
    ```
    CLI only: `{{ macos_cli }}` from the [Download page](../../download.md#macos). If macOS blocks it, run `xattr -d com.apple.quarantine ./netpulse` once.

=== "Linux"
    The `.deb` installs it as `/usr/bin/netpulse`, already on `PATH`. For live capture give it capture rights once (and after every update):
    ```bash
    sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/netpulse
    ```
    CLI only (also for AppImage users): `{{ linux_cli }}` from the [Download page](../../download.md#linux):
    ```bash
    tar -xzf {{ linux_cli }} && sudo install -m 755 netpulse /usr/local/bin/netpulse
    ```

The CLI finds the settings the desktop app wrote automatically ([search order](../configuration.md#where-the-settings-file-is)). Monitoring and scans need an [access key](../../access.md).

## Commands

| Command | Purpose |
|---|---|
| [`version`](version.md) | Version, build, feature schema, capture backend |
| [`status`](status.md) | One-screen status: monitor, adapter, AI service, risk |
| [`interfaces`](interfaces.md) | Capture adapters; checks that live capture works |
| [`start`](start.md) | Start monitoring in the background |
| [`stop`](stop.md) | Stop monitoring gracefully |
| [`monitor`](monitor.md) | Live view, or monitor in the foreground |
| [`scan`](scan.md) | Time-boxed capture + analysis, or analyse a capture file |
| [`threats`](threats.md) | Flows the AI labelled as attacks |
| [`alerts`](alerts.md) | Alerts (repeated detections folded together) |
| [`devices`](devices.md) | Hosts seen in the analysed traffic |
| [`flows`](flows.md) | Analysed flows |
| [`report`](report.md) | Write a Markdown or JSON report |
| [`config`](config.md) | `path`, `show`, `init`, `check` |
| [`service`](service.md) | Background service: `install`, `uninstall`, `start`, `stop`, `restart`, `status` |

Every command explains itself: `netpulse --help`, `netpulse <command> --help` or `netpulse help <command>`.

--8<-- "cli/netpulse.md"

## Global options

| Option | Meaning |
|---|---|
| `--config <FILE>` | Use this settings file. Default: the first one found in the [search order](../configuration.md#where-the-settings-file-is). |
| `--json` | Machine-readable JSON on standard output, for every command. Errors are JSON too: `{"error": "...", "help": "..."}`. |
| `-h`, `--help` | Help for the command. |
| `-V`, `--version` | Print the version (`netpulse 0.1.0`). |

## Periods
`--since` takes a number with `s`, `m`, `h` or `d` (`30m`, `24h`, `7d`) or `all`. The default is `24h`. Anything else is refused: `invalid duration unit in "5x" (use s, m, h or d)`.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Error: configuration, capture, access key, … The message says what to do. |
| `2` | Usage error: unknown option or bad value |
| `3` | Nothing could be analysed: the AI service was unavailable. Flows were kept, not guessed. |
| `4` | Partly analysed: some flows could not be checked |

## JSON conventions
- Times are RFC 3339 in UTC (`2026-10-08T13:20:30.722519700+00:00`).
- `observed_at` is when the traffic happened (for a capture file: when it was recorded); `scored_at` is when the AI checked it.
- `label`, `confidence` (0–1) and `risk` (`low`/`medium`/`high`/`critical`) come from the AI service; `model_version` names the model.
- `app` and `host` (program and website) are local context for live capture; they are never sent anywhere.
- `monitor --json` prints JSON Lines (one object per line).
