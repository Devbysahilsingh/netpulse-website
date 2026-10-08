# How it works

NetPulse is one **Rust core** used by three front ends, plus an AI service in the cloud. The model is never shipped to your computer.

```
 Desktop app (Tauri) ─┐
 CLI (netpulse) ──────┼─► NetPulse Core (Rust)
 Background service ──┘     capture → flows → 62 measurements ──HTTPS──► NetPulse AI service ─► model v2
                            + local context: app, website, Wi-Fi           (AWS API Gateway + Lambda)   (verified bundle)
                              (never sent)
                            + local history (SQLite), alerts, risk,
                              durable queue
```

## On your computer

| Part | What it does |
|---|---|
| **Collector** | Reads packets through Npcap (Windows) or libpcap/BPF (Linux, macOS). The library is loaded at run time, and on Windows only from the official Npcap folder. Groups packets into flows the same way CICFlowMeter-2018 did, quirks included. A flow ends after a FIN, after 120 s idle, or when capture stops. |
| **Feature contract** | Each finished flow becomes **62 numeric measurements**: duration, packet counts and sizes each way, inter-arrival times, TCP flags, window sizes, … The list is frozen as *feature schema 1.0.0* and shared by training, the AI service and the client; a mismatch is refused, never guessed around. |
| **Local context** | The app that owns a connection, the website name (from DNS and TLS SNI), the Wi-Fi network and the gateway. All of it **stays on the computer** and is only used to explain results to you. |
| **Engine** | Batches flows (up to 500), sends them to the AI service, validates the answer, stores verdicts, folds repeated detections into alerts, and computes the risk score. |
| **Durable queue** | When the AI service is unreachable, flows wait in memory (up to 50,000) and are saved to disk on shutdown. They are sent first next time and never scored locally. |
| **History** | SQLite database of flows, verdicts, alerts and devices in the data folder. |
| **Monitor lock** | One monitor per data folder. The desktop app, `netpulse start` and the service share it, and the others attach. |

## Front ends
- **Desktop app:** Tauri 2. The interface is plain HTML/CSS/JS with bundled fonts and a strict content-security policy (no inline scripts, no remote content). It calls the same core.
- **CLI:** `netpulse`, every command with `--json`.
- **Service:** the same `netpulse` binary registered with the Windows Service Control Manager, systemd or launchd.

## In the cloud
See [AI service (AWS)](ai-service.md):
- API Gateway (HTTPS)
- a Lambda function with the model
- model bundles with checksums
- hashed access keys

## Machine-learning pipeline (how the model is made)

```
CSE-CIC-IDS2018 (12.3 M flows) → validate → prepare (time repair, de-duplication, group-aware split)
  → train (XGBoost) → evaluate on a held-out test split once → quality gate → registry (@production)
  → signed-off bundle (model + manifest + checksums) → AI service
```

- **Split:** time-ordered within each day and label, 70/15/15. Identical flows never appear on both sides. Bot uses interleaved 1-minute blocks, because its C2 traffic changes over the session.
- **Quality gate:** a model is promoted only if it meets fixed thresholds (macro-F1, per-family recall, false alarms on benign traffic). Thresholds are never loosened to let a model pass.
- **Parity:** NetPulse's collector was checked against the dataset's own captures: 58 of 58 checked features match.

## Design rules
1. **No fake predictions.** No AI service, no verdict.
2. **Privacy:** only the 62 measurements and an opaque flow reference leave the computer.
3. **Model and app are decoupled.** The client only knows `POST /v1/predict` and the feature schema; models can be updated in the service without updating the app.
4. **Npcap is never bundled** (its licence forbids it). It is detected, and installing it is explained.
5. **No cloud credentials in the client.** The app knows only the public service address and your personal access key.
