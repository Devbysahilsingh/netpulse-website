---
title: netpulse start
---

# `netpulse start`

<span class="np-badge np-badge--green">needs an access key</span> <span class="np-badge np-badge--blue">--json</span>

Starts the monitor **in the background** and returns. It captures live traffic (or reads a capture file), has the AI service check every finished flow, stores the results and raises alerts. Only one monitor runs per settings file: the app, the CLI and the service share it.

## Syntax and options

--8<-- "cli/start.md"

## Examples

```text title="Monitor live traffic"
netpulse start
```

```text title="A specific adapter"
netpulse start -i "Ethernet"
```

```text title="Ignore SSH"
netpulse start --filter "not port 22"
```

```text title="Analyse a capture file in the background"
netpulse start --pcap capture.pcapng
```

## Expected output

```text
NetPulse started (pid 31720): monitoring \Device\NPF_{7619…} via Npcap [live]
Use `netpulse status`, `netpulse monitor` or `netpulse stop`.
```

## JSON output

```json
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

## Common errors

| You see | What to do |
|---|---|
| `NetPulse is already monitoring (pid N)` | A monitor is running (app, terminal or service). Use `netpulse status`, or `netpulse stop` first. |
| `interface "X" not found` | Use a name from `netpulse interfaces`. (In 0.1.0 the hint wrongly mentions `netpulse capture --list`; that command does not exist.) |
| `agent token not found` | No key yet: [request AI access]({{ access_form_url }}){ target="_blank" rel="noopener" }. |
| Capture errors | See [`interfaces`](interfaces.md#common-errors). |

## Notes

Needs an [access key](../../access.md) to analyse anything.

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error · `3` nothing analysed (AI service unavailable) · `4` partly analysed

Generated syntax from `netpulse start --help`; examples verified with NetPulse 0.1.0. Example addresses come from the public CSE-CIC-IDS2018 captures or are shortened.
