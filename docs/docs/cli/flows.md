---
title: netpulse flows
---

# `netpulse flows`

<span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

Every analysed flow, newest first, optionally only one label.

## Syntax and options

--8<-- "cli/flows.md"

## Examples

```text title="Last 50 flows"
netpulse flows
```

```text title="Only Bot verdicts"
netpulse flows --label Bot -n 2
```

## Expected output

```text
TIME         SOURCE               DESTINATION         PROTO  LABEL  CONF  RISK
03-03 01:24  18.219.211.138:8080  172.31.69.29:50909  TCP    Bot    0.99  CRITICAL
03-03 01:24  18.219.211.138:8080  172.31.69.29:50908  TCP    Bot    0.99  CRITICAL
2 flows (newest first; --since 24h, --limit 2).
```

## JSON output

Same objects as [`threats`](threats.md#json-output).

## Common errors

| You see | What to do |
|---|---|
| `No flows in the selected period (24h).` | Nothing matched: widen `--since`, check `--label` spelling (Benign, Bot, DoS, DDoS, BruteForce, WebAttack, Infiltration). |

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

