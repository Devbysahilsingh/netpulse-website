---
title: netpulse stop
---

# `netpulse stop`

<span class="np-badge np-badge--grey">no admin rights*</span> <span class="np-badge np-badge--blue">--json</span>

Stops the monitor gracefully: open flows are completed and sent for analysis first; flows the AI service could not check are saved and sent first next time.

## Syntax and options

--8<-- "cli/stop.md"

## Examples

```text title="Stop"
netpulse stop
```

```text title="Wait up to 60 s, then terminate"
netpulse stop --timeout 60 --force
```

## Expected output

```text
NetPulse stopped. Flows analysed: 1,111, alerts raised: 1.
```

## JSON output

```json
{ "forced": false, "stopped": true, "was_running": true,
  "status": { "state": "stopped", "engine": { "flows_scored": 1111, "alerts_raised": 1, "pending": 0, "risk_score": 20 } } }
```

## Common errors

| You see | What to do |
|---|---|
| `NetPulse is not running.` | Nothing to stop (exit code 0). In JSON: `{"stopped": true, "was_running": false}`. |
| A monitor started by the service | Stop the service with `netpulse service stop` (administrator/root). |

## Notes

\* Stopping the background service's monitor needs administrator/root; use `netpulse service stop`.

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

Generated syntax from `netpulse stop --help`; examples verified with NetPulse 0.1.0. Example addresses come from the public CSE-CIC-IDS2018 captures or are shortened.
