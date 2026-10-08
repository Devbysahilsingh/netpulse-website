"""Generate the release-driven parts of the site from the published GitHub Releases.

    python scripts/gen_downloads.py            # latest published release (what the Pages build runs)
    python scripts/gen_downloads.py v0.1.1     # a specific tag (preview)

Writes (all git-ignored; regenerated on every site build):
  docs/assets/downloads.json   release metadata: version, date, files, sizes, URLs, SHA-256
  docs/releases.md             every published release with its notes (from CHANGELOG.md)
The Download page (overrides/download.html), the header badge and the Home page render
downloads.json; Markdown pages use {{ version }}-style placeholders filled by
hooks/release_vars.py. A new release therefore needs no page edits.

Uses the public GitHub API (set GITHUB_TOKEN to avoid rate limits). Fails, and so
fails the build, if there is no published release, a file has no checksum, the
Windows installer is missing, or a download link does not answer.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

REPO = "Devbysahilsingh/netpulse-website"
ROOT = Path(__file__).resolve().parent.parent
API = f"https://api.github.com/repos/{REPO}"

# key, filename suffix, platform, architecture, description (page order)
KINDS = [
    ("windows_installer", "_x64-setup.exe", "Windows", "x64", "Desktop app + CLI (installer)"),
    ("windows_cli", "_windows_x86_64.zip", "Windows", "x64", "CLI only (zip)"),
    ("linux_deb", "_amd64.deb", "Linux", "x86_64", "Desktop app + CLI (.deb: Debian, Ubuntu)"),
    ("linux_appimage", "_amd64.AppImage", "Linux", "x86_64", "Desktop app (AppImage: any distribution)"),
    ("linux_cli", "_linux_x86_64.tar.gz", "Linux", "x86_64", "CLI only (tar.gz)"),
    ("macos_dmg", "_aarch64.dmg", "macOS", "Apple Silicon (arm64)", "Desktop app + CLI (.dmg)"),
    ("macos_cli", "_macos_aarch64.tar.gz", "macOS", "Apple Silicon (arm64)", "CLI only (tar.gz)"),
]
REQUIRED = {"windows_installer"}


def request(url, method="GET"):
    headers = {"User-Agent": "netpulse-website", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN") and url.startswith("https://api.github.com"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    return urllib.request.urlopen(urllib.request.Request(url, method=method, headers=headers), timeout=60)


def get_json(url):
    with request(url) as r:
        return json.loads(r.read())


def mb(n):
    return f"{n / 1024 / 1024:.1f} MB"


def day(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).date().isoformat()


def checksums(assets):
    sums = {}
    for a in assets:
        if a["name"].startswith("SHA256SUMS"):
            with request(a["browser_download_url"]) as r:
                for line in r.read().decode().splitlines():
                    if line.strip():
                        digest, fname = line.split(None, 1)
                        sums[fname.strip().lstrip("*")] = digest.lower()
    return sums


def manifest_for(rel):
    sums = checksums(rel["assets"])
    files = []
    for key, suffix, platform, arch, what in KINDS:
        match = [a for a in rel["assets"] if a["name"].endswith(suffix)]
        if not match:
            if key in REQUIRED:
                sys.exit(f"{rel['tag_name']} has no *{suffix}")
            continue
        a = match[0]
        if a["name"] not in sums:
            sys.exit(f"{a['name']} has no SHA-256 in the release's SHA256SUMS files")
        with request(a["browser_download_url"], method="HEAD") as r:  # follows the redirect to the file
            if r.status != 200:
                sys.exit(f"{a['browser_download_url']} answered {r.status}")
        files.append({"key": key, "platform": platform, "arch": arch, "what": what, "file": a["name"],
                      "size": a["size"], "url": a["browser_download_url"], "sha256": sums[a["name"]]})
    return {"version": rel["tag_name"].lstrip("v"), "tag": rel["tag_name"], "released": day(rel["published_at"]),
            "release_page": rel["html_url"], "files": files}


def releases_page(releases):
    out = ["---", "title: Releases", "---", "", "# Releases", "",
           "Every published version of NetPulse AI, newest first. Files: [Download](download.md) (latest) or each "
           "version's GitHub Release (older versions). Versions follow [semantic versioning](maintainer/versioning.md).", ""]
    for i, r in enumerate(releases):
        latest = " (latest)" if i == 0 else ""
        out += [f"## {r['tag_name'].lstrip('v')}{latest}", "",
                f"**Released:** {day(r['published_at'])} · [GitHub Release and files]({r['html_url']})", ""]
        body = (r.get("body") or "").replace("\r\n", "\n").strip()
        # demote the notes' own headings below this version's heading
        out += ["#" + line if line.startswith("#") else line for line in body.splitlines()]
        out += [""]
    return "\n".join(out)


def main(tag=None):
    releases = [r for r in get_json(f"{API}/releases?per_page=100") if not r["draft"] and not r["prerelease"]]
    if not releases:
        sys.exit("no published release yet: publish one (see the maintainer guide) before building the site")
    releases.sort(key=lambda r: r["published_at"], reverse=True)
    rel = next((r for r in releases if r["tag_name"] == tag), None) if tag else releases[0]
    if rel is None:
        sys.exit(f"{tag} is not a published release")
    m = manifest_for(rel)
    (ROOT / "docs/assets").mkdir(parents=True, exist_ok=True)
    (ROOT / "docs/assets/downloads.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
    (ROOT / "docs/releases.md").write_text(releases_page(releases), encoding="utf-8", newline="\n")
    print(f"site data for {m['tag']} (released {m['released']}): {len(m['files'])} files; {len(releases)} release(s) listed")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
