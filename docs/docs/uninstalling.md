---
title: Uninstalling
---

# Uninstalling NetPulse

Uninstalling removes the programs. Your settings, access key and history stay on your computer until you delete them, so a later reinstall continues where you left off.

1. **Stop the background service first**, if you installed it (administrator / root):
   ```text
   netpulse service uninstall
   ```
2. **Remove the program:**

=== "Windows"
    *Settings → Apps → Installed apps → NetPulse → Uninstall*, or run `%LOCALAPPDATA%\NetPulse\uninstall.exe`.

    Optional: delete `%APPDATA%\NetPulse` to remove settings, key and history. Npcap is a separate program; uninstall it from *Installed apps* if nothing else needs it.

=== "macOS"
    Quit NetPulse and drag it from Applications to the Bin.

    Optional: delete `~/Library/Application Support/NetPulse`.

=== "Linux"
    ```bash
    netpulse stop
    sudo apt remove net-pulse      # the Debian package is called net-pulse
    ```
    AppImage: delete the file. Optional: `rm -rf ~/.config/netpulse`.

Your access key stays valid. If you will not use NetPulse again, ask for it to be revoked ([@{{ github_handle }}](https://github.com/Devbysahilsingh) on GitHub).
