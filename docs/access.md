---
title: Request AI access
---

# Request AI access

NetPulse's threat analysis runs in the **NetPulse AI service**. To use it you need a personal **access key**. Keys are free and issued individually while NetPulse is invite-only.

<div class="np-access" markdown>
<div><b>Request your access key</b><p>A short form: name, e-mail, computer name and operating system. Your key is sent to the e-mail address you enter.</p></div>
<a class="np-btn np-btn--primary np-btn--lg" href="{{ access_form_url }}" target="_blank" rel="noopener">Request AI access</a>
</div>

## What happens next?

--8<-- "what-happens-next.md"

## Before you have a key

| Works without a key | Needs a key |
|---|---|
| Download and install NetPulse; open the app; check the capture driver (`netpulse interfaces`); `netpulse status`; `netpulse config check` | Monitoring, scans and every AI verdict |

Without a key, NetPulse does not analyse connections. It never guesses a result on your computer: nothing is marked safe or unsafe until the NetPulse AI service has checked it.

## Rules that protect you

- **NetPulse never asks for cloud credentials.** No AWS keys, passwords or similar are needed, requested or included anywhere in the app.
- **Your access key is personal.** Never share it publicly, and never put it into scripts, repositories, screenshots or other applications.
- **Where the key is kept.** NetPulse stores it in its own file on your computer (`secrets/agent.token` next to your settings) and sends it only to the NetPulse AI service, over HTTPS. The service keeps only a hash of it.
- **Keys are issued by hand.** There is no automatic sign-up and no shared key. If your key leaks or stops working, request a new one; the old one is revoked.

## What the form collects, and why

| Field | Why |
|---|---|
| Full name, e-mail address | To know who the key is for, and to send it to you |
| Computer name | A label for the computer you will use NetPulse on; it helps keep track of keys. It does not have to match anything in the app. |
| Operating system | Windows, macOS or Linux, to help if you have setup questions |
| Reason (optional) | What you want to use NetPulse for |
| Key security confirmation | You agree to keep your key private |

Nothing else is collected: no sign-in, no network information. Questions? Contact [@{{ github_handle }}](https://github.com/Devbysahilsingh) on GitHub.
