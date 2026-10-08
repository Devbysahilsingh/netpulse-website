---
title: netpulse alerts
---

# `netpulse alerts`

<span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

Security alerts. Identical detections (same label, source, destination and port) within the cooldown are folded into one alert with a `count`.

## Syntax and options

--8<-- "cli/alerts.md"

## Examples

```text title="Last 24 hours"
netpulse alerts
```

```text title="Only high and critical, last 7 days"
netpulse alerts --since 7d --severity high
```

## Expected output

```text
ID   SEVERITY  LABEL  SOURCE          DESTINATION   PORT   COUNT  FIRST     LAST
187  CRITICAL  Bot    18.219.211.138  172.31.69.29  50897  1      18:50:30  18:50:30
188  CRITICAL  Bot    18.219.211.138  172.31.69.29  50898  1      18:50:30  18:50:30
COUNT = repeated identical detections folded into one alert.
```

## JSON output

```json
[
  {
    "id": 187, "created_at": "2026-10-08T13:20:30.722519700+00:00", "last_seen": "2026-10-08T13:20:30.722519700+00:00",
    "severity": "critical", "label": "Bot", "src_ip": "18.219.211.138", "dst_ip": "172.31.69.29", "dst_port": 50897,
    "count": 1, "model_version": "2", "sample_flow_ref": "f56673558bb6f0-37709"
  }
]
```

## Common errors

| You see | What to do |
|---|---|
| `invalid duration unit …` | `--since` takes `30m`, `24h`, `7d` … or `all`. |

## Notes

Which threats become alerts is set by `alerts.min_level` and `alerts.cooldown_s` in the [configuration](../configuration.md).

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

Generated syntax from `netpulse alerts --help`; examples verified with NetPulse 0.1.0. Example addresses come from the public CSE-CIC-IDS2018 captures or are shortened.
