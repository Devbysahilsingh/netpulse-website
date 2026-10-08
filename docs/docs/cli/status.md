---
title: netpulse status
---

# `netpulse status`

<span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

The one-screen summary: is a monitor running and on which adapter, what the AI service says, and the last five minutes' threats and risk. When nothing is monitoring, it asks the AI service directly and also checks that your access key is accepted.

## Syntax and options

--8<-- "cli/status.md"

## Examples

```text title="Show the status"
netpulse status
```

```text title="For scripts"
netpulse --json status
```

## Expected output

```text
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

## JSON output

```json
{
  "system": "OFFLINE",
  "liveness": "stopped",
  "network": "IDLE (not monitoring)",
  "devices": 4,
  "aws": { "state": "connected", "detail": "CONNECTED (model v2)", "model_version": "2" },
  "runtime": null
}
```

## Common errors

| You see | What to do |
|---|---|
| `no netpulse.toml found` | No settings yet. Open the desktop app once (its first run writes them) or run `netpulse config init`. |
| `AWS AI  NOT CONFIGURED (agent token not found …)` | The key file is missing: [request a key]({{ access_form_url }}){ target="_blank" rel="noopener" } and paste it in the app. |
| `AWS AI  ACCESS KEY NOT ACCEPTED` | The key is wrong or revoked. Check that it was pasted completely; otherwise request a new one. |
| `AWS AI  AWS AI service unavailable (…)` | The service cannot be reached (internet, proxy, outage). Flows wait in the queue; nothing is guessed. |

## Notes

**`AWS AI` values:** `CONNECTED (model vN)` · `CONNECTING (no batch sent yet)` · `AWS AI service unavailable (…)` · `ACCESS KEY NOT ACCEPTED (…)` · `NOT CONFIGURED (…)`.
In JSON, `aws.state` is `connected`, `connecting`, `unavailable`, `error` or `not_configured`; `runtime` holds the running monitor's full status (the same object as [`start`](start.md) returns).

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

Generated syntax from `netpulse status --help`; examples verified with NetPulse 0.1.0. Example addresses come from the public CSE-CIC-IDS2018 captures or are shortened.
