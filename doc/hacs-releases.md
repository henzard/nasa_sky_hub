# Creating GitHub Releases for HACS

## Why GitHub Releases Are Required

HACS displays version numbers from **GitHub Releases**, not from git tags or `manifest.json`. Without GitHub Releases, HACS will show commit hashes instead of version numbers.

## Step-by-Step: Creating a GitHub Release

### 1. Prepare Your Version

1. Update version in `manifest.json` (e.g., `1.1.5`)
2. Commit and push your changes
3. Create and push git tag:
   ```bash
   git tag v1.1.5 -m "Version 1.1.5: description"
   git push origin v1.1.5
   ```

### 2. Create GitHub Release

1. **Go to your GitHub repository**
2. **Click "Releases"** (right sidebar, or go to `https://github.com/USERNAME/nasa_sky_hub/releases`)
3. **Click "Draft a new release"** (or "Create a new release")
4. **Select tag**: Choose `v1.1.5` (must match your manifest.json version)
5. **Release title**: `Version 1.1.5` or `v1.1.5`
6. **Description**: Brief changelog, for example:
   ```
   ## Changes
   - Fixed ConfigEntryNotReady errors
   - Improved error handling in coordinators
   - Added comprehensive logging
   ```
7. **Click "Publish release"**

### 3. Verify in HACS

1. Go to HACS in Home Assistant
2. Click three dots (⋮) → "Update information"
3. Check that version shows as `v1.1.5` instead of commit hash

## Quick Checklist

- [ ] Version updated in `manifest.json`
- [ ] Code committed and pushed
- [ ] Git tag created: `git tag v{VERSION}`
- [ ] Tag pushed: `git push origin v{VERSION}`
- [ ] GitHub Release created using the tag
- [ ] Release published on GitHub
- [ ] HACS refreshed to show new version

## Common Issues

**HACS still shows commit hash:**
- Make sure GitHub Release is published (not draft)
- Refresh HACS: three dots → "Update information"
- Verify tag matches release tag exactly

**Release not appearing:**
- Check tag was pushed: `git push origin v{VERSION}`
- Wait a few minutes for GitHub to sync
- Try refreshing HACS again

## Automation (Future)

For now, GitHub Releases must be created manually. In the future, you could:
- Use GitHub Actions to auto-create releases
- Use release automation tools
- But manual creation ensures you control what's released
