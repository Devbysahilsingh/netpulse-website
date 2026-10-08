---
title: netpulse version
---

# `netpulse version`

<span class="np-badge np-badge--grey">works without a key</span> <span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

Shows the NetPulse version, the build commit, the feature-schema version the client sends, and the capture backend.

## Syntax and options

--8<-- "cli/version.md"

## Examples

```text title="Show the version"
netpulse version
```

## Expected output

```text
NetPulse AI 0.1.0 (03b07e14df4d)
target          x86_64-pc-windows-msvc
feature schema  1.0.0 (2ec9acdaa6da)
capture backend Npcap
```

## JSON output

```json
{
  "capture_backend": "Npcap",
  "feature_schema": { "sha256": "2ec9acdaa6da32c7d55a31f08b8427ab87188ec3d9e3ab0751d884771295bc45", "version": "1.0.0" },
  "git_commit": "03b07e14df4d",
  "name": "NetPulse AI",
  "target": "x86_64-pc-windows-msvc",
  "version": "0.1.0"
}
```

## Notes

`netpulse --version` (or `-V`) prints just `netpulse 0.1.0`.

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

