---
title: NetPulse AI
hide:
  - navigation
  - toc
---

<div class="np-hero" markdown>

# Know when something on your network looks wrong.

<p class="lead">NetPulse AI watches the connections your computer makes and asks an AI model, trained on real attack traffic, whether each one looks like an attack. It tells you in plain words. Experts get every detail in a technical view and a full command line.</p>

<div class="np-cta" markdown>
[Download for Windows](download.md#windows){ .md-button .md-button--primary }
[Linux](download.md#linux){ .md-button }
[macOS](download.md#macos){ .md-button }
[Read the docs](what-is-netpulse.md){ .md-button }
</div>

<p class="np-small">Version 0.1.0 · Windows 10/11 (64-bit), Linux x86_64, macOS 11+ on Apple Silicon · Free download · Access is invite-only for now: you need an <a href="faq/#how-do-i-get-an-access-key">access key</a>.</p>

</div>

## From download to protected in four steps

<div class="np-steps" markdown>
<div><b>Download</b>The installer for your system from the <a href="download/">Download page</a>.</div>
<div><b>Install</b>Run it. Windows also needs the free Npcap driver; NetPulse checks for it and links to the official page.</div>
<div><b>Launch</b>Open NetPulse and paste your access key. The computer name and AI service are filled in for you.</div>
<div><b>Start monitoring</b>Press <em>Start protection</em>. NetPulse picks the network adapter you use for the internet automatically.</div>
</div>

## What you get

<div class="np-grid" markdown>
<div class="np-card"><h3>Plain-words Home</h3><p>“Your computer looks safe”, or exactly which app is in trouble and what to do. Real dangers are <span class="np-red">red</span>; things worth a look are <span class="np-amber">amber</span>.</p></div>
<div class="np-card"><h3>AI verdict on every connection</h3><p>Each finished connection is described by 62 measurements and checked by the NetPulse model (XGBoost, trained on CSE-CIC-IDS2018).</p></div>
<div class="np-card"><h3>Private by design</h3><p>Only anonymous measurements are sent. IP addresses, app names, websites and your Wi-Fi name stay on your computer.</p></div>
<div class="np-card"><h3>Never makes things up</h3><p>No AI service, no verdict. Connections wait in a queue and are checked when the service is back. Nothing is guessed locally.</p></div>
<div class="np-card"><h3>Technical view and CLI</h3><p>Live flows, alerts, devices, reports, and a <code>netpulse</code> command line with JSON output for every command.</p></div>
<div class="np-card"><h3>Runs in the background</h3><p>Optional service for Windows, Linux (systemd) and macOS (launchd). It restarts itself after a failure and keeps unsent work across restarts.</p></div>
</div>

## Detects

| Family | Examples | How Home shows it |
|---|---|---|
| Bot | A program talking to a botnet's command server | <span class="np-red">May be hacked</span> |
| DoS / DDoS | Floods of traffic | <span class="np-red">Flood of traffic</span> |
| Brute force | Many fast password attempts (FTP, SSH) | <span class="np-red">Password guessing</span> |
| Web attack | SQL injection, cross-site scripting | <span class="np-red">Website attack</span> |
| Infiltration | Intruder-like movement inside a network | <span class="np-amber">Worth a look</span> |

Infiltration is shown in amber because the model is less certain about it. See [how to read AI results](desktop.md#how-to-read-the-ai-results).

!!! info "First public release"
    NetPulse 0.1.0 is the first public release. The installers are not code-signed yet, so Windows and macOS show a warning the first time. The [installation guides](install/index.md) show what you will see and how to continue.
