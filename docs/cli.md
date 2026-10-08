# CLI reference

`netpulse` is the command line of NetPulse AI. It uses the same engine as the desktop app and the background service, so all three see the same monitor, history and alerts.

```text
netpulse [--config <FILE>] [--json] <COMMAND> [OPTIONS]
```

| Command | Purpose |
|---|---|
| [`version`](#version) | Version, build, feature schema, capture backend |
| [`status`](#status) | One-screen system status |
| [`interfaces`](#interfaces) | List capture interfaces; check that live capture works |
| [`start`](#start) | Start monitoring in the background |
| [`stop`](#stop) | Stop monitoring (gracefully) |
| [`monitor`](#monitor) | Live view of the monitor, or monitor in the foreground |
| [`scan`](#scan) | Time-boxed capture + analysis, or analyse a capture file |
| [`threats`](#threats) | Flows the AI labelled as attacks |
| [`alerts`](#alerts) | Security alerts (repeated detections folded together) |
| [`devices`](#devices) | Hosts seen in the analysed traffic |
| [`flows`](#flows) | Analysed flows |
| [`report`](#report) | Write a Markdown or JSON report |
| [`config`](#config) | `path`, `show`, `init`, `check` |
| [`service`](#service) | Background service: `install`, `uninstall`, `start`, `stop`, `restart`, `status` |
| [`--help`](#help) | Help for any command |

Where is `netpulse`?
- **Windows:** `%LOCALAPPDATA%\NetPulse\netpulse.exe`.
- **Linux (.deb):** `/usr/bin/netpulse`.
- **macOS:** `/Applications/NetPulse.app/Contents/MacOS/netpulse`.

See the [installation guides](install/index.md).

## Global options

| Option | Meaning |
|---|---|
| `--config <FILE>` | Use this config file. Default: the first one found in the [search order](configuration.md#where-the-settings-file-is). |
| `--json` | Machine-readable JSON on standard output, for every command. Errors are JSON too: `{"error": "...", "help": "..."}`. |
| `-h`, `--help` | Help for the command. |
| `-V`, `--version` | Print the version. |

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Error (configuration, capture, access key, …); the message says what to do |
| `2` | Usage error (unknown option, bad value) |
| `3` | Nothing could be analysed: the AI service was unavailable (flows were kept, not guessed) |
| `4` | Partly analysed: some flows could not be checked |

## Periods
`--since` accepts `30m`, `24h`, `7d` (any number with `m`, `h` or `d`) or `all`. The default is `24h`.

---

## version
Shows the NetPulse version, the build commit, the feature-schema version the client sends, and the capture backend.

```text
netpulse version
```

```text title="Output"
NetPulse AI 0.1.0 (2e311a2a0c55)
target          x86_64-pc-windows-msvc
feature schema  1.0.0 (2ec9acdaa6da)
capture backend Npcap
```

```json title="netpulse --json version"
{
  "capture_backend": "Npcap",
  "feature_schema": { "sha256": "2ec9acdaa6da32c7d55a31f08b8427ab87188ec3d9e3ab0751d884771295bc45", "version": "1.0.0" },
  "git_commit": "2e311a2a0c55",
  "name": "NetPulse AI",
  "target": "x86_64-pc-windows-msvc",
  "version": "0.1.0"
}
```

## status
The one-screen summary: is a monitor running, on which adapter, what the AI service says, and the last 5 minutes' threats and risk. When nothing is monitoring, it asks the AI service directly, and also checks that your access key is accepted.

```text
netpulse status
```

```text title="Output (monitoring)"
NetPulse AI
--------------------------------
System        ONLINE
Network       MONITORING (Wi-Fi via Npcap)
Devices       2
Active Flows  114
Threats       0
Critical      0
Risk Score    0/100
AWS AI        CONNECTED (model v2)
--------------------------------
Flows/sec 0.7  |  analysed 63  |  alerts 0
Threats, Critical and Risk Score cover the last 5 minutes.
```

Possible `AWS AI` values:
- `CONNECTED (model v2)`
- `CONNECTING (no batch sent yet)`
- `AWS AI service unavailable (…)`
- `ACCESS KEY NOT ACCEPTED (…)`
- `NOT CONFIGURED (…)`

```json title="netpulse --json status (not monitoring)"
{
  "system": "OFFLINE",
  "liveness": "stopped",
  "network": "IDLE (not monitoring)",
  "devices": 4,
  "aws": { "state": "connected", "detail": "CONNECTED (model v2)", "model_version": "2" },
  "runtime": null
}
```

- `aws.state` is one of `connected`, `connecting`, `unavailable`, `error`, `not_configured`.
- `runtime` holds the running monitor's full status (the same object as `start --json` → `status`).

## interfaces
Lists every capture interface and marks the one NetPulse will use (`*`): the adapter that carries the computer's default route, i.e. your internet traffic. It ends with whether live capture works and, if not, why and what to do.

```text
netpulse interfaces
```

```text title="Output (shortened)"
Capture backend: Npcap
Library: C:\Windows\System32\Npcap\wpcap.dll (Npcap version 1.89, based on libpcap version 1.10.7 (64-bit time_t))
   INTERFACE                  STATE                             ADDRESS          DESCRIPTION
   \Device\NPF_{59D1…}        up, connected, virtual            192.168.112.1    Hyper-V Virtual Ethernet Adapter
*  \Device\NPF_{7619…}        up, connected, wi-fi              192.168.1.20     MediaTek Wi-Fi 6 MT7921 Wireless LAN Card
   \Device\NPF_Loopback       up, loopback                      127.0.0.1        Adapter for loopback traffic capture
   \Device\NPF_{0B7D…}        up, disconnected                  169.254.168.52   Realtek PCIe GbE Family Controller
Capture interface: MediaTek Wi-Fi 6 MT7921 Wireless LAN Card (default route: carries this computer's internet traffic)
Internet route via: 192.168.1.20
Live capture: READY
```

```json title="netpulse --json interfaces (shortened)"
{
  "backend": "Npcap",
  "library": ["C:\\Windows\\System32\\Npcap\\wpcap.dll", "Npcap version 1.89, based on libpcap version 1.10.7 (64-bit time_t)"],
  "interfaces": [
    { "name": "\\Device\\NPF_{7619…}", "description": "MediaTek Wi-Fi 6 MT7921 Wireless LAN Card",
      "loopback": false, "up": true, "wireless": true, "connected": true, "addresses": ["192.168.1.20"], "virtual": false }
  ]
}
```

## start
Starts the monitor **in the background** and returns. The monitor captures live traffic (or reads a capture file), sends the measurements to the AI service, stores the verdicts and raises alerts. Only one monitor runs at a time: the app, the CLI and the service share it.

```text
netpulse start [-i <INTERFACE>] [--filter <BPF>] [--pcap <FILE>]
```

| Option | Meaning |
|---|---|
| `-i`, `--interface <INTERFACE>` | Capture on this adapter (name or description). Default: `capture.interface` from the config, then the adapter that carries the default route. |
| `--filter <FILTER>` | BPF capture filter, tcpdump syntax, e.g. `"not port 22"`. |
| `--pcap <FILE>` | Analyse a `.pcap`/`.pcapng` file instead of live traffic. |

```text title="Example"
netpulse start
```

```text title="Output"
NetPulse started (pid 31720): monitoring \Device\NPF_{7619…} via Npcap [live]
Use `netpulse status`, `netpulse monitor` or `netpulse stop`.
```

```json title="netpulse --json start (shortened)"
{
  "pid": 31720,
  "started": true,
  "status": {
    "state": "running", "mode": "live", "source": "\\Device\\NPF_{7619…} via Npcap", "version": "0.1.0",
    "engine": { "monitoring": true, "aws": { "state": "unknown" }, "flows_seen": 0, "flows_scored": 0, "pending": 0, "risk_score": 0 },
    "error": null, "help": null
  }
}
```

If a monitor is already running: exit code 1, `{"error": "NetPulse is already monitoring (pid 9040)", "help": "Use `netpulse status` to see it, or `netpulse stop` first."}`.

## stop
Stops the monitor gracefully. Open flows are completed and sent for analysis first. Flows the AI service could not check are saved and sent first next time.

```text
netpulse stop [--timeout <SECONDS>] [--force]
```

| Option | Meaning |
|---|---|
| `--timeout <TIMEOUT>` | Seconds to wait for the last flows to be analysed. Default `30`. |
| `--force` | Terminate the monitor if it does not stop in time. |

```text title="Output"
NetPulse stopped. Flows analysed: 1,111, alerts raised: 1.
```

```json title="netpulse --json stop (shortened)"
{ "forced": false, "stopped": true, "was_running": true,
  "status": { "state": "stopped", "engine": { "flows_scored": 1111, "alerts_raised": 1, "pending": 0, "risk_score": 20 } } }
```

If nothing was running: `{"stopped": true, "was_running": false}`.

## monitor
Live view. If a monitor is running (started by the app, `netpulse start` or the service), `monitor` **attaches** to it and shows verdicts as they arrive. Otherwise it monitors in the foreground until **Ctrl-C**.

```text
netpulse monitor [-i <INTERFACE>] [--filter <BPF>] [--pcap <FILE>] [--threats-only]
```

| Option | Meaning |
|---|---|
| `-i`, `--interface`, `--filter`, `--pcap` | As for [`start`](#start), when `monitor` runs its own monitor. |
| `--threats-only` | Show only flows labelled as attacks. |

```text title="Example: netpulse monitor --threats-only --pcap capture.pcap"
NETPULSE AI
Monitoring: ACTIVE   Source: capture.pcap [pcap]   (Ctrl-C stops)
TIME        SOURCE                 DESTINATION            PROTOCOL LABEL        RISK
03-03 02:58 52.15.155.232:80       172.31.69.25:56702     TCP      Infiltration MEDIUM
THREATS: 1   CRITICAL: 0   RISK SCORE: 20/100
Analysed 1,111 flows from capture.pcap in 1s; alerts raised 1.
```

With `--json`, `monitor` prints **one JSON object per line** (JSON Lines). Each verdict is `"type": "flow"`, and the run ends with a `"type": "summary"`:

```json title="netpulse --json monitor --threats-only (one line each)"
{"type":"flow","seq":43027,"flow_ref":"f56674a7329387-1110","observed_at":"2018-03-02T21:28:10.902407+00:00","src_ip":"52.15.155.232","src_port":80,"dst_ip":"172.31.69.25","dst_port":56702,"protocol":6,"label":"Infiltration","confidence":0.227439,"risk":"medium","model_version":"2","app":null,"host":"us-east-2.ec2.archive.ubuntu.com","scored_at":"2026-10-08T13:26:14.219734500+00:00"}
{"type":"summary","report":{"ending":"source_finished","mode":"pcap","source":"capture.pcap","status":{"flows_seen":1111,"flows_scored":1111,"threats":1,"critical":0,"risk_score":20,"aws":{"state":"connected","model_version":"2"}}}}
```

## scan
A one-off check. It either listens live for a fixed time, or analyses a capture file, then prints a summary: verdicts by label, threats and risk. It can also write a report.

```text
netpulse scan [-d <DURATION>] [-i <INTERFACE>] [--filter <BPF>] [--pcap <FILE>] [--report]
```

| Option | Meaning |
|---|---|
| `-d`, `--duration <DURATION>` | How long to listen (live), e.g. `60s`, `5m`. |
| `--pcap <FILE>` | Analyse a `.pcap`/`.pcapng` file instead. |
| `-i`, `--interface`, `--filter` | As for [`start`](#start). |
| `--report` | Also write a report file to the reports folder. |

```text title="Example: netpulse scan --pcap bot-capture.pcap (CSE-CIC-IDS2018 Bot day)"
NetPulse scan
--------------------------------
Source        bot-capture.pcap [pcap]
Result        complete
Flows         40,806
Threats       28,393
Alerts        20
Devices       4
Risk Score    90/100
Model         2
--------------------------------
LABEL         FLOWS
Bot           28,379
Benign        12,413
Infiltration  10
DDoS          4

Threats (latest 20):
TIME         SOURCE               DESTINATION         PROTO  LABEL  CONF  RISK
03-03 01:24  18.219.211.138:8080  172.31.69.29:50909  TCP    Bot    0.99  CRITICAL
…
```

```json title="netpulse --json scan --pcap … (shortened)"
{
  "run": {
    "mode": "pcap", "source": "bot-capture.pcap", "ending": "source_finished",
    "status": { "flows_seen": 40806, "flows_scored": 40806, "threats": 28393, "critical": 26490,
                "risk_score": 90, "network_health": 10, "aws": { "state": "connected", "model_version": "2" } }
  },
  "summary": { "by_label": [["Bot", 28379], ["Benign", 12413], ["Infiltration", 10], ["DDoS", 4]], "by_risk": [["critical", 26490], …] },
  "alerts": [ { "id": 187, "severity": "critical", "label": "Bot", "src_ip": "18.219.211.138", "dst_ip": "172.31.69.29", "dst_port": 50897, "count": 1, … } ],
  "local_devices": 4,
  "report": null
}
```

Exit code `3` if the AI service was unavailable for the whole scan (nothing is guessed), `4` if only part could be analysed.

## threats
Flows the AI labelled as something other than Benign, newest first.

```text
netpulse threats [--since <PERIOD>] [-n <LIMIT>]
```

| Option | Meaning |
|---|---|
| `--since <SINCE>` | Period, default `24h`. |
| `-n`, `--limit <LIMIT>` | Maximum rows, default `50`. |

```text title="Output"
TIME         SOURCE               DESTINATION         PROTO  LABEL         CONF  RISK
03-03 02:55  5.101.40.43:57516    172.31.69.29:3389   TCP    Infiltration  0.20  LOW
03-03 01:24  18.219.211.138:8080  172.31.69.29:50909  TCP    Bot           0.99  CRITICAL
2 threats (newest first; --since 24h, --limit 2).
```

```json title="netpulse --json threats -n 1"
[
  {
    "seq": 40410, "flow_ref": "f566749d00809c-40410",
    "observed_at": "2018-03-02T21:25:19.848604+00:00", "scored_at": "2026-10-08T13:20:33.820962100+00:00",
    "src_ip": "5.101.40.43", "src_port": 57516, "dst_ip": "172.31.69.29", "dst_port": 3389, "protocol": 6,
    "label": "Infiltration", "confidence": 0.202923, "risk": "low", "model_version": "2",
    "app": null, "host": null
  }
]
```

`app` (the program that owned the connection) and `host` (the website name) are filled in for live capture when known. Both stay on your computer.

## alerts
Security alerts. Identical detections repeated within the cooldown are folded into one alert with a `count`.

```text
netpulse alerts [--since <PERIOD>] [-n <LIMIT>] [--severity <LEVEL>]
```

| Option | Meaning |
|---|---|
| `--since`, `-n` | As for [`threats`](#threats). |
| `--severity <SEVERITY>` | Minimum severity: `low`, `medium`, `high`, `critical`. Default `low`. |

```text title="Output"
ID   SEVERITY  LABEL  SOURCE          DESTINATION   PORT   COUNT  FIRST     LAST
187  CRITICAL  Bot    18.219.211.138  172.31.69.29  50897  1      18:50:30  18:50:30
188  CRITICAL  Bot    18.219.211.138  172.31.69.29  50898  1      18:50:30  18:50:30
COUNT = repeated identical detections folded into one alert.
```

```json title="netpulse --json alerts -n 1"
[
  {
    "id": 187, "created_at": "2026-10-08T13:20:30.722519700+00:00", "last_seen": "2026-10-08T13:20:30.722519700+00:00",
    "severity": "critical", "label": "Bot", "src_ip": "18.219.211.138", "dst_ip": "172.31.69.29", "dst_port": 50897,
    "count": 1, "model_version": "2", "sample_flow_ref": "f56673558bb6f0-37709"
  }
]
```

## devices
Hosts seen in the analysed traffic, with flow and threat counts. NetPulse is passive: it never probes the network.

```text
netpulse devices [--since <PERIOD>] [-n <LIMIT>] [--all]
```

| Option | Meaning |
|---|---|
| `--since`, `-n` | As for [`threats`](#threats). |
| `--all` | Include external (internet) hosts, not only local ones. |

```text title="Output"
DEVICE        SCOPE  FLOWS   THREATS  FIRST SEEN  LAST SEEN
172.31.69.29  local  40,766  28,393   18:49:46    18:50:34
172.31.0.2    local  3,008   0        18:49:46    18:50:34
Devices are hosts seen in analysed traffic (passive; NetPulse does not probe the network). Add --all to include external hosts.
```

```json title="netpulse --json devices -n 1"
[ { "ip": "172.31.69.29", "local": true, "flows": 40766, "threats": 28393,
    "first_seen": "2026-10-08T13:19:46.887173900+00:00", "last_seen": "2026-10-08T13:20:34.237572100+00:00" } ]
```

## flows
Every analysed flow, newest first.

```text
netpulse flows [--since <PERIOD>] [-n <LIMIT>] [--label <LABEL>]
```

| Option | Meaning |
|---|---|
| `--since`, `-n` | As for [`threats`](#threats). |
| `--label <LABEL>` | Only this label, e.g. `Bot`, `Benign`, `DDoS`. |

```text title="netpulse flows -n 2 --label Bot"
TIME         SOURCE               DESTINATION         PROTO  LABEL  CONF  RISK
03-03 01:24  18.219.211.138:8080  172.31.69.29:50909  TCP    Bot    0.99  CRITICAL
03-03 01:24  18.219.211.138:8080  172.31.69.29:50908  TCP    Bot    0.99  CRITICAL
2 flows (newest first; --since 24h, --limit 2).
```

JSON: the same objects as [`threats`](#threats).

## report
Writes a report: an overview, verdicts by label and by risk, alerts, threats and local devices.

```text
netpulse report [--since <PERIOD>] [--format md|json] [-o <FILE>]
```

| Option | Meaning |
|---|---|
| `--since <SINCE>` | `24h` (default), `7d`, … or `all`. |
| `--format <FORMAT>` | `md` (Markdown, default) or `json`. |
| `-o`, `--out <OUT>` | Output file. Default: the reports folder, named `netpulse-report-<date>-<time>.<ext>`. |

```text title="Output"
Report written: C:\Users\you\AppData\Roaming\NetPulse\reports\netpulse-report-20261008-185036.md
```

```json title="netpulse --json report"
{ "report": "C:\\Users\\you\\AppData\\Roaming\\NetPulse\\reports\\netpulse-report-20261008-185037.md" }
```

A JSON report (`--format json`) has the keys `generated_at`, `agent_id`, `since`, `summary`, `alerts`, `threats`, `local_devices`.

## config
Configuration helpers. See [Configuration](configuration.md) for every setting.

| Subcommand | Purpose |
|---|---|
| `netpulse config path` | Which config file is used, and the full search order |
| `netpulse config show` | The effective configuration. The token is **never** shown, only where it comes from. |
| `netpulse config init [--path <PATH>] [--force]` | Write a commented `netpulse.toml` template (default `./netpulse.toml`) |
| `netpulse config check` | Check the config, the key file, the folders, the AI service **and that it accepts your key**, and live capture |

```text title="netpulse config check"
[ OK ] config          C:\Users\you\AppData\Roaming\NetPulse\netpulse.toml
[ OK ] agent token     file secrets/agent.token
[ OK ] data folder     C:\Users\you\AppData\Roaming\NetPulse\netpulse-data
[ OK ] reports folder  C:\Users\you\AppData\Roaming\NetPulse\reports
[ OK ] AWS AI service  https://r223uzh3ad.execute-api.ap-south-1.amazonaws.com - model v2, schema 1.0.0
[ OK ] live capture    Npcap Npcap version 1.89, based on libpcap version 1.10.7 (64-bit time_t) (10 interfaces)

Ready.
```

A wrong key gives `[FAIL] AWS AI service … reachable, but the access key was not accepted` and exit code 1.

```json title="netpulse --json config check (shortened)"
{ "checks": [ { "name": "config", "result": "ok", "detail": "…\\netpulse.toml" },
              { "name": "AWS AI service", "result": "ok", "detail": "https://… - model v2, schema 1.0.0" } ] }
```
`result` is `ok`, `warn` or `fail`.

```text title="netpulse config show"
NetPulse configuration
--------------------------------
Config file          C:\Users\you\AppData\Roaming\NetPulse\netpulse.toml
API URL              https://r223uzh3ad.execute-api.ap-south-1.amazonaws.com
Agent ID             my-laptop
Agent token          file secrets/agent.token (set)
Interface            automatic
BPF filter           -
Exclude API traffic  true
Data folder          C:\Users\you\AppData\Roaming\NetPulse\netpulse-data
Reports folder       C:\Users\you\AppData\Roaming\NetPulse\reports
Batch / queue        500 flows / 50,000 pending
Alerts               min medium, cooldown 60s
Risk window          300s
--------------------------------
```

```json title="netpulse --json config show (shortened)"
{ "config_file": "…\\netpulse.toml",
  "api": { "url": "https://r223uzh3ad.execute-api.ap-south-1.amazonaws.com", "agent_id": "my-laptop",
           "token_present": true, "token_source": "file secrets/agent.token", "timeout_s": 10, "retry_attempts": 3 },
  "capture": { "interface": null, "bpf_filter": null, "promiscuous": false, "exclude_api_traffic": true },
  "batching": { "max_flows": 500, "flush_interval_ms": 2000 }, "queue": { "max_pending": 50000 },
  "alerts": { "min_level": "medium", "cooldown_s": 60 }, "risk": { "window_s": 300 },
  "storage": { "data_dir": "…\\netpulse-data", "reports_dir": "…\\reports" } }
```

```json title="netpulse --json config path"
{ "config": "C:\\Users\\you\\AppData\\Roaming\\NetPulse\\netpulse.toml",
  "search_order": ["netpulse.toml", "…\\NetPulse\\netpulse.toml", "…\\NetPulse\\config\\netpulse.toml", "C:\\Users\\you\\AppData\\Roaming\\NetPulse\\netpulse.toml"] }
```

## service
Runs NetPulse as a background service with the system's own service manager. Install, uninstall, start, stop and restart need **administrator/root**. Full guide: [Background service](service.md).

| Subcommand | Purpose |
|---|---|
| `netpulse service install` | Register the service (Windows SCM, systemd, launchd). Requires a config with `api.token_file`. |
| `netpulse service uninstall` | Remove it. Local history and reports are kept. |
| `netpulse service start` / `stop` | Start / gracefully stop it. |
| `netpulse service restart` | Graceful stop, then start. |
| `netpulse service status` | Service-manager state and what the service is monitoring. |

```text title="netpulse service status"
NetPulse service
--------------------------------
Manager       Windows Service Control Manager
Installed     yes
State         RUNNING
--------------------------------
```

```json title="netpulse --json service status (not installed)"
{ "monitor": null,
  "service": { "detail": null, "installed": false, "manager": "Windows Service Control Manager", "state": "not_installed" } }
```

## help
Every command explains itself:

```text
netpulse --help
netpulse <command> --help        e.g. netpulse scan --help
netpulse help <command>
```

```text title="netpulse --help"
NETPULSE AI
Network Intelligence Platform

AI-powered network security: capture flows, analyse them with the NetPulse AI service, alert.

Usage: netpulse [OPTIONS] <COMMAND>

Commands:
  start       Start monitoring (in the background)
  stop        Stop monitoring
  status      Show system status
  monitor     Live monitoring (attaches to the running monitor, or monitors in the foreground)
  scan        Run a passive network scan (time-boxed capture + analysis), or analyse a capture file
  threats     Show detected threats
  alerts      Show security alerts
  devices     Show devices seen on the network
  flows       Show analysed network flows
  report      Generate a report
  config      Configuration
  interfaces  List capture interfaces and check that live capture works
  service     Manage the background service (install, uninstall, start, stop, status)
  version     Show version
  help        Print this message or the help of the given subcommand(s)

Options:
      --config <FILE>  Config file (default: search order shown by `netpulse config path`)
      --json           Machine-readable JSON output
  -h, --help           Print help
  -V, --version        Print version
```

!!! note "About the examples"
    The examples were produced with NetPulse 0.1.0 against the live NetPulse AI service. The attack examples come from the public CSE-CIC-IDS2018 captures (its addresses, such as `172.31.69.29`, belong to that dataset). Local addresses and adapter IDs were shortened.
