---
title: Updating NetPulse
---

# Updating NetPulse

<span class="np-badge np-badge--amber">Automatic updates: currently not available</span>

NetPulse does **not** update itself and does **not** notify you about new versions yet. New versions appear on the [Download page](../download.md) and in the [release notes](../releases.md). The current version is **{{ version }}** (released {{ release_date }}).

## Update steps

--8<-- "update-steps.md"

This was tested with a real upgrade from 0.1.0 while NetPulse was running: the settings file and access key were unchanged, history was kept, and the new version started normally.

## Per system

| | How | Notes |
|---|---|---|
| **Windows** | Run the new `NetPulse_<version>_x64-setup.exe` | Closes NetPulse if it is open. A silent install (`/S`) does not restart it: open it again from the Start menu. |
| **macOS** | Drag the new NetPulse into Applications and replace the old one | Quit NetPulse first. |
| **Linux (.deb)** | `sudo apt install ./NetPulse_<version>_amd64.deb` | Run `sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/netpulse` again: replacing the file removes its capture rights. |
| **Linux (AppImage)** | Replace the file | Make it executable again. |
| **CLI archive** | Replace the `netpulse` binary | Stop the monitor first: `netpulse stop`. |

## Version numbers

NetPulse uses `MAJOR.MINOR.PATCH`:

| Change | Example | What it means for you |
|---|---|---|
| **Patch** | 0.1.0 → 0.1.1 | Fixes only. Safe to install at any time. |
| **Minor** | 0.1.1 → 0.2.0 | New features. Your settings and scripts keep working. |
| **Major** | 0.x → 1.0.0 | May change settings or CLI output. Read the [release notes](../releases.md) first. |

## Do I have to update?

Older versions keep working: every NetPulse talks to the same `/v1` API of the NetPulse AI service, which only ever gains optional additions. AI model improvements happen in the service and reach every version without an update. Updating still gets you the latest fixes, so it is recommended.

## Automatic updates later
An in-app updater is planned for a future version. When it arrives, the release notes will say so, and you will update manually one last time to get it.
