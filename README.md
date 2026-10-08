# NetPulse AI: website, documentation and downloads

This repository hosts the public side of NetPulse AI:
- **Website and documentation:** <https://devbysahilsingh.github.io/netpulse-website/> (built from `docs/` with MkDocs Material, deployed by GitHub Pages).
- **Downloads:** installers and CLI archives for Windows, Linux and macOS are attached to the [Releases](https://github.com/Devbysahilsingh/netpulse-website/releases).

The NetPulse source code is not in this repository.

## Download
Go to the [Download page](https://devbysahilsingh.github.io/netpulse-website/download/) or the [latest release](https://github.com/Devbysahilsingh/netpulse-website/releases/latest). NetPulse is invite-only for now: you need a personal access key ([FAQ](https://devbysahilsingh.github.io/netpulse-website/faq/#how-do-i-get-an-access-key)).

## Working on the site
```bash
pip install "mkdocs-material==9.6.*"
mkdocs serve                              # http://127.0.0.1:8000
python scripts/gen_downloads.py v0.1.0    # regenerate docs/download.md from a published release
mkdocs build --strict
```
The download page is generated from the published GitHub Release, never written by hand, so every link, size, date and checksum is real.

## Releasing a version
1. Build the packages from the tagged source and attach them, with `SHA256SUMS-*.txt`, to a GitHub Release `vX.Y.Z` here.
2. Run `python scripts/gen_downloads.py vX.Y.Z`. Update `docs/releases.md` and `CHANGELOG.md`.
3. Push to `main`. The Pages workflow rebuilds and publishes the site.

Nothing secret is ever published here: no access keys, no cloud credentials, no infrastructure state.
