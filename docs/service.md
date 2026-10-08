# Background service

The background service keeps NetPulse protecting your computer without a window open, from boot.

It is **not a separate program**. It is the same `netpulse` command line, running the same monitor as `netpulse start`, registered with your system's own service manager.

| OS | Manager | Runs as | Restarts after a failure |
|---|---|---|---|
| Windows | Service Control Manager: service `NetPulse` ("NetPulse AI"), automatic (delayed) start | LocalSystem | after 10 s, 30 s, 60 s |
| Linux | systemd: `/etc/systemd/system/netpulse.service`, enabled at boot | root, limited to `CAP_NET_RAW` + `CAP_NET_ADMIN`; `ProtectSystem=strict`, `NoNewPrivileges` | `Restart=on-failure` |
| macOS | launchd: `/Library/LaunchDaemons/ai.netpulse.agent.plist`, `RunAtLoad` | root (BPF access) | `KeepAlive` on error |

## Commands

```text
netpulse service install     # administrator / root
netpulse service start
netpulse service status
netpulse service stop
netpulse service restart     # graceful stop, then start
netpulse service uninstall   # local history and reports are kept
```

While the service runs, the other commands still work with the same config: `status`, `monitor`, `threats`, `alerts`, `devices`, `flows`, `report`. `netpulse start` refuses to start a second monitor.

!!! info "The desktop app and the service"
    The window and the service share one monitor and one history **when they use the same settings file**. The window then shows *Protection: On (background service or terminal)*.

    On a single-user computer, the simplest setup is to install the service with the settings the app wrote, e.g. `--config "%APPDATA%\NetPulse\netpulse.toml"` on Windows (from an administrator PowerShell of the same user). On shared computers and servers, use the system-wide locations below; the window then keeps its own, separate history.

## Before you install
1. **A config the service can read.** The service does not run as you, so give it a system-wide config:

    | OS | Recommended config | Key file |
    |---|---|---|
    | Windows | `C:\ProgramData\NetPulse\netpulse.toml` | `C:\ProgramData\NetPulse\secrets\agent.token` |
    | Linux | `/etc/netpulse/netpulse.toml` | `/etc/netpulse/agent.token` |
    | macOS | `/Library/Application Support/NetPulse/netpulse.toml` | next to it, in `secrets/` |

    Create it with `netpulse config init --path <that file>`, then set `agent_id` and `token_file`. The path you install with is recorded in the service definition.
2. **The key must be in a file** (`api.token_file`). Services do not see your shell environment, so `token_env` cannot work; `service install` refuses a config without `token_file`. Restrict the file to administrators/root, e.g. `sudo chmod 600 /etc/netpulse/agent.token`. The key is never written into the service definition.
3. **A capture driver:** Npcap on Windows, libpcap on Linux (macOS has it built in). Check with `netpulse interfaces`.

## Windows
In an **administrator** PowerShell:
```powershell
$np = "$env:LOCALAPPDATA\NetPulse\netpulse.exe"
& $np config init --path C:\ProgramData\NetPulse\netpulse.toml
notepad C:\ProgramData\NetPulse\netpulse.toml      # set agent_id; token_file = "secrets/agent.token"
# put your key into C:\ProgramData\NetPulse\secrets\agent.token
& $np --config C:\ProgramData\NetPulse\netpulse.toml config check
& $np --config C:\ProgramData\NetPulse\netpulse.toml service install
& $np --config C:\ProgramData\NetPulse\netpulse.toml service start
& $np service status
```
The service runs as LocalSystem, so it works even if Npcap was installed in administrators-only mode. On shutdown it uses the Windows **pre-shutdown** notification with a 30-second budget, so open flows are finished and the queue is saved.


## Linux
```bash
sudo mkdir -p /etc/netpulse
sudo netpulse config init --path /etc/netpulse/netpulse.toml
sudo nano /etc/netpulse/netpulse.toml            # agent_id, token_file = "/etc/netpulse/agent.token"
sudo install -m 600 /dev/null /etc/netpulse/agent.token && sudo nano /etc/netpulse/agent.token
sudo netpulse --config /etc/netpulse/netpulse.toml config check
sudo netpulse --config /etc/netpulse/netpulse.toml service install
sudo netpulse --config /etc/netpulse/netpulse.toml service start
systemctl status netpulse
```
Logs: `journalctl -u netpulse`, and `<data_dir>/logs/`.

## macOS
```bash
sudo mkdir -p "/Library/Application Support/NetPulse/secrets"
sudo netpulse config init --path "/Library/Application Support/NetPulse/netpulse.toml"
sudo nano "/Library/Application Support/NetPulse/netpulse.toml"   # agent_id; token_file = "secrets/agent.token"
sudo nano "/Library/Application Support/NetPulse/secrets/agent.token" && sudo chmod 600 "/Library/Application Support/NetPulse/secrets/agent.token"
sudo netpulse --config "/Library/Application Support/NetPulse/netpulse.toml" service install
sudo netpulse --config "/Library/Application Support/NetPulse/netpulse.toml" service start
```
Logs: `<data_dir>/logs/netpulse.log.<date>` and `launchd.{out,err}.log`.

## What the service guarantees
- **Graceful stop.** Stop, shutdown and SIGTERM finish open flows and send them for analysis.
- **Durable queue.** Flows the AI service could not check before a shutdown are saved to `<data_dir>/runtime/pending.jsonl` and sent **first** on the next start. They are never scored locally. A damaged queue file is kept aside (`pending.jsonl.corrupt`) and reported, never silently deleted.
- **Crash recovery.** The manager restarts the service. A killed monitor leaves no stale lock behind.
- **Clear failures.**
    - A missing capture driver, a rejected key or an unsupported schema stops the monitor with an error. The reason is in `netpulse service status` and the log.
    - An unreachable AI service is **not** a failure: flows wait in the bounded queue and are retried.

## Verified
The full lifecycle (install → start → AI outage → stop → start with queue restored → restart → crash → uninstall) is tested automatically on Linux (systemd) and macOS (launchd) for every change, and on Windows with a 22-point test on a real machine.
