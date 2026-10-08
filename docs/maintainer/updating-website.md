<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/updating-website.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Updating the website and documentation

The website is the public repository `Devbysahilsingh/netpulse-website`: MkDocs Material 9.6.23 with a NetPulse theme layer, deployed to GitHub Pages by `.github/workflows/pages.yml`.

## Where everything lives

| What | Where | How it goes live |
|---|---|---|
| **The AI access request form link** | `mkdocs.yml` → `extra.access_form_url`. **The only place.** Every *Request AI access* button (header, Home, Download, docs) and every `{{ access_form_url }}` placeholder reads it. | push to `main` |
| Contact handle, licence wording | `mkdocs.yml` → `extra.github_handle`, `extra.license` (licence: *All rights reserved. Free to use.*) | push to `main` |
| User docs | `docs/docs/**/*.md` (Docs tab), `docs/access.md`, `docs/about.md` | push to `main` → ✅ **AUTOMATED** build with `--strict` and deploy (~1 min) |
| Home page, Download page | templates `overrides/home.html`, `overrides/download.html` (text and per-OS steps live there; all numbers come from release data) | push to `main` |
| Header (version badge, Request AI access button), footer | `overrides/partials/header.html`, `overrides/partials/footer.html`. Copies of Material 9.6.23 partials with NetPulse additions. **Keep the Material version pinned in `pages.yml`**; re-copy the partials if you upgrade it. | push to `main` |
| Look and feel | `docs/assets/netpulse.css` (the desktop app's tokens), `docs/assets/netpulse.js` (OS detection, copy buttons), fonts in `docs/assets/fonts/` | push to `main` |
| Reusable text | `snippets/*.md`: `request-access.md`, `what-happens-next.md`, `update-steps.md`, `gatekeeper.md`. Include with `--8<-- "name.md"`; placeholders work inside. | push to `main` |
| Download data, Releases page, `downloads.json` | **generated**, never edited: `scripts/gen_downloads.py` reads the latest published release | ✅ **AUTOMATED** on every release publish/edit/delete and every push |
| Version numbers and file names in pages | placeholders `{{ version }}`, `{{ release_date }}`, `{{ windows_installer }}`, `{{ windows_cli }}`, `{{ linux_deb }}`, `{{ linux_appimage }}`, `{{ linux_cli }}`, `{{ macos_dmg }}`, `{{ macos_cli }}` (filled by `hooks/release_vars.py`) | automatic: no page edits per release |
| Release notes | private repo `CHANGELOG.md` → GitHub Release text → Releases page | with each release |
| CLI *Syntax and options* sections | generated from the real `--help` into `snippets/cli/*.md` by `packaging/cli_reference.py` (private repo). Examples and errors are hand-written in `docs/docs/cli/<command>.md`. | 🟠 **CURRENTLY MANUAL:** `python packaging/sync_website_docs.py` |
| Maintainer pages | private repo `docs/maintainer/*.md` → website `docs/maintainer/` | 🟠 **CURRENTLY MANUAL:** `python packaging/sync_website_docs.py` |
| Screenshots | `docs/assets/screens/*.png`; replace a file with the same name to update it | push to `main` |

## Change the request form
1. Edit `extra.access_form_url` in `mkdocs.yml` (it must start with `https://`; the build refuses anything else).
2. `mkdocs build --strict`, commit, push. Every button follows.

The current form is the Google Form *NetPulse AI — Request Access*, owned by the maintainer's personal Google account.
- **Responses:** Google Forms → the form → *Responses*.
- **E-mail notifications:** on.
- **Settings:** respondent e-mails are not collected and no sign-in is required; the form itself asks for name and e-mail.

## After changing CLI commands or options
```powershell
cd U:\Projects\NetPulse-AI
cargo build --release -p netpulse-cli
python packaging/sync_website_docs.py --no-push     # regenerates snippets/cli/, copies maintainer pages
# edit ..\netpulse-website\docs\docs\cli\<command>.md: examples, output, common errors (verify by running them)
cd ..\netpulse-website; mkdocs build --strict; git add -A; git commit -m "CLI docs: …"; git push origin main
```
The CLI reference should describe the **released** version. Regenerate it as part of the release, after tagging.

## Updating screenshots
Take them from the real app with **demo data only**. Never use your own traffic, Wi-Fi name or apps:
1. Use a scratch settings file whose `data_dir` holds a scan of a public CSE-CIC-IDS2018 capture (`netpulse --config <scratch> scan --pcap <public capture>`).
2. Start the app with it: `$env:NETPULSE_CONFIG = "<scratch>\netpulse.toml"`. For the first-run screen, start the app with `APPDATA` pointed at an empty temporary folder for that process only. **Never rename or move your real `%APPDATA%\NetPulse`.**
3. Replace the Wi-Fi name in the screenshot, and say so in the caption.

## Preview locally
```powershell
cd U:\Projects\netpulse-website
conda activate eda-env
python scripts/gen_downloads.py          # needs at least one published release
mkdocs serve                             # http://127.0.0.1:8000/netpulse-website/, live reload
mkdocs build --strict                    # what CI runs: must have no warnings
git add -A; git commit -m "Docs: …"; git push origin main
gh run list --repo Devbysahilsingh/netpulse-website --limit 2        # pages run: success?
```

## Rules
- Never write a private identifier on the public site: no account ID, no bucket or parameter names, no personal e-mail addresses, no keys.
- Example outputs use the public CSE-CIC-IDS2018 captures, never your own traffic.
- Only document behaviour you have verified with the released version.
