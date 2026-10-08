---
title: netpulse devices
---

# `netpulse devices`

<span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

Hosts seen in the analysed traffic, with flow and threat counts. NetPulse is passive: it never probes the network.

## Syntax and options

--8<-- "cli/devices.md"

## Examples

```text title="Local devices, last 24 hours"
netpulse devices
```

```text title="Include internet hosts"
netpulse devices --all
```

## Expected output

```text
DEVICE        SCOPE  FLOWS   THREATS  FIRST SEEN  LAST SEEN
172.31.69.29  local  40,766  28,393   18:49:46    18:50:34
172.31.0.2    local  3,008   0        18:49:46    18:50:34
Devices are hosts seen in analysed traffic (passive; NetPulse does not probe the network). Add --all to include external hosts.
```

## JSON output

```json
[ { "ip": "172.31.69.29", "local": true, "flows": 40766, "threats": 28393,
    "first_seen": "2026-10-08T13:19:46.887173900+00:00", "last_seen": "2026-10-08T13:20:34.237572100+00:00" } ]
```

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

