# NASA Sky Hub - Agent Instructions

## Project Overview

This is a Home Assistant integration that combines NASA APIs, satellite tracking, and sky visibility calculations into actionable space awareness.

## Key Principles

1. **Always bump version** before committing code changes
2. **Follow Home Assistant standards** - use coordinators, proper entity structure
3. **HACS compatible** - maintain required files and structure
4. **Value-focused documentation** - only document what adds value, keep it in `doc/` folder
5. **Industry standards** - PEP 8, type hints, proper error handling

## Quick Reference

- **Integration code**: `custom_components/nasa_sky_hub/`
- **Documentation**: `doc/` folder
- **Version**: Update in `manifest.json` before every commit
- **Git**: Commit and push after each logical change

## When Making Changes

1. Make code changes
2. Update version in `manifest.json` (e.g., 1.1.5)
3. Test the change
4. **ALWAYS commit immediately**: `git add . && git commit -m "feat: description"`
5. **ALWAYS push immediately**: `git push`
6. **MANDATORY: Create git tag**: `git tag v{VERSION} -m "Version {VERSION}: description"`
7. **MANDATORY: Push tag**: `git push origin v{VERSION}`

## Critical: HACS Version Display

**HACS shows versions from GitHub Releases, NOT git tags or manifest.json!**

**If you skip creating GitHub Releases:**
- ❌ HACS displays commit hashes instead of versions
- ❌ Users can't see version numbers
- ❌ Update system breaks

**Every version bump MUST include:**
1. Version in `manifest.json`
2. Git tag `v{VERSION}` created and pushed
3. **GitHub Release created** (this is what HACS actually reads!)

**GitHub Release Steps:**
- Go to GitHub → Releases → Draft a new release
- Select tag: `v{VERSION}`
- Title: `Version {VERSION}`
- Description: Brief changelog
- Publish release

**Never skip GitHub Release creation - it breaks HACS version display!**

## Critical: No Uncommitted Changes

**After ANY file creation or modification:**
- ✅ Stage changes: `git add .`
- ✅ Commit immediately: `git commit -m "type: description"`
- ✅ Push immediately: `git push`

**Never leave files uncommitted.** If you create or modify files, commit and push them in the same session.

## Code Style

- Use type hints everywhere
- Follow PEP 8 (88 char line length)
- Use async/await for I/O
- Log at appropriate levels
- Never log sensitive data

## Documentation

- Put detailed docs in `doc/` folder
- Keep README.md concise
- Only document non-obvious things
- Include examples for complex setups
- **Never create meta-documentation** (compliance reports, check files, status reports)
- **Never create temporary tracking files** (TODO lists, checklists for docs)
- If checking compliance, use `git status` - don't create files

## Files to Never Create

**Never create these types of files:**
- `*_COMPLIANCE_*.md` - Compliance check reports
- `*_CHECK_*.md` - Status check files  
- `*_REPORT_*.md` - Meta-reports about the project
- `TODO.md`, `CHECKLIST.md` - Temporary tracking files
- Any file that documents "how well we follow rules" rather than "how to use the product"

**Use git commands instead:**
- `git status` - See what changed
- `git diff` - Review changes
- Check rules directly in `.cursor/rules/` - Don't create files to track compliance