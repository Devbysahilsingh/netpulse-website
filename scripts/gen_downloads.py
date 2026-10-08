"""Generate docs/download.md and docs/assets/downloads.json from a published GitHub Release.

    python scripts/gen_downloads.py v0.1.0

Reads the release through the public GitHub API (no token needed), takes the
SHA-256 values from the release's own SHA256SUMS-*.txt assets, checks that every
download link answers, and refuses to write a page with a missing installer.
"""
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

REPO = "Devbysahilsingh/netpulse-website"
ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com/repos/{repo}/releases/tags/{tag}"

# (filename pattern, platform, architecture, what it is) in page order
KINDS = [
    ("_x64-setup.exe", "Windows", "x64", "Desktop app + CLI (installer)"),
    ("_windows_x86_64.zip", "Windows", "x64", "CLI only (zip)"),
    ("_amd64.deb", "Linux", "x86_64", "Desktop app + CLI (.deb: Debian, Ubuntu)"),
    ("_amd64.AppImage", "Linux", "x86_64", "Desktop app (AppImage: any distribution)"),
    ("_linux_x86_64.tar.gz", "Linux", "x86_64", "CLI only (tar.gz)"),
    ("_aarch64.dmg", "macOS", "Apple Silicon (arm64)", "Desktop app + CLI (.dmg)"),
    ("_macos_aarch64.tar.gz", "macOS", "Apple Silicon (arm64)", "CLI only (tar.gz)"),
]
REQUIRED = {"_x64-setup.exe"}  # never publish a download page without the Windows installer
INSTALL = {"Windows": "install/windows.md", "Linux": "install/linux.md", "macOS": "install/macos.md"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "netpulse-website", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
        return data if binary else json.loads(data)


def reachable(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "netpulse-website"})
    with urllib.request.urlopen(req, timeout=30) as r:  # follows the redirect to the file
        return r.status == 200


def size(n):
    return f"{n / 1024 / 1024:.1f} MB"


def main(tag):
    rel = get(API.format(repo=REPO, tag=tag))
    if rel.get("draft") or rel.get("prerelease"):
        sys.exit(f"{tag} is a draft or pre-release; publish it first")
    assets = {a["name"]: a for a in rel["assets"]}
    sums = {}
    for name, a in assets.items():
        if name.startswith("SHA256SUMS"):
            for line in get(a["browser_download_url"], binary=True).decode().splitlines():
                if line.strip():
                    digest, fname = line.split(None, 1)
                    sums[fname.strip().lstrip("*")] = digest.lower()

    version = tag.lstrip("v")
    date = datetime.fromisoformat(rel["published_at"].replace("Z", "+00:00")).date().isoformat()
    rows = []
    for suffix, platform, arch, what in KINDS:
        match = [a for n, a in assets.items() if n.endswith(suffix)]
        if not match:
            if suffix in REQUIRED:
                sys.exit(f"release {tag} has no *{suffix}")
            print(f"note: no *{suffix} in {tag}; left out of the page")
            continue
        a = match[0]
        if a["name"] not in sums:
            sys.exit(f"{a['name']} has no SHA-256 in the release's SHA256SUMS files")
        if not reachable(a["browser_download_url"]):
            sys.exit(f"{a['browser_download_url']} does not answer 200")
        rows.append({"platform": platform, "arch": arch, "what": what, "file": a["name"], "size": a["size"],
                     "url": a["browser_download_url"], "sha256": sums[a["name"]]})

    manifest = {"version": version, "tag": tag, "released": date, "release_page": rel["html_url"], "files": rows}
    (ROOT / "docs/assets").mkdir(parents=True, exist_ok=True)
    (ROOT / "docs/assets/downloads.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    out = [
        "---", "title: Download", "---", "",
        f"# Download NetPulse AI {version}", "",
        f"**Latest version:** {version} · **Released:** {date} · "
        f"[Release notes](releases.md) · [All files on GitHub]({rel['html_url']})", "",
        "Every package contains the desktop app and the `netpulse` command line, except the CLI-only archives. "
        "You also need a personal [access key](faq.md#how-do-i-get-an-access-key): NetPulse is invite-only for now, "
        "and no key is included in any download.", "",
    ]
    for platform in ("Windows", "Linux", "macOS"):
        mine = [r for r in rows if r["platform"] == platform]
        if not mine:
            continue
        out += [f"## {platform}", ""]
        first = mine[0]
        out += [f"[Download {first['file']}]({first['url']}){{ .md-button .md-button--primary }}", ""]
        out += ["| File | What | Architecture | Size |", "|---|---|---|---|"]
        out += [f"| [`{r['file']}`]({r['url']}) | {r['what']} | {r['arch']} | {size(r['size'])} |" for r in mine]
        out += ["", f"How to install: [{platform} guide]({INSTALL[platform]})."]
        if platform == "Windows":
            out += ["", "!!! warning \"Windows SmartScreen\"",
                    "    The installer is not code-signed yet. Windows may show *“Windows protected your PC”* and "
                    "*Unknown publisher*. Click **More info → Run anyway**. You also need the free "
                    "[Npcap](https://npcap.com/#download) driver; the app checks for it and links to it."]
        if platform == "macOS":
            out += ["", "!!! warning \"Unsigned app\"",
                    "    The app is not signed or notarised by Apple yet. The first launch is blocked until you "
                    "allow it: *System Settings → Privacy & Security → Open Anyway* (macOS 15+), or right-click → "
                    "**Open** (macOS 11–14). Requires Apple Silicon and macOS 11 or newer."]
        out += [""]
    out += ["## Verify your download", "",
            "The installers are not code-signed yet, so check that your file is exactly the published one. "
            "Compare its SHA-256 with this table (also in the `SHA256SUMS-*.txt` files of the release):", "",
            "| File | SHA-256 |", "|---|---|"]
    out += [f"| `{r['file']}` | `{r['sha256']}` |" for r in rows]
    out += ["", "```powershell title=\"Windows\"", f"Get-FileHash .\\{rows[0]['file']} -Algorithm SHA256", "```", "",
            "```bash title=\"Linux / macOS\"", "sha256sum <file>        # macOS: shasum -a 256 <file>", "```", "",
            "## System requirements", "",
            "| | Windows | Linux | macOS |", "|---|---|---|---|",
            "| System | Windows 10 or 11, 64-bit | x86_64 with WebKitGTK 4.1 (Ubuntu 22.04+, Debian 12+, Fedora 38+) | macOS 11+, Apple Silicon |",
            "| Capture | [Npcap](https://npcap.com/#download) (free, installed by you) | libpcap | built in |",
            "| Network | HTTPS to the NetPulse AI service | same | same |", ""]
    (ROOT / "docs/download.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    print(f"download page for {tag}: {len(rows)} files, released {date}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "v0.1.0")
