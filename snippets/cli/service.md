```text
netpulse service [OPTIONS] <COMMAND>
```

| Subcommand | What it does |
|---|---|
| `install` | Register NetPulse with the system service manager (administrator/root) |
| `uninstall` | Remove the service (local history and reports are kept) |
| `start` | Start the service |
| `stop` | Stop the service |
| `restart` | Stop the service (gracefully) and start it again |
| `status` | Service manager state and what the service is monitoring |

Also accepts the [global options](index.md#global-options) `--config <FILE>` and `--json`.
