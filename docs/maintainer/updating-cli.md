<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/updating-cli.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Updating the CLI and the service

- **Commands:** `cli/src/commands/*.rs`; argument definitions in `cli/src/main.rs` (clap). After adding or changing a command or option:
  1. `cargo test -p netpulse-cli` (the integration tests in `cli/tests/cli.rs` run the real binary against a mock API)
  2. update the website's `docs/cli.md` (public repo) with the new `--help` text and an example; the help text is the source of truth
  3. if the JSON output changes, note it in `CHANGELOG.md` under *Changed* (scripts depend on it)
- **Service:** `cli/src/service/{windows,systemd,launchd,units}.rs`. Lifecycle tests: Linux and macOS run in CI. Windows needs an elevated shell:
  ```powershell
  powershell -ExecutionPolicy Bypass -File tools\windows-service-test.ps1 -Out svc.log -Python C:\Users\Sahil\.conda\envs\eda-env\python.exe
  ```
- **Exit codes** (0, 1, 2, 3, 4) are a public contract: never renumber them.

---
