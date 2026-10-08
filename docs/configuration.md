# Configuration

NetPulse has one settings file, `netpulse.toml`. It is the same file for the desktop app, the CLI and the service. The desktop app writes it on first run; `netpulse config init` writes a commented template. Relative paths inside it are relative to the file's own folder.

## Where the settings file is
NetPulse uses the **first file that exists**, in this order (`netpulse config path` prints it):
1. `--config <FILE>` on the command line (then nothing else is searched)
2. the `NETPULSE_CONFIG` environment variable
3. `netpulse.toml` in the current folder
4. `netpulse.toml` next to the program, then `config/netpulse.toml` next to it
5. the user's settings folder (where the desktop app writes it):
    - Windows: `%APPDATA%\NetPulse\netpulse.toml`
    - Linux: `$XDG_CONFIG_HOME/netpulse/netpulse.toml`, or `~/.config/netpulse/netpulse.toml`
    - macOS: `~/Library/Application Support/NetPulse/netpulse.toml`
6. Linux and macOS: `/etc/netpulse/netpulse.toml`

## A complete example
```toml
# NetPulse configuration. Relative paths are relative to this file's folder.

[api]
url = "https://r223uzh3ad.execute-api.ap-south-1.amazonaws.com"   # the NetPulse AI service
agent_id = "my-laptop"                                          # this computer's name at the service
token_file = "secrets/agent.token"  # your access key lives in this file, never in the config
timeout_s = 10
retry_attempts = 3

[capture]
# interface = "Ethernet"            # default: the adapter carrying internet traffic (default route)
promiscuous = false
# bpf_filter = "not port 22"        # tcpdump syntax
exclude_api_traffic = true          # do not analyse NetPulse's own calls to the API
ipv6 = true                         # analyse IPv6 traffic too

[batching]
max_flows = 500                     # flows per API request (max 1000)
flush_interval_ms = 2000

[queue]
max_pending = 50000                 # flows kept while the API is unreachable

[storage]
data_dir = "netpulse-data"          # local history (SQLite), runtime state, logs

[reports]
dir = "reports"

[alerts]
min_level = "medium"                # low | medium | high | critical
cooldown_s = 60

[risk]
window_s = 300
```

## Settings

### `[api]`: the AI service

| Key | Default | Meaning |
|---|---|---|
| `url` | the NetPulse AI service | Address of the inference API. Leave it unless told otherwise. |
| `agent_id` | – | This computer's name at the service. It must match the name your access key was issued for. |
| `token_file` | – | File holding your access key (one line, `np_…`). **Recommended**; required for the service. |
| `token_env` | – | Alternative: the name of an environment variable holding the key (for terminals and CI). |
| `timeout_s` | `10` | Seconds per request. |
| `retry_attempts` | `3` | Retries for temporary failures (timeouts, 502/503/504, 429). Wrong keys are never retried. |

!!! warning "Never put the key itself in `netpulse.toml`"
    Use `token_file` (or `token_env`). Restrict the key file to your user: `chmod 600` on Linux/macOS; on Windows it lives in your own profile. `netpulse config show` never prints the key.

### `[capture]`: what is captured

| Key | Default | Meaning |
|---|---|---|
| `interface` | automatic | Adapter name or description. Automatic means the adapter that holds the default route, found by a routing lookup that sends nothing. `netpulse interfaces` marks it with `*`. |
| `promiscuous` | `false` | Also capture traffic not addressed to this computer (on networks where that is visible). |
| `bpf_filter` | none | Capture filter in tcpdump syntax, e.g. `"not port 22"`. |
| `exclude_api_traffic` | `true` | Do not analyse NetPulse's own calls to the AI service. |
| `ipv6` | `true` | Analyse IPv6 too. `false` = IPv4 only, like the original 2018 tool. |

### `[batching]` and `[queue]`

| Key | Default | Meaning |
|---|---|---|
| `batching.max_flows` | `500` | Flows per request to the AI service (1–1000). |
| `batching.flush_interval_ms` | `2000` | Send a partial batch after this long. |
| `queue.max_pending` | `50000` | Flows kept while the AI service is unreachable. They are checked, in order, when it is back. They are never guessed. |

### `[storage]`, `[reports]`

| Key | Default | Meaning |
|---|---|---|
| `storage.data_dir` | `netpulse-data` | Local history (SQLite), runtime state, the durable queue and logs. |
| `reports.dir` | `reports` | Where `netpulse report` and the app write reports. |

### `[alerts]`, `[risk]`

| Key | Default | Meaning |
|---|---|---|
| `alerts.min_level` | `medium` | Lowest risk that raises an alert: `low`, `medium`, `high`, `critical`. |
| `alerts.cooldown_s` | `60` | Identical detections (same label, source, destination, port) within this time are folded into one alert with a count. |
| `risk.window_s` | `300` | Window for the risk score, threats and critical counts. |

## Environment variables

| Variable | Meaning |
|---|---|
| `NETPULSE_CONFIG` | Path of the settings file to use. |
| the one named by `token_env` | Your access key, if you use `token_env` instead of `token_file`. |

## Check your settings
```text
netpulse config check
```
It checks:
- the file
- the key file
- that the data and reports folders are writable
- that the AI service is reachable, has a verified model, uses the same feature schema, and **accepts your key**
- that live capture works
