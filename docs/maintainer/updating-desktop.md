<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/updating-desktop.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Updating the desktop app

| What you change | Where | Test |
|---|---|---|
| NetPulse Home screens, wording, colours | `desktop/ui/home.js`, `home.css`, `index.html` | `node --check desktop\ui\home.js`; run the app; check light **and** dark theme |
| Technical view | `desktop/ui/app.js`, `technical.html`, `app.css` | `node --check desktop\ui\app.js`; run the app |
| Data shown on Home (problems, explanations, red/amber levels) | `desktop/src-tauri/src/home.rs` | `cargo test -p netpulse-desktop` |
| Tauri commands, first-run setup | `desktop/src-tauri/src/main.rs` | run the app with no config: `$env:NETPULSE_CONFIG="C:\nonexistent.toml"` shows the first-run screen |
| App name, identifier, window, CSP | `desktop/src-tauri/tauri.conf.json` | **Never change `identifier` (`ai.netpulse.desktop`)**: installers use it to recognise an existing install for upgrades |
| Installer behaviour, metadata | `packaging/tauri.release.json` | build the installer locally (below) and install it |
| Icons | `desktop/src-tauri/icons/` (regenerate: `cargo tauri icon icons\icon.png -o <tmp>` then copy `32x32.png`, `128x128*.png`, `icon.icns`, `icon.ico`) | the macOS build needs `icon.icns` |

Build and test the Windows installer locally before tagging (the same script CI runs):
```powershell
powershell -ExecutionPolicy Bypass -File packaging\build-release.ps1      # → dist\<version>\
Start-Process "dist\<version>\NetPulse_<version>_x64-setup.exe" -ArgumentList "/S" -Wait   # silent per-user install over the old one
& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" version
```

The UI is plain JavaScript loaded from `desktop/ui` by Tauri. There is no `npm install` and no bundler. The CSP forbids inline scripts, so put code in the `.js` files.

---
