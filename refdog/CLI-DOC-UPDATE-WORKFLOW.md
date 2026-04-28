# CLI-Doc Update Workflow

**Purpose**: Instructions for updating command documentation when Skupper CLI releases a new version.

---

## Overview

When Skupper releases a new version, the CLI help text may change. This guide explains how to update the refdog documentation to reflect those changes.

**Key Principle**: The cli-doc files are the **source of truth** for command documentation. When they update, regenerate the docs automatically.

---

## When to Update

Update refdog documentation whenever:
- ✅ New Skupper CLI version is released
- ✅ CLI commands change (new flags, changed descriptions, etc.)
- ✅ New commands are added
- ✅ Commands are deprecated/removed

---

## Step-by-Step Process

### 1. Update cli-doc Files

**You've already done this!** The cli-doc files are updated from the Skupper CLI repository.

```bash
# This is what you do each release (already done):
# - Copy updated cli-doc/*.md files from skupper repo
# - Or regenerate using: skupper --help-md
```

**Verify the update**:
```bash
# Check how many files you have
ls cli-doc/*.md | wc -l

# Should be 38-40 files (as of 2026-04-27)

# Check a sample to see if it looks current
head -20 cli-doc/skupper_site_create.md
```

---

### 2. Regenerate Documentation

Run the generation script to rebuild all command docs from the updated cli-doc files:

```bash
./plano generate
```

**What happens**:
1. Loads all 38+ cli-doc markdown files
2. Parses each file to extract commands, options, descriptions
3. Merges with metadata (examples, cross-references)
4. Generates 43+ markdown files in `input/commands/`

**Expected output**:
```
plano: notice: Loading cli-doc files...
plano: notice: Loaded 38 cli-doc files
--> generate
plano: notice: Generating resources
plano: notice: Generating commands
plano: notice: Generating input/commands/site/create.md
plano: notice: Generating input/commands/connector/create.md
...
<-- generate
OK (0s)
```

---

### 3. Review Changes

Check what changed in the generated documentation:

```bash
# See which files changed
git status --short input/commands/

# See summary of changes
git diff --stat input/commands/

# Review specific changes (pick a few key commands)
git diff input/commands/site/create.md
git diff input/commands/connector/create.md
git diff input/commands/listener/create.md
```

**What to look for**:

✅ **New options** - CLI added new flags  
✅ **Removed options** - CLI removed flags  
✅ **Changed descriptions** - Help text updated  
✅ **Changed defaults** - Default values changed  
✅ **Changed types** - Option types changed  

