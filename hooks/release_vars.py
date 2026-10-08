"""MkDocs hook: fill release placeholders from docs/assets/downloads.json.

Pages write {{ version }}, {{ release_date }}, {{ release_url }} or a file name such as
{{ windows_installer }}, {{ windows_cli }}, {{ linux_deb }}, {{ linux_appimage }},
{{ linux_cli }}, {{ macos_dmg }}, {{ macos_cli }}. downloads.json is written by
scripts/gen_downloads.py from the latest published GitHub Release, so a new release
needs no page edits. An unknown placeholder fails the build.
"""
import json
import re
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{\s*([a-z_]+)\s*\}\}")
_values = None


def on_config(config):
    global _values
    path = Path(config["docs_dir"]) / "assets" / "downloads.json"
    if not path.exists():
        raise SystemExit("docs/assets/downloads.json is missing: run `python scripts/gen_downloads.py` first")
    m = json.loads(path.read_text(encoding="utf-8"))
    _values = {"version": m["version"], "release_date": m["released"], "release_url": m["release_page"]}
    _values.update({f["key"]: f["file"] for f in m["files"]})
    return config


def on_page_markdown(markdown, page, config, files):
    if page.file.src_path.replace("\\", "/").startswith("maintainer/"):
        return markdown  # the maintainer guide talks about the placeholders themselves
    def fill(match):
        key = match.group(1)
        if key not in _values:
            raise SystemExit(f"{page.file.src_path}: unknown placeholder {{{{ {key} }}}}")
        return _values[key]

    return PLACEHOLDER.sub(fill, markdown)
