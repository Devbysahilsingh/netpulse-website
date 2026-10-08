<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/troubleshooting.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Troubleshooting (maintainers)

| Symptom | Cause / fix |
|---|---|
| `release.yml` fails at *tag matches the app version* | You tagged without bumping. Delete the tag (`git push origin :refs/tags/vX.Y.Z; git tag -d vX.Y.Z`), bump, commit, re-tag. Allowed only while nothing has been published for that tag. |
| macOS job: `No matching IconType` | `icon.icns` missing from `tauri.conf.json` `bundle.icon` |
| `publish_release.py`: `missing release files` | A package job failed or was skipped; re-run it: `gh run rerun <run-id> --failed --repo Devbysahilsingh/netpulse-ai` |
| `publish_release.py`: `no '## [X.Y.Z]' section` | Write the CHANGELOG section, commit, push. The tag does not need to move, because the script reads the CHANGELOG from your working copy. |
| Pages build fails at `gen_downloads.py` | No published release yet, a missing SHA256SUMS entry, or a broken asset link. The error names it. |
| Pages build fails in `mkdocs build --strict` | A broken link or anchor in `docs/`. The log names the file. |
| Pages **deploy** job fails after a release event (*"Tag vX.Y.Z is not allowed to deploy to github-pages"*) | The `github-pages` environment must allow tags `v*` as well as `main`. This was set up once on 2026-10-08. If it is ever lost: `gh api -X POST repos/Devbysahilsingh/netpulse-website/environments/github-pages/deployment-branch-policies -f name='v*' -f type=tag`, then `gh workflow run pages.yml --repo Devbysahilsingh/netpulse-website` |
| Users get 401 | SSM token list wrong or missing: check `aws logs tail … --filter-pattern agent_tokens_unavailable`; restore with `put-parameter` from `server\.secrets\aws_agent_tokens.json` |
| Users get "AI service unavailable" | `curl $api/v1/health`. `503`: no verified model, so check `s3_publish status`. Timeout: check the Lambda logs and the AWS Health Dashboard. |
| Windows build is slow (~35 min) on a fresh cache | It compiles the Tauri CLI once; later runs reuse the cache |
