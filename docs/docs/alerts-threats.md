---
title: Alerts & threats
---

# Alerts & threats: reading the results

Every connection NetPulse checks gets three things from the AI:

- **Label:** the traffic family: Benign, Bot, DoS, DDoS, BruteForce, WebAttack, Infiltration.
- **Confidence** (0–1): how sure the model is. 0.99 is very sure; 0.25 is a weak hint.
- **Risk:** `low`, `medium`, `high` or `critical`. It combines how serious the family is with the confidence (risk = impact weight × confidence; `low` < 0.2 ≤ `medium` < 0.5 ≤ `high` < 0.8 ≤ `critical`).

A **threat** is any connection not labelled Benign. The **risk score** (0–100) summarises the last 5 minutes; **network health** is 100 minus it.

## Red vs amber on NetPulse Home

| AI label | Home shows | Colour | Why |
|---|---|---|---|
| Bot | **May be hacked** | <span class="np-red">red</span> | Very reliable (Bot recall 0.997). A program is talking to a botnet's controller. |
| DoS / DDoS | **Flood of traffic** | <span class="np-red">red</span> | Attack-like floods |
| BruteForce | **Password guessing** | <span class="np-red">red</span> | Many fast login attempts |
| WebAttack | **Website attack** | <span class="np-red">red</span> | Attempts to break into a website |
| Infiltration | **Worth a look** | <span class="np-amber">amber</span> | See below |
| other | **Looks unusual** | <span class="np-amber">amber</span> | Flagged, without specific advice |

Each problem on Home says **what was seen**, **why it matters** and **what to do** (for example: run a full virus scan), with the technical details folded underneath.

## The Infiltration limitation
In the training data, Infiltration traffic looks very much like normal traffic: an intruder already inside uses ordinary connections. The model therefore finds only part of the real infiltration and labels some normal connections Infiltration, usually with **low confidence** (about 0.2–0.4). That is why it is amber, never red.

- **One-off, low-confidence Infiltration** to a well-known service is most likely normal.
- **Repeated Infiltration** from the same app to unknown addresses is worth a closer look: run a virus scan and check which program it is.

The Technical view and the CLI always show the label exactly as the AI returned it.

## Alerts
An **alert** is raised for threats at or above `alerts.min_level` (default `medium`). Identical detections (same label, source, destination and port) within the cooldown (60 s) are **folded into one alert with a count**, so a flood reads as one line. See [`netpulse alerts`](cli/alerts.md), and the *Alerts* section of the Technical view.

## What a result is not
- **Not a file scan.** The AI judges connections, not files. It can tell that a program behaves like a bot; your antivirus finds the file.
- **Not a guarantee.** Attacks unlike the training data may look normal.
- **Not a guess.** Without the AI service there is no result at all; see [Monitoring](monitoring.md#when-the-ai-service-is-unreachable).
