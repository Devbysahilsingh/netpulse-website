---
title: netpulse interfaces
---

# `netpulse interfaces`

<span class="np-badge np-badge--grey">works without a key</span> <span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

Lists every capture interface, marks with `*` the one NetPulse will use (the adapter that carries your internet traffic), and ends with whether live capture works and, if not, what to do.

## Syntax and options

--8<-- "cli/interfaces.md"

## Examples

```text title="List adapters and check capture"
netpulse interfaces
```

## Expected output

```text
Capture backend: Npcap
Library: C:\Windows\System32\Npcap\wpcap.dll (Npcap version 1.89, based on libpcap version 1.10.7 (64-bit time_t))
   INTERFACE                  STATE                             ADDRESS          DESCRIPTION
   \Device\NPF_{59D1…}        up, connected, virtual            192.168.112.1    Hyper-V Virtual Ethernet Adapter
*  \Device\NPF_{7619…}        up, connected, wi-fi              192.168.1.20     MediaTek Wi-Fi 6 MT7921 Wireless LAN Card
   \Device\NPF_Loopback       up, loopback                      127.0.0.1        Adapter for loopback traffic capture
Capture interface: MediaTek Wi-Fi 6 MT7921 Wireless LAN Card (default route: carries this computer's internet traffic)
Internet route via: 192.168.1.20
Live capture: READY
```

## JSON output

```json
{
  "backend": "Npcap",
  "library": ["C:\\Windows\\System32\\Npcap\\wpcap.dll", "Npcap version 1.89, based on libpcap version 1.10.7 (64-bit time_t)"],
  "interfaces": [
    { "name": "\\Device\\NPF_{7619…}", "description": "MediaTek Wi-Fi 6 MT7921 Wireless LAN Card",
      "loopback": false, "up": true, "wireless": true, "connected": true, "addresses": ["192.168.1.20"], "virtual": false }
  ]
}
```

## Common errors

| You see | What to do |
|---|---|
| Live capture not ready on Windows | Install [Npcap](https://npcap.com/#download) (default options), then run the command again. |
| Permission denied (Linux) | `sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/netpulse` |
| Permission denied (macOS) | Install Wireshark's ChmodBPF helper, or use the background service. |

## Notes

Adapter IDs and addresses above are shortened examples.

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

Generated syntax from `netpulse interfaces --help`; examples verified with NetPulse 0.1.0. Example addresses come from the public CSE-CIC-IDS2018 captures or are shortened.
