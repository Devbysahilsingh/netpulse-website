<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/versioning.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Versioning

Semantic versioning, `MAJOR.MINOR.PATCH`, tags `v0.1.0`, `v0.1.1`, `v0.2.0`, `v1.0.0`. The version is **one number for the whole product**: CLI, desktop app, installers, tag. `bump_version.py` keeps them identical; `release.yml` refuses a tag that differs from `Cargo.toml`.

| Increment | When | Examples |
|---|---|---|
| **PATCH** `0.1.0 → 0.1.1` | Bug fixes and wording; no new feature; config, CLI output and JSON stay compatible | fix a crash, fix a typo on Home, dependency security update |
| **MINOR** `0.1.1 → 0.2.0` | New features, still compatible with existing configs, scripts and the `/v1` API | a new CLI command, a new Home screen, a new option with a default |
| **MAJOR** `0.x → 1.0.0`, `1.x → 2.0.0` | Breaking changes: config keys renamed/removed, CLI JSON fields removed, exit codes changed, a new feature schema (needs a new API version), dropping an OS | `1.0.0` = the first release you promise to keep stable |

While the version is `0.x`, a MINOR may contain small breaking changes, but list them under *Changed* in the CHANGELOG. **AI model versions (v1, v2, …) are independent** of app versions. A new model alone is not an app release ([Updating the AI model](updating-ai-model.md)).

---
