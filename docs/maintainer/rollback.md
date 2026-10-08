<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/rollback.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Rollback

| What went wrong | Rollback | Time |
|---|---|---|
| A new **app release** is broken | **Never delete or replace a published release's files.** Users and checksums depend on them. Release a fixed PATCH (`vX.Y.Z+1`) the normal way. If users must not download the broken one meanwhile, mark the previous release as latest: `gh release edit vPREVIOUS --repo Devbysahilsingh/netpulse-website --latest`. The site rebuilds and offers it. Optionally change the broken one to a pre-release: `gh release edit vBROKEN --repo Devbysahilsingh/netpulse-website --prerelease`. | minutes |
| A new **model** misbehaves | `python -m ml.export.s3_publish rollback --bucket $bucket --profile default` (needs a `previous`; see [Updating the AI model](updating-ai-model.md)). Live within 60 s; no client change | 1 minute |
| A new **inference image** fails | Set `image_tag` back to the previous ECR tag, then `terraform plan -out` / `apply` | 5 minutes |
| A **Terraform** change broke something | Revert the `.tf` change in git, then `plan -out` / `apply` | 5–10 minutes |
| **Website** broken | `git revert <commit>` in `netpulse-website`, push. Or re-run the last good deploy: `gh run rerun <run-id> --repo Devbysahilsingh/netpulse-website` | 2 minutes |
