---
title: Monitoring
---

# Monitoring

Monitoring means: capture the computer's network traffic, turn it into flows, have the NetPulse AI service check each finished flow, and keep the results. It needs an [access key](../access.md).

## Start and stop

| From | Start | Stop |
|---|---|---|
| Desktop app | **Start protection** on Home (or *Start monitoring* in the Technical view) | **Pause protection** |
| Command line | [`netpulse start`](cli/start.md) (background) or [`netpulse monitor`](cli/monitor.md) (foreground) | [`netpulse stop`](cli/stop.md), or Ctrl-C for `monitor` |
| Background service | [`netpulse service start`](cli/service.md) | `netpulse service stop` |

**One monitor at a time** per settings file. If one is already running, the desktop app shows *On (background service or terminal)* and attaches to it, `netpulse monitor` attaches to it, and `netpulse start` refuses to start a second one.

## Which network adapter
NetPulse chooses the adapter that carries your **default route**: the one your internet traffic actually uses. It finds it with a routing lookup that sends nothing. It never picks "the first adapter that is up".

- On a VPN, that is usually the VPN adapter.
- `netpulse interfaces` shows the chosen adapter with `*` and explains why.
- To choose yourself, set `capture.interface` in the [configuration](configuration.md) or use `netpulse start -i "<name>"`.

## When connections appear
A connection is checked when its flow **ends**: after the connection closes, or after 120 seconds without packets, or when monitoring stops (open flows are completed and checked). So right after starting, give it a minute and use the internet a little.

## When the AI service is unreachable
- **Flows are not lost.** They wait in a queue (up to 50,000 by default) and are checked, in order, as soon as the service is back.
- **They are kept across stops.** On stop, unchecked flows are saved and sent first next time.
- **Nothing is guessed meanwhile.** Home shows *NetPulse AI not reachable*; the CLI shows `AWS AI service unavailable`.

## What is checked
IPv4 and IPv6, TCP and UDP. NetPulse's own calls to the AI service are excluded. Only 62 measurements per flow are sent: [Security & privacy](security-privacy.md).

## Capture permissions

| System | What is needed |
|---|---|
| Windows | [Npcap](https://npcap.com/#download), installed once by you |
| Linux | `CAP_NET_RAW` + `CAP_NET_ADMIN` for the CLI (`setcap`, see [Linux](install/linux.md)), or the service |
| macOS | BPF access: Wireshark's ChmodBPF helper, or the service |
