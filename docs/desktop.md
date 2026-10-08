# Desktop app

The desktop app has two faces over the same data:
- **NetPulse Home**, for everyone: plain words, no jargon.
- **Technical view**, for experts: every flow, alert and number.

You can switch between them at any time (*Settings → Open technical view*, and *← Home* to come back).

## First run
The first time you open NetPulse, it walks you through three steps:

1. **Connect to NetPulse protection.**
    - Paste **your access key** (NetPulse is invite-only for now).
    - The **computer name** is pre-filled.
    - The AI **service address** is pre-filled under *Advanced*.

    The key is saved in its own file and never shown again.
2. **Allow NetPulse to see your network.** NetPulse checks for the capture driver.
    - **Windows:** if Npcap is missing, it shows the official link <https://npcap.com/#download> with a **Copy link** button, then **Check again**. NetPulse never installs Npcap itself.
    - **Linux / macOS:** see the [install guides](install/index.md) for capture rights.
3. **Start protection.** NetPulse chooses the adapter that carries your internet traffic.

## NetPulse Home

### The big answer
At the top, one sentence:

| What you see | Meaning |
|---|---|
| **Your computer looks safe** (green) | Protection is on, and nothing needs attention. |
| **Something needs your attention** (red) | At least one real danger was found. The problem is listed below with what to do. |
| **Worth a look** (amber) | Only less certain findings. See [red vs amber](#red-alerts-vs-amber-worth-a-look). |
| **Protection is off** (grey) | Nothing is being watched. Press **Start protection**. |

Below it, three numbers:
- **connections checked today**
- **apps online** (used the internet in the last 10 minutes)
- **problems found**

### Network health and the Wi-Fi card
The Wi-Fi card (top left) shows the network you are on.
- **Safe · Password protected**, or a warning when the network has **no password** (anyone nearby can join it: avoid banking or shopping there).
- Open it to see the other devices NetPulse has seen on your network and whether your router was found.

### Apps using the internet
The left column lists every app that made connections today, newest first, with its main website.
- Search by app or website.
- Open an app to see the websites it talked to and any problems.
- An app with a problem is marked in red or amber.

### Problems
Each problem card says, in plain words:
- **What was seen**, e.g. *"A program on this computer is secretly talking to a computer on the internet that is known for controlling hacked devices."*
- **Why it matters.**
- **What to do**, e.g. *run a full virus scan*, with the exact clicks.
- **Technical details** (collapsed): label, confidence, addresses and ports, model version, for experts or support.

### Today
A timeline of what happened:
- problems
- "Everything looks normal"
- Wi-Fi changes
- the AI being unreachable or a rejected key
- protection paused

### Footer and Start / Stop
- The footer shows the version and the AI connection, e.g. **NetPulse {{ version }} · Connected to NetPulse AI · model 2**.
- **Start protection / Pause protection** turns monitoring on and off.
- If `netpulse start` or the background service is already monitoring **with the same settings file**, Home shows **On (background service or terminal)** and attaches to it. Pausing from the window does not stop someone else's monitor.

### Settings
- Theme (light, dark, system).
- Protection and AI status.
- The privacy promise.
- Where your data and settings live.
- The link to the Technical view.

## Red alerts vs amber "Worth a look"

| Label from the AI | Home shows | Colour | Why |
|---|---|---|---|
| Bot | **May be hacked** | <span class="np-red">red</span> | Very reliable (Bot recall 0.997). A program is talking to a botnet's controller. |
| DoS / DDoS | **Flood of traffic** | <span class="np-red">red</span> | Attack-like floods. |
| BruteForce | **Password guessing** | <span class="np-red">red</span> | Many fast login attempts. |
| WebAttack | **Website attack** | <span class="np-red">red</span> | Attempts to break into a website, e.g. hidden commands. |
| Infiltration | **Worth a look** | <span class="np-amber">amber</span> | See below. |
| anything else | **Looks unusual** | <span class="np-amber">amber</span> | Flagged, but no specific advice. |

### The Infiltration limitation
In the training data, *Infiltration* traffic looks very much like normal traffic: an intruder already inside uses ordinary connections. The model cannot separate the two reliably. It finds only part of the real infiltration, and some normal connections get this label, usually with **low confidence** (often 0.2–0.3).

That is why NetPulse shows Infiltration as **amber "Worth a look"**, never as a red danger. Treat it as a hint:
- **One-off, low-confidence Infiltration** on a well-known service (an update server, a big website) is most likely normal.
- **Repeated Infiltration** from the same app to unknown addresses is worth a closer look. Run a virus scan and check which program it is.

The Technical view and the CLI still show the label exactly as the AI returned it.

## How to read the AI results
Every verdict has three parts:
- **Label:** the traffic family (Benign, Bot, DoS, DDoS, BruteForce, WebAttack, Infiltration).
- **Confidence** (0–1): how sure the model is about that label. 0.99 is very sure; 0.25 is a weak guess.
- **Risk:** `low`, `medium`, `high` or `critical`. It combines the label's severity with the confidence. A critical Bot verdict at 0.99 matters; a low-risk Infiltration at 0.20 is a hint.

The **risk score** (0–100) summarises the last 5 minutes; **network health** is 100 minus it.

Remember:
- **The AI judges connections, not files.** It can tell that a program behaves like a bot; it cannot tell which file is infected. Use your antivirus for that.
- **A clean result is not a guarantee.** Attacks unlike the training data may look normal.
- **No AI, no verdict.** If the footer says the AI is not reachable, connections are waiting in a queue and nothing is shown as safe or unsafe until they are checked.

## Technical view
For experts. Six sections:

| Section | Shows |
|---|---|
| **01 Overview** | Monitoring state, AI service and model version, uptime, queue, risk score and scale, threats, critical, flows per second |
| **02 Live flows** | The latest analysed flows: time, source, destination, protocol, label, confidence, risk |
| **03 Alerts** | Alerts with severity, label, addresses, port, count (identical detections folded), first/last seen. Filter by period and minimum severity. |
| **04 Devices** | Hosts seen in the traffic, local and external, with flow and threat counts |
| **05 Reports** | Create Markdown/JSON reports for a period, and read earlier ones |
| **06 Settings** | Readiness checks (settings, key, folders, AI service, capture) and the capture interfaces |

**Start monitoring / Stop monitoring** are in the top bar. Everything shown comes from the AI service: nothing is predicted locally, and IP addresses never leave the computer.

## Where the app keeps things

| | Windows | Linux | macOS |
|---|---|---|---|
| Settings | `%APPDATA%\NetPulse\netpulse.toml` | `~/.config/netpulse/netpulse.toml` | `~/Library/Application Support/NetPulse/netpulse.toml` |
| Access key | `…\NetPulse\secrets\agent.token` | `…/netpulse/secrets/agent.token` | `…/NetPulse/secrets/agent.token` |
| History, logs | `…\NetPulse\netpulse-data\` | `…/netpulse/netpulse-data/` | `…/NetPulse/netpulse-data/` |
| Reports | `…\NetPulse\reports\` | `…/netpulse/reports/` | `…/NetPulse/reports/` |
