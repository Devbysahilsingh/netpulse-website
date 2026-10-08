---
title: netpulse monitor
---

# `netpulse monitor`

<span class="np-badge np-badge--green">needs an access key</span> <span class="np-badge np-badge--blue">--json</span>

Live view. If a monitor is already running (app, `netpulse start` or the service), `monitor` **attaches** to it and shows verdicts as they arrive. Otherwise it monitors in the foreground until **Ctrl-C**.

## Syntax and options

--8<-- "cli/monitor.md"

## Examples

```text title="Live view of everything"
netpulse monitor
```

```text title="Only attacks"
netpulse monitor --threats-only
```

```text title="Replay a capture file"
netpulse monitor --pcap capture.pcap --threats-only
```

## Expected output

```text
NETPULSE AI
Monitoring: ACTIVE   Source: capture.pcap [pcap]   (Ctrl-C stops)
TIME        SOURCE                 DESTINATION            PROTOCOL LABEL        RISK
03-03 02:58 52.15.155.232:80       172.31.69.25:56702     TCP      Infiltration MEDIUM
THREATS: 1   CRITICAL: 0   RISK SCORE: 20/100
Analysed 1,111 flows from capture.pcap in 1s; alerts raised 1.
```

## JSON output

With `--json`, `monitor` prints **one JSON object per line** (JSON Lines): `"type": "flow"` for each verdict, and a final `"type": "summary"`.

```json
{"type":"flow","seq":43027,"flow_ref":"f56674a7329387-1110","observed_at":"2018-03-02T21:28:10.902407+00:00","src_ip":"52.15.155.232","src_port":80,"dst_ip":"172.31.69.25","dst_port":56702,"protocol":6,"label":"Infiltration","confidence":0.227439,"risk":"medium","model_version":"2","app":null,"host":"us-east-2.ec2.archive.ubuntu.com","scored_at":"2026-10-08T13:26:14.219734500+00:00"}
{"type":"summary","report":{"ending":"source_finished","mode":"pcap","source":"capture.pcap","status":{"flows_seen":1111,"flows_scored":1111,"threats":1,"critical":0,"risk_score":20,"aws":{"state":"connected","model_version":"2"}}}}
```

## Common errors

| You see | What to do |
|---|---|
| `cannot read capture file …` | The file does not exist or is not a .pcap/.pcapng capture (Ethernet, Linux cooked, loopback or raw IP). |
| `agent token not found` | No key yet: [request AI access]({{ access_form_url }}){ target="_blank" rel="noopener" }. |

## Notes

Needs an [access key](../../access.md) to analyse anything.

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error · `3` nothing analysed (AI service unavailable) · `4` partly analysed

