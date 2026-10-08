# Install on Linux

**Needs:** x86_64 · a desktop with WebKitGTK 4.1 (Ubuntu 22.04+, Debian 12+, Fedora 38+ and similar) · **libpcap** · your [access key](../faq.md#how-do-i-get-an-access-key).

Two packages are offered on the [Download page](../download.md#linux):

| Package | Best for | CLI location |
|---|---|---|
| `NetPulse_0.1.0_amd64.deb` | Debian, Ubuntu, Mint, Pop!_OS | `/usr/bin/netpulse` (on `PATH`) |
| `NetPulse_0.1.0_amd64.AppImage` | Any distribution, no install | inside the AppImage; use the CLI tarball |
| `netpulse-cli_0.1.0_linux_x86_64.tar.gz` | Servers, CLI only | wherever you unpack it |

## 1. Install
=== "Debian / Ubuntu (.deb)"
    ```bash
    sudo apt install ./NetPulse_0.1.0_amd64.deb
    ```
    `apt` also installs the dependencies, including `libpcap0.8`.

=== "AppImage"
    ```bash
    sudo apt install libpcap0.8            # or: sudo dnf install libpcap
    chmod +x NetPulse_0.1.0_amd64.AppImage
    ./NetPulse_0.1.0_amd64.AppImage
    ```

=== "CLI only (.tar.gz)"
    ```bash
    sudo apt install libpcap0.8            # or: sudo dnf install libpcap
    tar -xzf netpulse-cli_0.1.0_linux_x86_64.tar.gz
    sudo install -m 755 netpulse /usr/local/bin/netpulse
    ```

## 2. Launch and connect
Open **NetPulse** from your applications menu.
1. Paste your **access key**.
2. Check the computer name.
3. Click **Connect**.

Settings go to `~/.config/netpulse/netpulse.toml` and the key to `~/.config/netpulse/secrets/agent.token`.

CLI only: `netpulse config init --path ~/.config/netpulse/netpulse.toml`. Then set `agent_id`, and put your key in the file named by `token_file` (`chmod 600`).

## 3. Allow capture
On Linux, reading network traffic needs the `CAP_NET_RAW` and `CAP_NET_ADMIN` capabilities. Give them to the **`netpulse` command line**, not to the desktop app. (GTK, which the desktop app uses, refuses to run with extra capabilities.)

```bash
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/netpulse
netpulse interfaces          # should end with: Live capture: READY
```

## 4. Start monitoring
Start the monitor with the CLI; the desktop app **attaches to it automatically** and shows everything (*Protection: On (background service or terminal)*):

```bash
netpulse start               # runs in the background, uses the settings the app wrote
netpulse status
```

To keep it running across reboots, use the [systemd service](../service.md#linux) instead.

## Update
Install the newer `.deb` the same way, or replace the AppImage. Settings and history in `~/.config/netpulse` are kept. Run the `setcap` command again after updating: replacing the file removes its capabilities.

## Uninstall
```bash
netpulse stop                 # if running
sudo netpulse service uninstall   # if you installed the service
sudo apt remove netpulse
rm -rf ~/.config/netpulse     # optional: settings, key and history
```

!!! note "Testing status"
    The Linux packages are built and checked automatically for every release. The live capture and service lifecycle are tested on Ubuntu in CI. End-to-end testing of the downloaded packages on real Linux desktops is part of the release-testing phase; see [Releases](../releases.md).
