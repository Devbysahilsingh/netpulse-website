<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/making-changes.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Making code changes

1. **Branch** (optional for a one-person project, recommended for big changes): `git switch -c fix/short-name`.
2. **Change the code.** Keep one Core: the CLI, the service and the desktop app must share logic through `core/` or `cli/src/commands/` (the desktop links `netpulse_cli`), never duplicate it.
3. **Run the quality gate.** Every command must pass:
   ```powershell
   cargo fmt --all
   cargo clippy --workspace --all-targets -- -D warnings
   cargo test --workspace
   node --check desktop\ui\home.js; node --check desktop\ui\app.js
   conda activate eda-env
   python -m pytest --ignore=tests/e2e -q -p no:cacheprovider
   cargo build --release -p netpulse-cli; python -m pytest tests/e2e -q -p no:cacheprovider
   ```
4. **Commit and push to `main`.** ✅ **AUTOMATED:** `.github/workflows/ci.yml` runs Python tests, end-to-end tests, Rust on Linux/macOS/Windows, the service lifecycle on Linux and macOS, and the desktop build on all three OSes.
   ```powershell
   git add -A; git commit -m "Short summary of the change"; git push origin main
   gh run list --repo Devbysahilsingh/netpulse-ai --limit 3          # find the run id
   gh run watch <run-id> --repo Devbysahilsingh/netpulse-ai --exit-status   # wait for green
   ```
5. **Decide whether it needs a release** ([Versioning](versioning.md) *Versioning*). If yes, follow [the release process](release-process.md).

What must **never** be committed: anything in `server/.secrets/`, `*.token`, `infrastructure/aws/terraform.tfvars`, `*.tfstate*`, `*.tfplan`, `.env`. All of these are already in `.gitignore` ([Secrets: where they belong](secrets.md)).

---
