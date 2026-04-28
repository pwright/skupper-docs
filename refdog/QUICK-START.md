# Quick Start: CLI Update Workflow

**TL;DR**: When you update cli-doc files, just run `./plano generate`

---

## Every Release (2 minutes)

```bash
# 1. You already updated cli-doc files from skupper repo
# (This is what you just did)

# 2. Regenerate all command documentation
./plano generate

# 3. Check what changed
git status --short input/commands/

# 4. Spot-check a few files
git diff input/commands/site/create.md

# 5. Commit everything
git add cli-doc/ input/commands/
git commit -m "Update CLI docs for Skupper vX.Y.Z"
```

---

## That's It!

The documentation **automatically syncs** with the CLI.

- ✅ New options appear automatically
- ✅ Removed options disappear automatically  
- ✅ Changed descriptions update automatically
- ✅ No manual YAML editing needed

---

## Only If You Need More

**Add rich examples** (Phase 2 - not yet implemented):

```bash
# Metadata files exist but aren't used yet
# See YAML-STATUS.md for details
# Phase 2 will enable this feature
```

**See full details**: `CLI-DOC-UPDATE-WORKFLOW.md`

---

## What Changed vs Old System

### Before (painful):
1. Update cli-doc
2. **Manually update YAML files to match**
3. **Hunt for inconsistencies**
4. Generate
5. **Fix errors**
6. Repeat

### Now (automatic):
1. Update cli-doc
2. Generate
3. Done ✅

---

## Files

- **Update**: `cli-doc/*.md` (from skupper repo)
- **Run**: `./plano generate`
- **Commit**: `cli-doc/` and `input/commands/`
- **Never edit**: `input/commands/*.md` (auto-generated!)
