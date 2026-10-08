<!-- Generated from Devbysahilsingh/netpulse-ai docs/maintainer/releasing.md by packaging/sync_website_docs.py. Do not edit here: edit the source and run the script again. -->

# Creating a release and publishing the installer

Follow the [release process](release-process.md); it is the exact procedure. In short:
```powershell
python packaging/bump_version.py X.Y.Z            # Cargo.toml + tauri.conf.json + Cargo.lock
# write the "## [X.Y.Z] - YYYY-MM-DD" section in CHANGELOG.md
git commit -am "Release X.Y.Z"; git push origin main
git tag vX.Y.Z; git push origin vX.Y.Z            # ✅ AUTOMATED: builds every package
python packaging/publish_release.py vX.Y.Z        # 🟠 CURRENTLY MANUAL (until WEBSITE_RELEASE_TOKEN exists): draft release
# test the draft's installer, then:
gh release edit vX.Y.Z --repo Devbysahilsingh/netpulse-website --draft=false --latest   # ✅ site updates itself
```

## Making the draft step automatic (one-time, optional)
`release.yml` already contains the `publish` job. It creates the draft by itself once the private repository has the secret **`WEBSITE_RELEASE_TOKEN`**:
1. GitHub → *Settings → Developer settings → Fine-grained personal access tokens → Generate new token*.
   - **Repository access:** only `Devbysahilsingh/netpulse-website`.
   - **Permissions:** *Contents: Read and write*. Nothing else.
   - **Expiration:** 1 year (put a reminder in your calendar).
2. Store it in the **private** repository (it prompts for the value; never paste it into a file):
   ```powershell
   gh secret set WEBSITE_RELEASE_TOKEN --repo Devbysahilsingh/netpulse-ai
   ```
3. The next tag push creates the draft without `publish_release.py`. Until you have seen that happen once, treat the step as manual.

The token only lets CI write releases on the public repository. It is not a code-signing key or an AWS credential.

---
