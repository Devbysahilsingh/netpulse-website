# Troubleshooting

Start with the built-in check. It tells you what is wrong and what to do:

```text
netpulse config check
netpulse interfaces
netpulse status
```

## Installing

### Windows says "Windows protected your PC"
NetPulse 0.1.0 is not code-signed yet. Click **More info → Run anyway**, but only for the file from the official [release page](https://github.com/Devbysahilsingh/netpulse-website/releases). [Verify the checksum](download.md#verify-your-download) if unsure.

### macOS says the developer cannot be verified
- **macOS 15+:** *System Settings → Privacy & Security → Open Anyway*.
- **macOS 11–14:** right-click the app → **Open** → **Open**.

See [Install on macOS](install/macos.md#2-install).

### Linux: the AppImage does not start
- Make it executable: `chmod +x NetPulse_0.1.0_amd64.AppImage`.
- Some distributions need FUSE 2: `sudo apt install libfuse2`. Or run it with `--appimage-extract-and-run`.

## Capture

### "Npcap is not installed" (Windows)
Install it from the official page **<https://npcap.com/#download>** (administrator; default options), then press **Check again** in the app or run `netpulse interfaces`. NetPulse never installs it for you. You can still analyse saved captures with `netpulse scan --pcap <file>`.

### "Permission denied" / no interfaces
- **Windows:** Npcap was installed with *"Restrict Npcap driver's access to Administrators only"*. Reinstall Npcap without that option, or run NetPulse as administrator, or use the [service](service.md).
- **Linux:** give the CLI capture rights, `sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/netpulse`, then start monitoring with `netpulse start` or the service. Repeat after every update.
- **macOS:** install Wireshark's ChmodBPF helper and log in again, or use the [service](service.md#macos).

### Linux: "libpcap not found"
`sudo apt install libpcap0.8` (Debian/Ubuntu), `sudo dnf install libpcap` (Fedora), `sudo apk add libpcap` (Alpine).

### NetPulse watches the wrong adapter
NetPulse picks the adapter that carries your **default route** (your internet traffic). `netpulse interfaces` shows it with `*` and explains why. If you use a VPN, the VPN adapter may hold the default route. To choose yourself, set `capture.interface` in [the settings](configuration.md#capture-what-is-captured) or use `netpulse start -i "<name>"`.

### Nothing happens / "0 connections"
Flows are checked when they **end**: after the connection closes, or after 120 seconds idle. Give it a minute and browse a little. `netpulse monitor` shows verdicts as they arrive.

## The AI service

### Access key not accepted
Home shows **Access key not accepted**, `status` shows `ACCESS KEY NOT ACCEPTED`, `config check` fails with *"the access key was not accepted"*. Check that:
- the key file (`secrets/agent.token` next to your settings) holds exactly your key, `np_…`, on one line
- `agent_id` in `netpulse.toml` is the computer name your key was issued for
- the key was not revoked

To enter the key again in the app:
1. Close NetPulse.
2. Delete the settings file shown by `netpulse config path`.
3. Open NetPulse again.

### "AI service unavailable"
NetPulse cannot reach the service: no internet, a firewall or proxy blocking `*.execute-api.ap-south-1.amazonaws.com`, or a service outage. Your connections are **kept in the queue** (up to 50,000) and checked automatically when the service is back. Nothing is guessed meanwhile. The first request after a quiet period can take a few seconds (cold start).

### "schema … is not supported by the service"
Your NetPulse is older or newer than the service expects. Install the current version from the [Download page](download.md).

### "invalid response from the service"
The answer did not match what was sent, and NetPulse refused to use it ([why](ai-service.md#how-netpulse-protects-you-from-bad-answers)). Flows stay queued. A proxy that rewrites HTTPS traffic can cause this; otherwise it is temporary.

## The app

### The window is empty or does not open
- **Windows:** NetPulse needs the Microsoft Edge **WebView2 runtime**, which is part of Windows 10/11. If it was removed, the installer downloads it.
- **Linux:** install WebKitGTK 4.1 (`sudo apt install libwebkit2gtk-4.1-0`).

### "Already monitoring"
Only one monitor runs at a time per settings file. Another one (`netpulse start`, the service, or another window) is running. The app attaches to it, or stop it with `netpulse stop`.

## Logs and support
- **Logs:** `<data folder>/logs/netpulse.log.<date>`. On Linux also `journalctl -u netpulse`.
- **Your version:** `netpulse version`.
- When asking for help, include `netpulse --json config check` and `netpulse version`. They never contain your key.
