---
description: "Version management and git workflow standards"
alwaysApply: true
---

# Version and Git Workflow Rules

## Version Bumping

- **Always bump version** in `custom_components/nasa_sky_hub/manifest.json` before committing changes
- Use semantic versioning: `MAJOR.MINOR.PATCH`
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes, small improvements
- Update version in `manifest.json` before every commit that changes code

## Git Workflow

- **ALWAYS commit changes immediately** - Never leave uncommitted changes
- **Commit after each logical change** - don't batch unrelated changes
- **Commit message format**: `feat: description` or `fix: description` or `docs: description`
- **ALWAYS push immediately after committing** - use `git push` right after `git commit`
- **Never leave files uncommitted** - If you create or modify files, commit them in the same session
- **Check git status** before committing to ensure only intended files are staged

## Critical Rule: No Uncommitted Changes

**After making ANY changes:**
1. ✅ Check what changed: `git status`
2. ✅ Stage changes: `git add .` (or specific files)
3. ✅ Commit immediately: `git commit -m "type: description"`
4. ✅ Push immediately: `git push`

**Never:**
- ❌ Leave files uncommitted
- ❌ Create files without committing them
- ❌ Make changes and forget to commit
- ❌ Commit without pushing

**If you see uncommitted changes at the end of a session, commit and push them before finishing.**

## Pre-Commit Checklist

Before committing:
1. ✅ Version bumped in `manifest.json`
2. ✅ Code follows HA standards
3. ✅ No syntax errors
4. ✅ All changes are intentional
5. ✅ Commit message is clear and descriptive
6. ✅ No temporary/compliance files created (check git status)

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

## Example Workflow

```bash
# 1. Make changes
# 2. Update version in manifest.json
# 3. Stage changes
git add .
# 4. Commit with clear message
git commit -m "feat: add comprehensive logging to coordinators"
# 5. Push immediately
git push
```
