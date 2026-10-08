---
title: How it works
---

# How NetPulse works

```
 your computer                                                   NetPulse AI service
 ┌───────────────────────────────────────────────────┐          ┌──────────────────────┐
 │ 1. capture: copies of network packets (read-only) │          │                      │
 │ 2. flows: one per conversation between programs   │          │  AI model            │
 │ 3. 62 measurements per finished flow ─────────────┼── HTTPS ─►  label · confidence  │
 │ 4. results stored and explained ◄─────────────────┼──────────┤  risk                │
 │    app, website, Wi-Fi: added locally, never sent │          └──────────────────────┘
 └───────────────────────────────────────────────────┘
```

## Step by step
1. **Capture.** NetPulse reads copies of the packets your computer sends and receives: through Npcap on Windows, libpcap on Linux, BPF on macOS. It never blocks, changes or sends traffic of its own on your network.
2. **Flows.** Packets are grouped into *flows*: one flow is one conversation between two programs. A flow is finished when the connection closes, after 120 seconds without packets, or when monitoring stops.
3. **Measurements.** Each finished flow is described by 62 numbers: how long it lasted, how many packets and bytes went each way, the gaps between packets, and similar. These are computed exactly like the dataset the AI learned from.
4. **AI check.** Only those numbers go to the [NetPulse AI service](ai-service.md), which answers with a label, a confidence and a risk level.
5. **Explanation.** NetPulse adds what only your computer knows (which app made the connection, which website it was, which Wi-Fi you are on) and shows the result: in plain words on NetPulse Home, in full detail in the Technical view and the CLI.

## What NetPulse keeps on your computer
- **History:** every checked connection, alerts and devices, in a local database in your NetPulse folder ([where](desktop.md#where-the-app-keeps-things)).
- **Waiting connections:** a queue for when the AI service is unreachable, saved when NetPulse stops and sent first next time.
- **Your settings and access key**, each in its own file.

## One engine, three ways to use it
The desktop app, the `netpulse` command line and the background service are the same program inside. They share one monitor and one history, so you can start monitoring in one and watch it in another. Only one monitor runs at a time.

## Principles
- **No AI, no verdict.** Nothing is guessed locally.
- **Private by design.** Only the 62 measurements leave your computer ([details](security-privacy.md)).
- **Honest about limits.** Uncertain findings are amber, not red, and a clean result is not a guarantee.
- **No cloud credentials in the app.** NetPulse knows only the public address of the AI service and your personal access key.
