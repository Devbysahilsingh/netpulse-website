# NetPulse AI: website, documentation and downloads

The public side of NetPulse AI:
- **Website and documentation:** <https://devbysahilsingh.github.io/netpulse-website/>. MkDocs Material, built from `docs/` by `.github/workflows/pages.yml` and deployed to GitHub Pages.
- **Downloads:** installers and CLI archives for Windows, Linux and macOS, attached to this repository's [Releases](https://github.com/Devbysahilsingh/netpulse-website/releases).

The NetPulse source code is in a private repository.

## Download
[Download page](https://devbysahilsingh.github.io/netpulse-website/download/) · [latest release](https://github.com/Devbysahilsingh/netpulse-website/releases/latest). NetPulse is invite-only for now: you need a personal access key ([FAQ](https://devbysahilsingh.github.io/netpulse-website/faq/#how-do-i-get-an-access-key)).

## How the site works
Releases drive the site; nothing version-specific is written by hand:
- **`scripts/gen_downloads.py` runs before every build.** It reads the latest **published** release and writes three git-ignored files:
  - `docs/assets/downloads.json` (version, date, files, sizes, URLs, SHA-256)
  - `docs/download.md`
  - `docs/releases.md` (every release's notes)
- **Pages use placeholders** such as `{{ version }}`, `{{ windows_installer }}` and `{{ linux_deb }}`. `hooks/release_vars.py` fills them from `downloads.json`.
- **`pages.yml` runs** on every push to `main` and whenever a release is published, edited or deleted. So publishing a release updates the site by itself.

## Working on the site
```bash
pip install "mkdocs-material==9.6.*"
python scripts/gen_downloads.py     # needs at least one published release
mkdocs serve                        # http://127.0.0.1:8000
mkdocs build --strict               # what CI runs
```

## Maintainers
Everything about releasing, AWS, the model and this site is in the **Maintainers** section of the website. It is generated from the private repository's `docs/MAINTAINER.md`, `docs/release-process.md` and `docs/release-checklist.md`; do not edit `docs/maintainer/` here.

Nothing secret is ever published here: no access keys, no cloud credentials, no infrastructure state.
