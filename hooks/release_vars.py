"""MkDocs hook: one source for every value that changes between releases or settings.

Markdown pages may write these placeholders:
  {{ version }}  {{ release_date }}  {{ release_url }}
  {{ windows_installer }} {{ windows_cli }} {{ linux_deb }} {{ linux_appimage }}
  {{ linux_cli }} {{ macos_dmg }} {{ macos_cli }}            (file names)
  {{ access_form_url }}                                       (the AI access request form)
Release values come from docs/assets/downloads.json, written by scripts/gen_downloads.py
from the latest published GitHub Release. The form URL comes from mkdocs.yml
(extra.access_form_url). Templates (overrides/*.html) read the same data as
config.extra.release. An unknown placeholder fails the build.
"""
import json
import re
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{\s*([a-z_]+)\s*\}\}")
_values: dict = {}


def on_config(config):
    path = Path(config["docs_dir"]) / "assets" / "downloads.json"
    if not path.exists():
        raise SystemExit("docs/assets/downloads.json is missing: run `python scripts/gen_downloads.py` first")
    form = (config["extra"].get("access_form_url") or "").strip()
    if not form.startswith("https://"):
        raise SystemExit("mkdocs.yml: extra.access_form_url must be the https:// link of the access request form")
    m = json.loads(path.read_text(encoding="utf-8"))
    for f in m["files"]:
        f["size_mb"] = f"{f['size'] / 1048576:.1f} MB"
    m["by_key"] = {f["key"]: f for f in m["files"]}
    config["extra"]["release"] = m
    _values.clear()
    _values.update({"version": m["version"], "release_date": m["released"], "release_url": m["release_page"],
                    "access_form_url": form, "github_handle": config["extra"].get("github_handle", ""),
                    "license": config["extra"].get("license", "")})
    _values.update({f["key"]: f["file"] for f in m["files"]})
    return config


INCLUDE = re.compile(r'^([ \t]*)--8<-- "([^"]+)"[ \t]*$', re.MULTILINE)
SNIPPETS = Path(__file__).resolve().parent.parent / "snippets"


def expand_includes(markdown: str, page) -> str:
    """Inline `--8<-- "file"` (snippets/) before placeholders are filled, so shared
    snippets may use {{ access_form_url }} and friends too."""
    def include(m):
        path = SNIPPETS / m.group(2)
        if not path.exists():
            raise SystemExit(f"{page.file.src_path}: snippet {m.group(2)} not found in snippets/")
        text = path.read_text(encoding="utf-8").rstrip("\n")
        return "\n".join(m.group(1) + line if line else line for line in text.split("\n"))
    return INCLUDE.sub(include, markdown)


def on_page_markdown(markdown, page, config, files):
    if page.file.src_path.replace("\\", "/").startswith("maintainer/"):
        return markdown  # the maintainer pages talk about the placeholders themselves
    markdown = expand_includes(markdown, page)

    def fill(match):
        key = match.group(1)
        if key not in _values:
            raise SystemExit(f"{page.file.src_path}: unknown placeholder {{{{ {key} }}}}")
        return _values[key]

    return PLACEHOLDER.sub(fill, markdown)
