---
title: netpulse scan
---

# `netpulse scan`

<span class="np-badge np-badge--green">needs an access key</span> <span class="np-badge np-badge--blue">--json</span>

A one-off check: listen live for a fixed time, or analyse a capture file, then print a summary (verdicts by label, threats, risk) and optionally write a report.

## Syntax and options

--8<-- "cli/scan.md"

## Examples

```text title="Listen for one minute"
netpulse scan --duration 60s
```

```text title="Analyse a Wireshark capture"
netpulse scan --pcap capture.pcapng
```

```text title="…and write a report"
netpulse scan --pcap capture.pcapng --report
```

## Expected output

A real scan of the public CSE-CIC-IDS2018 Bot capture, through the NetPulse AI service.

```text
NetPulse scan
--------------------------------
Source        bot-capture.pcap [pcap]
Result        complete
Flows         40,806
Threats       28,393
Alerts        20
Devices       4
Risk Score    90/100
Model         2
--------------------------------
LABEL         FLOWS
Bot           28,379
Benign        12,413
Infiltration  10
DDoS          4
```

## JSON output

```json
{
  "run": { "mode": "pcap", "source": "bot-capture.pcap", "ending": "source_finished",
           "status": { "flows_seen": 40806, "flows_scored": 40806, "threats": 28393, "critical": 26490,
                       "risk_score": 90, "network_health": 10, "aws": { "state": "connected", "model_version": "2" } } },
  "summary": { "by_label": [["Bot", 28379], ["Benign", 12413], ["Infiltration", 10], ["DDoS", 4]] },
  "alerts": [ { "id": 187, "severity": "critical", "label": "Bot", "src_ip": "18.219.211.138", "dst_ip": "172.31.69.29", "dst_port": 50897, "count": 1 } ],
  "local_devices": 4,
  "report": null
}
```

## Common errors

| You see | What to do |
|---|---|
| `cannot read capture file …` | Check the path; the file must be .pcap or .pcapng. |
| `agent token not found` | No key yet: [request AI access]({{ access_form_url }}){ target="_blank" rel="noopener" }. |
| Exit code 3 | The AI service was unavailable for the whole scan: nothing was analysed (and nothing guessed). |
| Exit code 4 | Only part of the scan could be analysed. |

## Notes

Capture files do not need Npcap. Needs an [access key](../../access.md) to analyse anything.

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error · `3` nothing analysed (AI service unavailable) · `4` partly analysed

