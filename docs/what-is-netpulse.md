# What is NetPulse AI

NetPulse AI is network security software for a single computer. It watches the connections the computer makes (to websites, apps, other machines) and asks an AI model whether each one looks like an attack.

It is made for two kinds of people:

- **Everyday users.** They open the desktop app and see **NetPulse Home**: one sentence about how things look, which apps are using the internet, and plain advice when something is wrong. No jargon.
- **Security professionals.** They use the desktop app's **Technical view** and the `netpulse` **command line**: every flow, label, confidence and risk level, with JSON output for scripts.

## How it works, in one paragraph

NetPulse captures the network packets of your computer (read-only, it never blocks or changes traffic) and groups them into *flows*: one flow is one conversation between two programs. When a flow ends, NetPulse computes 62 measurements of it, such as how long it lasted, how many packets went each way and how big they were. It sends **only those numbers** to the NetPulse AI service. The service runs the model and answers with a label (Benign, Bot, DDoS, …), a confidence and a risk level. NetPulse stores the answer on your computer, raises an alert when needed, and shows it to you.

```
your computer                                           NetPulse AI service (AWS)
┌──────────────────────────────────────────┐            ┌─────────────────────────┐
│ capture → flows → 62 measurements ───────┼── HTTPS ──►│ model (v2, XGBoost)     │
│ app names, websites, IPs (kept locally)  │◄───────────┼ label · confidence · risk│
│ history · alerts · Home · CLI            │            └─────────────────────────┘
└──────────────────────────────────────────┘
```

## What NetPulse is not

- **Not a firewall or antivirus.** It does not block connections or remove programs. It tells you what it sees, and what you can do about it.
- **Not a network scanner.** It never probes other devices; it only looks at traffic that already reaches your computer.
- **Not offline AI.** The model runs on the NetPulse AI service, not on your computer. Without the service, NetPulse queues connections and checks them later. It never guesses.

## Where the model comes from

The model was trained on **CSE-CIC-IDS2018**, a public dataset of real attack and normal traffic from the Canadian Institute for Cybersecurity (about 12 million labelled flows). Its 15 attack types are grouped into 7 families: Benign, DoS, DDoS, BruteForce, WebAttack, Bot, Infiltration.

NetPulse's flow measurements reproduce the tool that produced that dataset (CICFlowMeter-2018), so what the model sees on your computer matches what it learned from. This was checked on the dataset's own captures: 58 of 58 checked features matched.

The model in service is **version 2** (XGBoost). It passed the release quality gate: macro-F1 0.867, Bot recall 0.997, false alarms on normal traffic 0.44 %. [More on the AI service](ai-service.md).

## Status

The current version is NetPulse {{ version }} (released {{ release_date }}); 0.1.0 was the first public release.
- **Windows:** the main, fully tested platform.
- **Linux and macOS:** packages are provided. See [Releases](releases.md) for known limitations.
- **Access:** invite-only. You need a personal access key ([FAQ](faq.md#how-do-i-get-an-access-key)).
