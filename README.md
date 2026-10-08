# NetPulse AI: website, documentation and downloads

The public side of NetPulse AI:
- **Website and documentation:** <https://devbysahilsingh.github.io/netpulse-website/>. MkDocs Material 9.6.23 with a NetPulse theme layer, built by `.github/workflows/pages.yml` and deployed to GitHub Pages.
- **Downloads:** installers and CLI archives for Windows, Linux and macOS on this repository's [Releases](https://github.com/Devbysahilsingh/netpulse-website/releases).
- **AI access:** invite-only. Request a key with the form linked on the site.

The NetPulse source code is in a private repository. Licence: All rights reserved. Free to use (see `LICENSE`).

## Layout

| Path | What |
|---|---|
| `mkdocs.yml` | Navigation, theme, and the one place for site settings: `extra.access_form_url` (the request form), `extra.github_handle`, `extra.license` |
| `docs/` | Pages. `docs/docs/` = Docs tab, `docs/docs/cli/` = CLI reference. User documentation only. |
| `overrides/` | Templates: `home.html`, `download.html`, `partials/header.html`, `partials/footer.html` |
| `snippets/` | Reusable text (`--8<-- "name.md"`); `snippets/cli/` = **generated** from the real `netpulse --help` |
| `hooks/release_vars.py` | Fills `{{ version }}`, file names, `{{ access_form_url }}` … and gives templates the release data |
| `scripts/gen_downloads.py` | Runs before every build: latest published release → `docs/assets/downloads.json` and `docs/releases.md` (both git-ignored) |
| `docs/assets/` | `netpulse.css`, `netpulse.js`, fonts, logo, screenshots (`screens/`) |

Releases drive the site. Publishing, editing or deleting a release rebuilds it; nothing version-specific is written by hand.

## Working on the site
```bash
pip install "mkdocs-material==9.6.23"
python scripts/gen_downloads.py     # needs at least one published release
mkdocs serve                        # http://127.0.0.1:8000/netpulse-website/
mkdocs build --strict               # what CI runs
```

Maintainer documentation (releasing, AWS, the model, this site) is private and not published here.

Nothing secret is ever published here: no access keys, no cloud credentials, no infrastructure state.
