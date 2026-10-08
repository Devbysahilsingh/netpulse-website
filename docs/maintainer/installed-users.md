<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/installed-users.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# What happens to installed users

**There is no automatic updater today.** It is not implemented. NetPulse does not check for, download or announce new versions.

When you publish `v0.1.1`:

| Installed users… | What happens |
|---|---|
| keep running 0.1.0 | Nothing changes for them. 0.1.0 keeps working against the same `/v1` API and model, **as long as the API stays backward-compatible** ([Updating AWS](updating-aws.md)). That is why `/v1` must never break. |
| visit the website | The Download page offers 0.1.1, and the Releases page lists what changed. |
| install 0.1.1 over 0.1.0 (Windows) | The installer recognises the existing install (same `identifier`) and replaces the program files in `%LOCALAPPDATA%\NetPulse`. **Settings, access key and history are kept**, because they live in `%APPDATA%\NetPulse`, which the installer never touches. **If NetPulse is open, the installer closes it** (the monitor saves its last flows) and does not restart it after a silent install; the normal installer offers to run NetPulse on its last page. Verified 2026-10-08 with a real 0.1.0 → 0.1.1 upgrade while monitoring: config and key byte-identical, history kept, footer showed 0.1.1. |
| install a new `.deb` / `.dmg` | Same: program files are replaced, and `~/.config/netpulse` or `~/Library/Application Support/NetPulse` is kept. On Linux, re-run `setcap` on `/usr/bin/netpulse`. |
| use the background service | They must stop it before upgrading (`netpulse service stop`, admin), because Windows cannot replace a running `netpulse.exe`. The service definition points at the same path, so it keeps working after the upgrade: `netpulse service start`. |

Users learn about updates only from the website. If an update is important (security fix, or an API change is coming), announce it on the website's home page (an admonition in `docs/index.md` of the public repo).

## Adding automatic updates later (designed for, not built)
The release layout already fits the Tauri updater:
- stable file names
- one public GitHub Release per version
- a `releases/latest` URL
- one workflow that builds all platforms

Steps, when you decide to build it (a MINOR release):
1. Generate an **updater signing key** (free; this is not code signing): `cargo tauri signer generate -w %USERPROFILE%\.tauri\netpulse-updater.key`.
   - Store the **private key** and its password as private-repo secrets `TAURI_SIGNING_PRIVATE_KEY` / `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`, plus an offline backup.
   - **Never commit the private key.**
2. Add `tauri-plugin-updater` to `desktop/src-tauri`. Put the **public** key and the endpoint `https://github.com/Devbysahilsingh/netpulse-website/releases/latest/download/latest.json` into `tauri.conf.json`. Add an "Update available" banner to Home.
3. In `packaging/tauri.release.json` set `"createUpdaterArtifacts": true`. Make `release.yml` pass the two secrets, and make `publish_release.py` upload the `.sig` files plus a generated `latest.json`.
4. **Test a real update** from the previous version before announcing it. Users of versions without the updater still update manually once.

---
