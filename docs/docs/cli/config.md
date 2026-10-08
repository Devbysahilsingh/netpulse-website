---
title: netpulse config
---

# `netpulse config`

<span class="np-badge np-badge--grey">no admin rights</span> <span class="np-badge np-badge--blue">--json</span>

Settings helpers: where the settings file is, what is in effect, a template, and a full readiness check. See [Configuration](../configuration.md) for every setting.

## Syntax and options

--8<-- "cli/config.md"

### `netpulse config path`

--8<-- "cli/config-path.md"

### `netpulse config show`

--8<-- "cli/config-show.md"

### `netpulse config init`

--8<-- "cli/config-init.md"

### `netpulse config check`

--8<-- "cli/config-check.md"

## Examples

```text title="Which file is used"
netpulse config path
```

```text title="Effective settings (never the key)"
netpulse config show
```

```text title="Write a template"
netpulse config init --path netpulse.toml
```

```text title="Check everything"
netpulse config check
```

## Expected output

`netpulse config check`. It also verifies that the AI service **accepts your key**: a wrong key gives `[FAIL] AWS AI service … reachable, but the access key was not accepted` and exit code 1.

```text
[ OK ] config          C:\Users\you\AppData\Roaming\NetPulse\netpulse.toml
[ OK ] agent token     file secrets/agent.token
[ OK ] data folder     C:\Users\you\AppData\Roaming\NetPulse\netpulse-data
[ OK ] reports folder  C:\Users\you\AppData\Roaming\NetPulse\reports
[ OK ] AWS AI service  https://r223uzh3ad.execute-api.ap-south-1.amazonaws.com - model v2, schema 1.0.0
[ OK ] live capture    Npcap Npcap version 1.89, based on libpcap version 1.10.7 (64-bit time_t) (10 interfaces)

Ready.
```

## JSON output

`result` is `ok`, `warn` or `fail`. `config show --json` returns every setting (the key only as `token_present` and `token_source`); `config path --json` returns `config` and `search_order`.

```json
{ "checks": [ { "name": "config", "result": "ok", "detail": "…\\netpulse.toml" },
              { "name": "AWS AI service", "result": "ok", "detail": "https://… - model v2, schema 1.0.0" } ] }
```

## Common errors

| You see | What to do |
|---|---|
| `netpulse.toml already exists` | `config init` will not overwrite: add `--force`, or choose another `--path`. |
| `no netpulse.toml found` | Open the desktop app once, or `netpulse config init`. |

## Exit codes

`0` success · `1` error (the message says what to do) · `2` usage error

Generated syntax from `netpulse config --help`; examples verified with NetPulse 0.1.0. Example addresses come from the public CSE-CIC-IDS2018 captures or are shortened.
