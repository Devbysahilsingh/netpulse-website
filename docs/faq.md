# FAQ

### How do I get an access key?
NetPulse is **invite-only** while the service is young. Keys are personal and handed out by the maintainer. To ask for one, contact [@Devbysahilsingh on GitHub](https://github.com/Devbysahilsingh). You will receive your key privately; never post a key in a public issue. One key is issued per computer name (`agent_id`).

### How do I update NetPulse?
**NetPulse does not update itself yet, and does not tell you about new versions.** New versions are announced on the [Releases](releases.md) page and the [Download](download.md) page always offers the latest one. To update:

1. Close NetPulse. If you use the background service, stop it first (`netpulse service stop`, as administrator/root).
2. Download the new version and install it **over** the old one, exactly like the first time.
3. Your settings, access key and history are kept: they live in your user folder, not in the program folder.
4. Start NetPulse (and the service) again. The footer of NetPulse Home shows the new version; `netpulse version` shows it for the CLI.

Automatic updates are planned for a later version.

### Is NetPulse free?
The download is free. The AI service is currently available by invitation.

### Does NetPulse slow down my computer or my internet?
Hardly. It reads copies of packets; it never sits in the path of your traffic. It sends only small batches of numbers (a few KB) to the AI service.

### Does NetPulse block attacks?
No. It detects and explains. Act on its advice, for example with your antivirus or your router settings.

### Does it replace my antivirus?
No. It complements it. Antivirus checks files; NetPulse watches how programs behave on the network. A bot that hides from your antivirus still has to talk to its controller, and that is what NetPulse sees.

### Can NetPulse see what I type, my passwords or the pages I read?
No. The AI only gets 62 measurements per connection: sizes, counts and timings. Website and app names are used **only on your computer** to explain results, and are never sent. See [Security & privacy](security-privacy.md).

### Why does NetPulse need internet access to judge my traffic?
The model runs in the NetPulse AI service, so it can be improved and updated without updating your app, and so the model is never copied onto computers. Without the service, NetPulse waits instead of guessing.

### What happens when I'm offline?
Connections are queued (up to 50,000) and checked when you are back online. Home says the AI is not reachable. Nothing is shown as safe until it was checked.

### Why is "Infiltration" amber and not red?
The model is unsure about this family: intruders inside a network use ordinary-looking connections. So NetPulse shows it as *Worth a look*. [Details](desktop.md#the-infiltration-limitation).

### Why does Windows/macOS warn me about the installer?
The installers are not code-signed yet. [What you will see and how to continue](install/index.md#why-do-i-see-a-security-warning).

### Why do I have to install Npcap myself?
Npcap's licence does not allow other software to include it, and installing a network driver should be your decision. NetPulse checks for it and links to the official page.

### Does NetPulse work on a VPN?
Yes. NetPulse watches the adapter that carries your internet traffic, which is the VPN adapter while the VPN is connected. You can [choose an adapter](configuration.md#capture-what-is-captured) yourself.

### Can I use it on a server without a screen?
Yes. Use the CLI-only archive and the [background service](service.md).

### Can I analyse a capture file from Wireshark?
Yes: `netpulse scan --pcap capture.pcapng`. It does not need Npcap.

### Which data was the AI trained on?
CSE-CIC-IDS2018 from the Canadian Institute for Cybersecurity: about 12 million labelled flows of real attacks and normal traffic. [More](what-is-netpulse.md#where-the-model-comes-from).

### Where are my settings and history? How do I remove everything?
See [where the app keeps things](desktop.md#where-the-app-keeps-things). Uninstall NetPulse, then delete that folder.
