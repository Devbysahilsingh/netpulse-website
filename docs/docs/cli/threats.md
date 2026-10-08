---
title: netpulse threats
---

# `netpulse threats`

<span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

Flows the AI labelled as something other than Benign, newest first.

## Syntax and options

--8<-- "cli/threats.md"

## Examples

```text title="Last 24 hours"
netpulse threats
```

```text title="Last hour, at most 20"
netpulse threats --since 1h -n 20
```

## Expected output

```text
TIME         SOURCE               DESTINATION         PROTO  LABEL         CONF  RISK
03-03 02:55  5.101.40.43:57516    172.31.69.29:3389   TCP    Infiltration  0.20  LOW
03-03 01:24  18.219.211.138:8080  172.31.69.29:50909  TCP    Bot           0.99  CRITICAL
2 threats (newest first; --since 24h, --limit 2).
```

## JSON output

```json
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

## Common errors

| You see | What to do |
|---|---|
| `invalid duration unit in "5x" (use s, m, h or d)` | `--since` takes `30m`, `24h`, `7d` … or `all`. |

## Notes

`app` (the program behind the connection) and `host` (the website) are filled in for live capture when known; both stay on your computer.

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

Generated syntax from `netpulse threats --help`; examples verified with NetPulse 0.1.0. Example addresses come from the public CSE-CIC-IDS2018 captures or are shortened.
