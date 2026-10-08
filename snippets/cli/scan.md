```text
netpulse scan [OPTIONS]
```

| Option | Meaning |
|---|---|
| `-i, --interface <INTERFACE>` | Capture interface (default: config, then the adapter that carries the default route) |
| `--filter <FILTER>` | BPF capture filter, tcpdump syntax (e.g. "not port 22") |
| `--pcap <FILE>` | Analyse a .pcap/.pcapng file instead of live traffic |
| `-d, --duration <DURATION>` | How long to listen (live capture), e.g. 60s, 5m |
| `--report` | Also write a report file |

Also accepts the [global options](index.md#global-options) `--config <FILE>` and `--json`.
