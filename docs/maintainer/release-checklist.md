<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/release-checklist.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Release checklist

Copy this list into the release commit message, or into an issue, and tick it as you go. The commands are in [release-process.md](release-process.md); the explanations are in the [maintainer guide](index.md).

**Version:** `X.Y.Z` · **Type:** PATCH / MINOR / MAJOR ([rules](versioning.md)) · **Date:** ____

### Before tagging
- [ ] Code changes done; `git status` clean on `main`
- [ ] `cargo fmt --all -- --check` and `cargo clippy --workspace --all-targets -- -D warnings`
- [ ] `cargo test --workspace` · `node --check desktop\ui\home.js` · `node --check desktop\ui\app.js`
- [ ] `python -m pytest --ignore=tests/e2e` · `python -m pytest tests/e2e` (after `cargo build --release -p netpulse-cli`)
- [ ] AWS needed? If yes: `python -m ml.common.aws preflight` → OK, change deployed **first**, `/v1/health` verified (scenario E)
- [ ] `CHANGELOG.md`: `## [X.Y.Z] - date` written for users
- [ ] `python packaging/bump_version.py X.Y.Z`; `netpulse version` shows X.Y.Z
- [ ] Commit `Release X.Y.Z`, push; CI (`ci.yml`) green

### Build
- [ ] `git tag vX.Y.Z; git push origin vX.Y.Z`
- [ ] `release` run green: 3 package jobs + publish job
- [ ] Draft release on `netpulse-website` (automatic with `WEBSITE_RELEASE_TOKEN`, otherwise `python packaging/publish_release.py vX.Y.Z`)
- [ ] Draft has 10 files: 1 .exe, 1 .zip, 1 .deb, 1 .AppImage, 1 .dmg, 2 .tar.gz, 3 SHA256SUMS

### Test the real download
- [ ] `gh release download vX.Y.Z --repo Devbysahilsingh/netpulse-website`; SHA-256 of the installer equals SHA256SUMS
- [ ] Upgrade over the previous version: footer shows X.Y.Z; settings and history kept
- [ ] Fresh install (new PC/user) when the installer or first run changed: Npcap check, key, Start protection
- [ ] `netpulse config check` all OK; Home lists apps; footer *Connected to NetPulse AI · model N*
- [ ] AI negative check when the client↔AI code changed: wrong key shows *Access key not accepted*

### Publish
- [ ] `gh release edit vX.Y.Z --repo Devbysahilsingh/netpulse-website --draft=false --latest`
- [ ] `pages` run green; `downloads.json` shows X.Y.Z; the Download page button downloads the new file
- [ ] Website docs updated for new or changed features; maintainer docs synced (`python packaging/sync_website_docs.py`) if they changed
- [ ] Important update? Notice on the website's home page (there is no auto-update)
