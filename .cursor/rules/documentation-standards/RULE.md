---
description: "Documentation standards - value-focused docs in doc folder"
alwaysApply: true
---

# Documentation Standards

## Documentation Location

- **All documentation** goes in `doc/` folder
- **README.md** stays in root (required for GitHub/HACS)
- **Only document things that add value** - avoid redundant or obvious documentation

## What to Document

✅ **DO Document:**
- Setup/installation procedures
- Configuration examples
- Troubleshooting guides
- API/service usage
- Architecture decisions
- Common issues and solutions
- Dashboard/card examples

❌ **DON'T Document:**
- Obvious code comments (self-explanatory code)
- Redundant information already in code
- Overly verbose explanations of simple concepts
- Documentation that duplicates README.md
- **Meta-documentation** (files about the project itself, compliance reports, checklists)
- **Temporary files** (compliance checks, status reports, TODO lists for documentation)
- **Self-referential docs** (files that document the documentation process)

## Files to Never Create

**Never create these types of files:**
- `*_COMPLIANCE_*.md` - Compliance check reports
- `*_CHECK_*.md` - Status check files
- `*_REPORT_*.md` - Meta-reports about the project
- `TODO.md`, `CHECKLIST.md` - Temporary tracking files
- Any file that documents "how well we follow rules" rather than "how to use the product"

**If you need to check compliance:**
- Use git status/diff
- Check rules directly in `.cursor/rules/`
- Don't create files to track this

## Documentation Structure

```
doc/
├── installation.md      # Detailed installation steps
├── configuration.md     # Configuration options
├── troubleshooting.md   # Common issues and fixes
├── dashboards.md        # Dashboard setup guides
└── api-reference.md     # Service/API documentation
```

## Documentation Format

- Use clear headings and structure
- Include code examples where helpful
- Use checklists for step-by-step procedures
- Add screenshots when they clarify concepts
- Keep each doc focused on one topic

## README.md Rules

- Keep README.md concise and high-level
- Link to detailed docs in `doc/` folder
- Include quick start guide
- List key features
- Provide installation overview (details in `doc/installation.md`)

## Code Comments

- Only comment code that's not self-explanatory
- Explain "why" not "what" (code shows what)
- Remove obvious comments like `# Set variable to 5`
- Keep comments up-to-date with code changes

## Example Good Documentation

```markdown
# Troubleshooting Entity Not Found

## Problem
Entities show "Entity not found" after installation.

## Solution
1. Verify integration is configured (Settings → Devices & Services)
2. Check modules are enabled
3. Restart Home Assistant
4. Wait 2-3 minutes for first data fetch
```

## Example Bad Documentation

```markdown
# How to Click a Button
This document explains how to click a button. 
First, move your mouse over the button. 
Then click the left mouse button.
```
