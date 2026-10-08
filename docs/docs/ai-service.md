---
title: AI service
---

# The NetPulse AI service

NetPulse's threat analysis runs in the **NetPulse AI service**, hosted on Amazon Web Services (AWS) in the *Asia Pacific – Mumbai* region. The desktop app, the command line and the background service all use it over an encrypted HTTPS connection.

## What it does for you
1. NetPulse sends the **62 measurements** of each finished connection: durations, sizes, timings. No addresses, app names or websites.
2. The service's AI model decides whether the connection looks like normal traffic or one of the attack families, and how sure it is.
3. NetPulse receives a **label**, a **confidence** and a **risk level** for every connection and shows them to you. See [Alerts & threats](alerts-threats.md).

The model is never copied onto your computer. It can therefore be improved in the service, and every NetPulse version benefits without an update.

## The model

| | Current model (version 2) |
|---|---|
| Trained on | CSE-CIC-IDS2018: real attack and normal traffic, about 12 million labelled connections |
| Detects | Bot, DoS, DDoS, password guessing (brute force), web attacks, infiltration |
| Overall accuracy (macro-F1) | 0.867 |
| Bot connections found | 99.7 % |
| False alarms on normal traffic | 0.44 % |

Infiltration is the hardest family to tell apart from normal traffic, which is why NetPulse shows it as amber *Worth a look*. [Why](alerts-threats.md#the-infiltration-limitation)

## Safeguards
- **No answer, no verdict.** If the service cannot be reached, or cannot answer properly, NetPulse keeps the connections in a queue and checks them later. Nothing is guessed on your computer, and nothing is marked safe or unsafe until the service has answered.
- **Only real answers are accepted.** NetPulse checks that every answer matches exactly the connections it sent. An incomplete, mixed-up or altered answer is discarded and the connections stay queued.
- **Encrypted.** Everything travels over HTTPS.
- **Your key, nobody else's.** Each person gets an individual [access key](../access.md). The service stores only a fingerprint of it, never the key itself, and a key can be revoked on its own.

## Availability
- **First request after a quiet period:** the service starts on demand, so it can take a few seconds. NetPulse waits and retries by itself.
- **Outages:** NetPulse keeps up to 50,000 connections waiting and checks them when the service is back. Home shows *NetPulse AI not reachable* meanwhile.
- **Status check:** `netpulse status` or `netpulse config check` tell you whether the service is reachable and accepts your key.
