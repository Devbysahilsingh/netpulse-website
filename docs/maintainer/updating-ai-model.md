<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/updating-ai-model.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Updating the AI model

The model is **not** in any installer. Changing it needs no app release. Model versions are MLflow registry versions (`NetPulse-IDS` v1, v2, …), not app versions.

🔒 Publishing to S3 changes what every user gets: do it deliberately. Cost is negligible (a ~10 MB upload).

```powershell
cd U:\Projects\NetPulse-AI
conda activate eda-env
git status                                   # must be clean: training refuses uncommitted code
dvc repro evaluate                           # data → train → register (@challenger) → evaluate + quality gate
Get-Content reports\metrics\quality_gate.json   # "passed": true ?  If false: STOP. Never loosen a threshold.
python -m ml.tracking.registry promote --version N --gate reports/metrics/quality_gate.json
python -m ml.export.bundle export --alias production        # verified bundle in artifacts\bundles\N
python -m ml.export.bundle activate --version N             # serve it locally first; test with the local server ([Local development](local-development.md))
```

Publish to AWS (the Lambda picks it up within 60 s; no redeploy):
```powershell
python -m ml.common.aws preflight                           # must print OK for the NetPulse-AI account
$env:NETPULSE_AWS_ACCOUNT_ID = (Select-String infrastructure\aws\terraform.tfvars -Pattern 'allowed_account_ids\s*=\s*\["(\d{12})"\]').Matches[0].Groups[1].Value
$bucket = terraform -chdir=infrastructure\aws output -raw artifacts_bucket
python -m ml.export.s3_publish status  --bucket $bucket --profile default      # what is live now
python -m ml.export.s3_publish publish --version N --bucket $bucket --profile default
```

Verify ([Updating AWS](updating-aws.md), *Verify the API*): `/v1/health` must report `"model_version":"N"` within about a minute, and a `netpulse scan --pcap` of a known capture must give sensible labels.

**Rollback a model:** `python -m ml.export.s3_publish rollback --bucket $bucket --profile default` swaps `active` and `previous` in `active.json`. Note that **today `previous` is empty**: v2 is the only model ever published, because v1 failed the gate. So rollback becomes possible after the next publish. The local registry has its own rollback: `python -m ml.tracking.registry rollback`.

**Schema rule:** if a new model needs different features, that is a new feature schema version and needs a client release first ([Versioning](versioning.md), MAJOR or MINOR). Never publish a model trained on a schema the released clients do not send.

---
