---
title: netpulse report
---

# `netpulse report`

<span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

Writes a report: overview, verdicts by label and by risk, alerts, threats and local devices.

## Syntax and options

--8<-- "cli/report.md"

## Examples

```text title="Markdown report for the last 24 hours"
netpulse report
```

```text title="JSON for the last 7 days, to a file"
netpulse report --since 7d --format json -o week.json
```

## Expected output

```text
Report written: C:\Users\you\AppData\Roaming\NetPulse\reports\netpulse-report-20261008-185036.md
```

## JSON output

```json
{ "report": "C:\\Users\\you\\AppData\\Roaming\\NetPulse\\reports\\netpulse-report-20261008-185037.md" }
```

## Common errors

| You see | What to do |
|---|---|
| `unknown report format "xml" (md or json)` | Use `--format md` or `--format json`. |

## Notes

A JSON report has the keys `generated_at`, `agent_id`, `since`, `summary`, `alerts`, `threats`, `local_devices`. The Technical view's *Reports* section writes the same reports.

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

Generated syntax from `netpulse report --help`; examples verified with NetPulse 0.1.0. Example addresses come from the public CSE-CIC-IDS2018 captures or are shortened.
