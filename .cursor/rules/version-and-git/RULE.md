---
description: "Version management and git workflow standards"
alwaysApply: true
---

# Version and Git Workflow Rules

## Version Bumping - CRITICAL FOR HACS

- **Always bump version** in `custom_components/nasa_sky_hub/manifest.json` before committing changes
- Use semantic versioning: `MAJOR.MINOR.PATCH`
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes, small improvements
- Update version in `manifest.json` before every commit that changes code
- **MANDATORY: Create git tag** after pushing: `git tag v{VERSION} -m "Version {VERSION}: {description}"`
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
1. ✅ Version bumped in `manifest.json`
2. ✅ Code follows HA standards
3. ✅ No syntax errors
4. ✅ All changes are intentional
5. ✅ Commit message is clear and descriptive
6. ✅ No temporary/compliance files created (check git status)

## Post-Push Checklist (MANDATORY)

After pushing code:
1. ✅ **Create git tag**: `git tag v{VERSION} -m "Version {VERSION}: description"`
2. ✅ **Push tag**: `git push origin v{VERSION}`
3. ✅ Verify tag exists: `git tag -l` (should show `v{VERSION}`)
4. ✅ Verify tag pushed: Check GitHub tags page

**If you forget to tag, HACS will show commit hashes instead of version numbers!**

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
# 6. MANDATORY: Create git tag (HACS REQUIRES THIS)
git tag v1.1.5 -m "Version 1.1.5: add comprehensive logging to coordinators"
# 7. MANDATORY: Push tag (HACS REQUIRES THIS)
git push origin v1.1.5
```

## HACS Version Display - CRITICAL

**HACS displays versions from git tags ONLY, NOT from manifest.json!**

**If you skip tagging:**
- ❌ HACS shows commit hashes (e.g., "4b79009", "ab5d6ba")
- ❌ Users can't tell what version they have
- ❌ Update notifications break
- ❌ Version comparison fails

**Tag requirements:**
- Tag format: `v{VERSION}` (e.g., `v1.1.5` - must match manifest.json exactly)
- Tag message: `"Version {VERSION}: {description}"`
- Push tag: `git push origin v{VERSION}` (MANDATORY)

**Every single version bump MUST include both:**
1. Version update in `manifest.json`
2. Git tag creation and push

**This is not optional - HACS breaks without tags!**