❌ **Watch out for**:
- Massive deletions (might indicate parsing error)
- All files unchanged (might mean cli-doc wasn't updated)
- Generation errors (check `plano generate` output)

---

### 4. Handle New/Removed Commands

#### If a NEW command was added:

```bash
# 1. Generate will create the basic file automatically
./plano generate

# 2. Optionally create metadata for richer examples
# (Create config/commands/metadata/<command-name>.yaml)

# Example: config/commands/metadata/site-backup.yaml
cat > config/commands/metadata/site-backup.yaml <<EOF
command: site backup
examples:
  - description: Backup site configuration to a file
    command: skupper site backup my-site.yaml
    output: |
      Site configuration saved to my-site.yaml

related_commands: [site/create, site/update]
related_concepts: [site]
EOF

# 3. Regenerate to include the metadata
./plano generate
```

#### If a command was REMOVED:

```bash
# 1. The generated file will be outdated (cli-doc missing)
# 2. Manually delete the file
rm input/commands/path/to/removed-command.md

# 3. Delete the metadata file if it exists
rm config/commands/metadata/removed-command.yaml

# 4. Update groups.yaml if needed
vim config/commands/groups.yaml
```

---

### 5. Test the Output (Optional)

If you want to verify the generated markdown looks correct:

```bash
# Build the site (if you have transom/jekyll set up)
./plano build

# Or just review the markdown directly
cat input/commands/site/create.md

# Check for common issues:
# - Empty option descriptions
# - Missing types
# - Broken formatting
```

---

### 6. Commit Changes

Commit both the updated cli-doc files AND the regenerated documentation:

```bash
# Add the updated cli-doc files
git add cli-doc/

# Add the regenerated documentation
git add input/commands/

# Add any new metadata files you created
git add config/commands/metadata/

# Commit with descriptive message
git commit -m "Update CLI documentation for Skupper vX.Y.Z

- Updated cli-doc files from skupper vX.Y.Z
- Regenerated command documentation
- Added metadata for new commands: <list>
- Removed deprecated commands: <list>
"
```

---

## Common Scenarios

### Scenario 1: New CLI Option Added

**Example**: Skupper CLI adds `--verbose` flag to `site create`

**What happens automatically**:
1. Updated `cli-doc/skupper_site_create.md` has the new option
2. Run `./plano generate`
3. `input/commands/site/create.md` now includes `--verbose`
4. No manual editing needed!

**Verify**:
```bash
./plano generate
git diff input/commands/site/create.md | grep -A5 "verbose"
```

---

### Scenario 2: CLI Option Removed

**Example**: Skupper CLI removes deprecated `--timeout` flag

**What happens automatically**:
1. Updated `cli-doc/skupper_connector_create.md` no longer has `--timeout`
2. Run `./plano generate`
3. `input/commands/connector/create.md` no longer shows `--timeout`
4. Users can't accidentally use removed option!

**Verify**:
```bash
./plano generate
git diff input/commands/connector/create.md | grep "timeout"
# Should show deletions (lines starting with -)
```

---

### Scenario 3: Command Description Changed

**Example**: Skupper team improves help text for `listener create`

**What happens automatically**:
1. Updated `cli-doc/skupper_listener_create.md` has new description
2. Run `./plano generate`
3. `input/commands/listener/create.md` gets new description
4. Documentation stays current!

**Verify**:
```bash
./plano generate
git diff input/commands/listener/create.md
# Look for changes in the description section
```

---

### Scenario 4: Want Better Examples

**Status**: ⏳ **Phase 2 - Not Yet Implemented**

The cli-doc files have **basic examples** from `skupper <command> --help`.  
Metadata files exist (`config/commands/metadata/*.yaml`) with richer examples, but the code doesn't use them yet.

**Current state**:
- Metadata files were extracted from old YAML
- They contain examples, cross-references, error docs
- The code has helpers to load them (`_get_metadata()`)
- But they're not merged into the output yet

**To enable this** (requires Phase 2 implementation ~2-3 hours):
1. Modify `Command.__init__` to load metadata
2. Merge metadata examples with cli-doc data
3. Test and verify

**For now**: Examples come from cli-doc (basic) or old YAML fallback.

**See [YAML-STATUS.md](YAML-STATUS.md) for details.**

---

## Troubleshooting

### Problem: Generation fails with errors

```
plano: error: Command 'site create': Option 'help' has no type
```

**Solution**: This was fixed in the POC. If you see it, check:
```bash
# Verify cli_parser.py has the default type fix
grep -A3 "Default to boolean" python/cli_parser.py
```

Should show:
```python
else:
    # Default to boolean for flags without explicit type
    option['type'] = 'boolean'
```

---

### Problem: All commands show no changes after cli-doc update

```bash
./plano generate
git diff input/commands/  # Shows nothing
```

**Diagnosis**: cli-doc files might not have actually changed

**Check**:
```bash
# Did cli-doc files actually change?
git diff cli-doc/

# If no changes, the CLI help text is the same
# This is fine! No documentation update needed.
```

---

### Problem: One command fails to parse

```
plano: warning: Command 'debug check' has no cli-doc file
```

**Solution**: This is expected for commands that:
- Are new (no cli-doc yet)
- Are deprecated (cli-doc removed)
- Have different naming

**Action**: The system falls back to YAML automatically. Either:
1. Add the missing cli-doc file manually
2. Keep using YAML for that command
3. Remove the command if it's deprecated

---

### Problem: Choices show as empty in docs

**Example**: `--link-access-type` shows `route`, `loadbalancer` but no descriptions

**This is expected**: cli-doc only has choice names, not descriptions.

**Solution**: Add descriptions in metadata:

```yaml
# config/commands/metadata/site-create.yaml
options:
  link-access-type:
    choices:
      - name: route
        description: Use an OpenShift route. _OpenShift only._
      - name: loadbalancer
        description: Use a Kubernetes load balancer.
```

**Note**: This metadata enhancement is not yet implemented (Phase 2).  
For now, the choices will show with empty descriptions.

---

## Quick Reference

**Every release**:

```bash
# 1. Update cli-doc files (you do this from skupper repo)
cp /path/to/skupper/docs/cli-doc/*.md cli-doc/

# 2. Regenerate documentation
./plano generate

# 3. Review changes
git diff --stat input/commands/
git diff input/commands/site/create.md  # spot check

# 4. Commit
git add cli-doc/ input/commands/
git commit -m "Update CLI docs for Skupper vX.Y.Z"
```

**That's it!** The whole process should take < 5 minutes.

---

## What Gets Updated Automatically

When you run `./plano generate` after updating cli-doc:

✅ Command descriptions (from cli-doc synopsis)  
✅ Command usage syntax (from cli-doc usage)  
✅ Option names (from cli-doc options)  
✅ Option types (from cli-doc options)  
✅ Option defaults (from cli-doc options)  
✅ Option descriptions (from cli-doc options)  
✅ Choices/enums (from cli-doc options)  

❌ **Not updated automatically** (preserved from metadata):  
- Examples (kept from metadata/YAML)  
- Cross-references (kept from metadata/YAML)  
- Error messages (kept from metadata/YAML)  
- Platform notes (kept from metadata/YAML)

---

## Files You Touch

**Every release**:
- `cli-doc/*.md` - Update from skupper repo (you already do this)

**Run every release**:
- `./plano generate` - Regenerates all docs

**Rarely** (special cases only):
- `config/commands/options.yaml` - Shared option definitions (still active)
- `config/commands/groups.yaml` - Command grouping (still active)

**Not yet** (Phase 2 - not implemented):
- `config/commands/metadata/*.yaml` - Prepared but not used yet

**Never touch**:
- `input/commands/*.md` - These are GENERATED, don't edit by hand!
- `python/commands.py` - Generation code, already set up
- `config/commands/*.yaml` - Old command files (fallback only, being phased out)

**See [YAML-STATUS.md](YAML-STATUS.md) for complete details on YAML files.**

---

## Summary

**The new workflow is simpler**:

### Old way (before POC):
1. Update cli-doc files
2. Manually edit config/commands/*.yaml to match
3. Hunt for inconsistencies
4. Run ./plano generate
5. Fix errors
6. Repeat until docs match CLI

### New way (after POC):
1. Update cli-doc files
2. Run `./plano generate`
3. Done! ✅

**The docs automatically stay in sync with the CLI.**

---

## Need Help?

- **Generation errors**: Check `./plano generate` output for clues
- **Missing commands**: Check if cli-doc file exists in `cli-doc/`
- **Wrong output**: Check cli-doc file content matches CLI help text
- **Want enhancements**: Add metadata in `config/commands/metadata/`

Questions? See `POC-RESULTS.md` for technical details.
