# Install on macOS

**Needs:** macOS 11 Big Sur or newer · a Mac with **Apple Silicon** (M1 or newer) · your [access key](../../access.md). Intel Macs can use the CLI built from source for now.

## 1. Download
Download **`{{ macos_dmg }}`** from the [Download page](../../download.md#macos).

## 2. Install
1. Open the `.dmg` and drag **NetPulse** into **Applications**.
2. The first launch is blocked because NetPulse is not notarised yet:

--8<-- "gatekeeper.md"

    After this, NetPulse opens normally.

!!! warning "Only for the official download"
    Only bypass this warning for the file from the official [GitHub Release](https://github.com/Devbysahilsingh/netpulse-website/releases), and [verify its checksum](../../download.md#verify-your-download) if in doubt.

## 3. Launch and connect
1. Paste your **access key** (no key yet? [request AI access]({{ access_form_url }}){ target="_blank" rel="noopener" }).
2. Keep or change the computer name; it is only a label.
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
A CLI-only `{{ macos_cli }}` is also on the [Download page](../../download.md#macos). If macOS blocks the downloaded CLI, run `xattr -d com.apple.quarantine ./netpulse` once.

## Update
See [Updating NetPulse](../updating.md): install the new version over the old one; settings, key and history are kept. There is no automatic updater yet.

## Uninstall
1. Remove the service if you installed it: `sudo netpulse service uninstall`.
2. Drag **NetPulse** from Applications to the Bin.
3. Optional: delete `~/Library/Application Support/NetPulse` (settings, key, history).

!!! note "Testing status"
    The macOS package is built and checked automatically for every release. The launchd service lifecycle is tested on macOS in CI. End-to-end testing of the downloaded `.dmg` on a real Mac is part of the release-testing phase; see [Releases](../../releases.md).
