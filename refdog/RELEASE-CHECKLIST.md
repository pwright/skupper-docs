# Release Checklist: Update CLI Documentation

Print this out or bookmark for each Skupper release.

---

## Pre-Flight Check

- [ ] cli-doc files updated from skupper repo
- [ ] Working directory is clean (or commit work first)
- [ ] On correct branch (usually `main` or `deprecration`)

---

## The Process

### 1. Verify cli-doc files updated

```bash
# Check that cli-doc files are present and recent
ls -lt cli-doc/*.md | head -5

# Should show recent timestamps
```

- [ ] cli-doc files have recent dates
- [ ] ~38-40 files present

---

### 2. Regenerate documentation

```bash
./plano generate
```

**Expected output:**
```
plano: notice: Loading cli-doc files...
plano: notice: Loaded 38 cli-doc files
--> generate
...
<-- generate
OK (0s)
```

- [ ] No errors in output
- [ ] Sees "Loaded XX cli-doc files"
- [ ] Completes with "OK"

---

### 3. Review changes

```bash
# Quick check: what files changed?
git status --short input/commands/

# Summary of changes
git diff --stat input/commands/

# Spot-check important commands
git diff input/commands/site/create.md
git diff input/commands/connector/create.md
git diff input/commands/listener/create.md
```

- [ ] Files show modifications (M) not deletions
- [ ] Changes make sense (new options, updated descriptions)
- [ ] No massive unexpected deletions

---

### 4. Test (optional but recommended)

```bash
# Quick sanity check - view a generated file
head -50 input/commands/site/create.md

# Check for:
# - Title looks good
# - Usage syntax looks correct
# - Description makes sense
# - Options are present
```

- [ ] Generated files look correct
- [ ] No obvious formatting issues
- [ ] Options match CLI help text

---

### 5. Commit

```bash
# Add both cli-doc and generated docs
git add cli-doc/ input/commands/

# Commit with version number
git commit -m "Update CLI documentation for Skupper vX.Y.Z

- Updated cli-doc files from skupper vX.Y.Z
- Regenerated command documentation
"

# Push (if ready)
git push origin <branch>
```

- [ ] Both cli-doc/ and input/commands/ committed
- [ ] Commit message includes version number
- [ ] Pushed to remote (if appropriate)

---

## That's It!

Total time: **~2-5 minutes**

---

## Troubleshooting

### If generation fails:

1. Check error message in `./plano generate` output
2. See [CLI-DOC-UPDATE-WORKFLOW.md](CLI-DOC-UPDATE-WORKFLOW.md#troubleshooting)
3. Common issues:
   - Missing cli-doc file → Fall back to YAML (expected)
   - Type error → Check cli_parser.py has default type
   - Import error → Check venv activated

### If no changes appear:

```bash
# Check if cli-doc actually changed
git diff cli-doc/

# If no changes, CLI help text is the same
# This is OK! No doc update needed.
```

### If something looks wrong:

1. Check the specific cli-doc file: `cat cli-doc/skupper_<command>.md`
2. Does it match `skupper <command> --help`?
3. If cli-doc is wrong, regenerate it from skupper CLI
4. If cli-doc is right, file an issue

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Generate docs | `./plano generate` |
| See what changed | `git status --short input/commands/` |
| Review changes | `git diff input/commands/` |
| Spot-check file | `git diff input/commands/site/create.md` |
| Commit both | `git add cli-doc/ input/commands/` |

---

## Need More Help?

- **Quick reference**: [QUICK-START.md](QUICK-START.md)
- **Full guide**: [CLI-DOC-UPDATE-WORKFLOW.md](CLI-DOC-UPDATE-WORKFLOW.md)
- **Technical details**: [POC-RESULTS.md](POC-RESULTS.md)
- **All docs**: [README-CLIDOC.md](README-CLIDOC.md)

---

**Date**: ____________  
**Version**: skupper v______  
**Completed by**: ____________  

---

*Save this checklist for next release!*
