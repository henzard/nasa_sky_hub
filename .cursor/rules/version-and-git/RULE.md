---
description: "Version management and git workflow standards"
alwaysApply: true
---

# Version and Git Workflow Rules

## Version Bumping - CRITICAL FOR HACS

- **Only bump version for code changes** - NOT for documentation, rules, or non-code files
- **Bump version** in `custom_components/nasa_sky_hub/manifest.json` before committing code changes
- Use semantic versioning: `MAJOR.MINOR.PATCH`
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes, small improvements
- **When to bump version:**
  - ✅ Code changes in `custom_components/nasa_sky_hub/` (Python files)
  - ✅ Changes to `manifest.json` itself (requirements, dependencies)
  - ✅ Changes to `hacs.json` (HACS metadata)
  - ❌ Documentation changes (`doc/`, `README.md`)
  - ❌ Rule changes (`.cursor/rules/`, `AGENTS.md`)
  - ❌ Lovelace dashboard/card changes (`lovelace/`)
- **MANDATORY: Create git tag** after pushing code changes: `git tag v{VERSION} -m "Version {VERSION}: {description}"`
- **MANDATORY: Push tag**: `git push origin v{VERSION}` (HACS REQUIRES tags for version display)
- **Version in manifest.json MUST match git tag** (e.g., manifest "1.1.4" = tag "v1.1.4")

## HACS Version Display Requirements

**HACS displays versions from git tags, NOT from manifest.json!**

Without git tags:
- ❌ HACS shows commit hashes (e.g., "4b79009") instead of versions
- ❌ Users can't see what version they're running
- ❌ Update notifications don't work properly

**Every version bump MUST include:**
1. Update `manifest.json` version
2. Commit and push code
3. Create git tag: `git tag v{VERSION}`
4. Push tag: `git push origin v{VERSION}`

**Never skip tagging - it breaks HACS version display!**

## Git Workflow

- **ALWAYS commit changes immediately** - Never leave uncommitted changes
- **Commit after each logical change** - don't batch unrelated changes
- **Commit message format**: `feat: description` or `fix: description` or `docs: description`
- **ALWAYS push immediately after committing** - use `git push` right after `git commit`
- **Never leave files uncommitted** - If you create or modify files, commit them in the same session
- **Check git status** before committing to ensure only intended files are staged

## Critical Rule: No Uncommitted Changes + Mandatory Tagging

**After making ANY changes:**
1. ✅ Check what changed: `git status`
2. ✅ Update version in `manifest.json` (if code changed)
3. ✅ Stage changes: `git add .` (or specific files)
4. ✅ Commit immediately: `git commit -m "type: description"`
5. ✅ Push immediately: `git push`
6. ✅ **Create git tag**: `git tag v{VERSION} -m "Version {VERSION}: description"`
7. ✅ **Push tag**: `git push origin v{VERSION}` (REQUIRED for HACS)

**Never:**
- ❌ Leave files uncommitted
- ❌ Create files without committing them
- ❌ Make changes and forget to commit
- ❌ Commit without pushing
- ❌ **Push code without creating/pushing git tag** (breaks HACS version display)
- ❌ **Skip tagging** (HACS needs tags to show versions)

**If you see uncommitted changes at the end of a session, commit, push, AND tag before finishing.**

## Pre-Commit Checklist

Before committing:
1. ✅ **Version bumped in `manifest.json`** (ONLY if code changed, NOT for docs/rules)
2. ✅ Code follows HA standards
3. ✅ No syntax errors
4. ✅ All changes are intentional
5. ✅ Commit message is clear and descriptive
6. ✅ No temporary/compliance files created (check git status)

## When to Bump Version

**Bump version for:**
- ✅ Code changes in `custom_components/nasa_sky_hub/*.py`
- ✅ Changes to `manifest.json` (requirements, dependencies)
- ✅ Changes to `hacs.json` (HACS metadata)

**DO NOT bump version for:**
- ❌ Documentation changes (`doc/`, `README.md`)
- ❌ Rule changes (`.cursor/rules/`, `AGENTS.md`)
- ❌ Lovelace dashboards/cards (`lovelace/`)
- ❌ Git workflow improvements
- ❌ Comments or formatting only

## Post-Push Checklist (MANDATORY)

After pushing code:
1. ✅ **Create git tag**: `git tag v{VERSION} -m "Version {VERSION}: description"`
2. ✅ **Push tag**: `git push origin v{VERSION}`
3. ✅ **Create GitHub Release** (MANDATORY - HACS reads releases, not tags!):
   - Go to GitHub repository → Releases → Draft a new release
   - Select tag: `v{VERSION}`
   - Title: `Version {VERSION}` or `v{VERSION}`
   - Description: Brief changelog
   - Click "Publish release"
4. ✅ Verify release exists: Check GitHub Releases page

**If you forget to create GitHub Release, HACS will show commit hashes instead of version numbers!**

## Files to Never Commit

**Never commit these types of files:**
- Compliance check reports (`*_COMPLIANCE_*.md`)
- Status reports (`*_REPORT_*.md`, `*_CHECK_*.md`)
- Temporary tracking files (`TODO.md`, `CHECKLIST.md`)
- Meta-documentation about the project itself

**Use git commands to check status, don't create files:**
- `git status` - See what changed
- `git diff` - See differences
- `git log` - See commit history

## Example Workflow (COMPLETE - Never Skip Steps)

```bash
# 1. Make changes to code
# 2. Update version in manifest.json (e.g., 1.1.5)
# 3. Stage changes
git add .
# 4. Commit with clear message
git commit -m "feat: add comprehensive logging to coordinators"
# 5. Push immediately
git push
# 6. MANDATORY: Create git tag
git tag v1.1.5 -m "Version 1.1.5: add comprehensive logging to coordinators"
# 7. MANDATORY: Push tag
git push origin v1.1.5
# 8. MANDATORY: Create GitHub Release (HACS REQUIRES THIS!)
#    - Go to GitHub → Releases → Draft a new release
#    - Select tag: v1.1.5
#    - Title: "Version 1.1.5"
#    - Description: "add comprehensive logging to coordinators"
#    - Publish release
```

**Note:** GitHub Releases must be created manually on GitHub website. Git tags alone are NOT enough!

## HACS Version Display - CRITICAL

**HACS displays versions from GitHub Releases, NOT from git tags or manifest.json!**

**If you skip creating GitHub Releases:**
- ❌ HACS shows commit hashes (e.g., "4b79009", "ab5d6ba")
- ❌ Users can't tell what version they have
- ❌ Update notifications break
- ❌ Version comparison fails

**HACS Requirements (ALL must be done):**
1. ✅ Update version in `manifest.json`
2. ✅ Create git tag: `git tag v{VERSION}`
3. ✅ Push tag: `git push origin v{VERSION}`
4. ✅ **Create GitHub Release** using the tag (MANDATORY - this is what HACS reads!)

**GitHub Release Steps:**
1. Go to GitHub repository → "Releases" → "Draft a new release"
2. Select tag: `v{VERSION}` (must match manifest.json version)
3. Release title: `Version {VERSION}` or `v{VERSION}`
4. Description: Brief changelog or description
5. Click "Publish release"

**Every single version bump MUST include:**
1. Version update in `manifest.json`
2. Git tag creation and push
3. **GitHub Release creation** (this is what HACS actually uses!)

**Without GitHub Releases, HACS will show commit hashes instead of versions!**
