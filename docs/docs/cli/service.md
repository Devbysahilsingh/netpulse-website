---
title: netpulse service
---

# `netpulse service`

<span class="np-badge np-badge--amber">needs admin / root</span> <span class="np-badge np-badge--green">needs an access key</span> <span class="np-badge np-badge--blue">--json</span>

Runs NetPulse as a background service with the system's own service manager (Windows Service Control Manager, systemd, launchd). Install, uninstall, start, stop and restart need **administrator/root**. Full guide: [Background service](../service.md).

## Syntax and options

--8<-- "cli/service.md"

### `netpulse service install`

--8<-- "cli/service-install.md"

### `netpulse service uninstall`

--8<-- "cli/service-uninstall.md"

### `netpulse service start`

--8<-- "cli/service-start.md"

### `netpulse service stop`

--8<-- "cli/service-stop.md"

### `netpulse service restart`

--8<-- "cli/service-restart.md"

### `netpulse service status`

--8<-- "cli/service-status.md"

## Examples

```text title="Install with the app's settings (Windows, elevated PowerShell)"
netpulse --config "$env:APPDATA\NetPulse\netpulse.toml" service install
netpulse service start
netpulse service status
```

```text title="Linux / macOS"
sudo netpulse --config /etc/netpulse/netpulse.toml service install
sudo netpulse service start
```

## Expected output

```text
NetPulse service
--------------------------------
Manager       Windows Service Control Manager
Installed     yes
State         RUNNING
--------------------------------
```

## JSON output

```json
{ "monitor": null,
  "service": { "detail": null, "installed": false, "manager": "Windows Service Control Manager", "state": "not_installed" } }
```

## Common errors

| You see | What to do |
|---|---|
| `cannot open the service manager: access denied` | Run from an elevated terminal (*Run as administrator*) or with `sudo`. |
| Install refuses the config | The service needs the key in a file (`api.token_file`), not an environment variable. |

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

