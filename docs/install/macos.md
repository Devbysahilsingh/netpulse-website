# Install on macOS

**Needs:** macOS 11 Big Sur or newer · a Mac with **Apple Silicon** (M1 or newer) · your [access key](../faq.md#how-do-i-get-an-access-key). Intel Macs can use the CLI built from source for now.

## 1. Download
Download **`NetPulse_0.1.0_aarch64.dmg`** from the [Download page](../download.md#macos).

## 2. Install
1. Open the `.dmg` and drag **NetPulse** into **Applications**.
2. Because NetPulse 0.1.0 is **not signed or notarised by Apple** yet, the first launch shows *"NetPulse cannot be opened because the developer cannot be verified"* (or *"Apple could not verify…"*). To open it once:
    - **macOS 15 Sequoia and newer:** try to open NetPulse, click **Done**. Then open *System Settings → Privacy & Security*, scroll to *Security*, click **Open Anyway** next to NetPulse, and confirm with your password.
    - **macOS 11–14:** in *Finder → Applications*, **right-click (Control-click) NetPulse → Open**, then click **Open**.

    After this, NetPulse opens normally.

!!! warning "Only for the official download"
    Only bypass this warning for the file from the official [GitHub Release](https://github.com/Devbysahilsingh/netpulse-website/releases), and [verify its checksum](../download.md#verify-your-download) if in doubt.

## 3. Launch and connect
1. Paste your **access key**.
2. Check the computer name.
3. Click **Connect**.

Settings go to `~/Library/Application Support/NetPulse/netpulse.toml`, and the key to the `secrets` folder next to it.

## 4. Allow capture
macOS lets only administrators read network traffic (the `/dev/bpf*` devices). Choose one way:

=== "ChmodBPF (recommended for the app)"
    Install Wireshark's free **ChmodBPF** helper: it comes with [Wireshark](https://www.wireshark.org/download.html) (choose *Install ChmodBPF* in the installer). It lets members of the `access_bpf` group capture. Then log out and back in, and **Start protection** works from the app.

=== "Background service (root)"
    Run the monitor as a launchd daemon; the app attaches to it. See the [service guide](../service.md#macos).

## The command line
The CLI is inside the app bundle:
```bash
sudo ln -sf /Applications/NetPulse.app/Contents/MacOS/netpulse /usr/local/bin/netpulse
netpulse status
```
A CLI-only `netpulse-cli_0.1.0_macos_aarch64.tar.gz` is also on the [Download page](../download.md#macos). If macOS blocks the downloaded CLI, run `xattr -d com.apple.quarantine ./netpulse` once.

## Update
Drag the newer NetPulse into Applications and replace the old one. Settings and history are kept.

## Uninstall
1. Remove the service if you installed it: `sudo netpulse service uninstall`.
2. Drag **NetPulse** from Applications to the Bin.
3. Optional: delete `~/Library/Application Support/NetPulse` (settings, key, history).

!!! note "Testing status"
    The macOS package is built and checked automatically for every release. The launchd service lifecycle is tested on macOS in CI. End-to-end testing of the downloaded `.dmg` on a real Mac is part of the release-testing phase; see [Releases](../releases.md).
