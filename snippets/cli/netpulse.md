```text
NETPULSE AI
Network Intelligence Platform

AI-powered network security: capture flows, analyse them with the NetPulse AI service, alert.

Usage: netpulse [OPTIONS] <COMMAND>

Commands:
  start       Start monitoring (in the background)
  stop        Stop monitoring
  status      Show system status
  monitor     Live monitoring (attaches to the running monitor, or monitors in the foreground)
  scan        Run a passive network scan (time-boxed capture + analysis), or analyse a capture file
  threats     Show detected threats
  alerts      Show security alerts
  devices     Show devices seen on the network
  flows       Show analysed network flows
  report      Generate a report
  config      Configuration
  interfaces  List capture interfaces and check that live capture works
  service     Manage the background service (install, uninstall, start, stop, status)
  version     Show version
  help        Print this message or the help of the given subcommand(s)

Options:
      --config <FILE>  Config file (default: search order shown by `netpulse config path`)
      --json           Machine-readable JSON output
  -h, --help           Print help
  -V, --version        Print version
```
