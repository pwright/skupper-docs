# YAML Files Status

**Important**: There are TWO sets of YAML files. Here's what they are and which ones matter.

---

## Current State (After POC)

### 1. OLD YAML Files (Still Active as Fallback)

**Location**: `config/commands/*.yaml`  
**Status**: ✅ **Still used** (as fallback when cli-doc missing)  
**Count**: 10 files

**Files**:
- `connector.yaml` - Old format, fallback only
- `debug.yaml` - Old format, fallback only  
- `link.yaml` - Old format, fallback only
- `listener.yaml` - Old format, fallback only
- `site.yaml` - Old format, fallback only
- `system.yaml` - Old format, fallback only
- `token.yaml` - Old format, fallback only
- `version.yaml` - Old format, fallback only
- `options.yaml` - ✅ **Still actively used** (shared options)
- `groups.yaml` - ✅ **Still actively used** (command grouping)

**What they do now**:
- Fallback if cli-doc file is missing
- Provide shared options (`options.yaml`)
- Define command groups (`groups.yaml`)

**Should you edit them?**
- ❌ **No** - Don't edit the command files (connector.yaml, site.yaml, etc.)
- ✅ **Yes** - `options.yaml` and `groups.yaml` are still used

---

### 2. NEW Metadata Files (Prepared but NOT Used Yet)

**Location**: `config/commands/metadata/*.yaml`  
**Status**: ⏳ **Extracted but NOT implemented** (Phase 2 work)  
**Count**: 30 files

**Files**: `site-create.yaml`, `connector-create.yaml`, etc.

**What they're for**:
- Enhanced examples (richer than cli-doc)
- Cross-references (links to concepts/resources)
- Error documentation
- Option grouping hints

**Should you edit them?**
- ⏳ **Not yet** - They're not being used by the code yet
- They're ready for Phase 2 (when we implement metadata merging)

---

## How It Works Right Now

### Priority Order (Current Implementation)

```
For each command:
  1. Try cli-doc/*.md (38 files) ← PRIMARY
  2. Fall back to config/commands/*.yaml (old YAML) ← FALLBACK
  3. config/commands/metadata/*.yaml ← NOT USED YET
```

**In code** (`python/commands.py`):
```python
if cli_doc and cli_doc.get("options"):
    # Use cli-doc (MOST COMMANDS - 38 of them)
    option_data_list = cli_doc.get("options", [])
else:
    # Fall back to old YAML (FEW COMMANDS - only if cli-doc missing)
    option_data_list = self.merge_option_data()  # Reads old YAML

# Metadata is NOT checked yet (Phase 2)
```

---

## What Gets Used When?

### Scenario 1: Command has cli-doc (38 commands)

```
site create:
  ✅ Uses: cli-doc/skupper_site_create.md
  ❌ Ignores: config/commands/site.yaml (old)
  ❌ Ignores: config/commands/metadata/site-create.yaml (not implemented)
```

### Scenario 2: Command missing cli-doc (1 command)

```
debug check:
  ❌ No cli-doc file exists
  ✅ Uses: config/commands/debug.yaml (fallback)
  ❌ Ignores: config/commands/metadata/debug-check.yaml (not implemented)
```

### Scenario 3: Shared options (all commands)

```
All commands:
  ✅ Use: config/commands/options.yaml (still active)
  ✅ Use: config/commands/groups.yaml (still active)
```

---

## What You Should Edit (Current System)

### ✅ Edit These (Still Active)

**`config/commands/options.yaml`** - Shared options across commands
```yaml
# Example: Global options like --context, --namespace
global/*:
  context:
    name: context
    type: string
    description: Set the kubeconfig context
```

**`config/commands/groups.yaml`** - Command grouping for index
```yaml
- title: Primary commands
  objects: [site, link, listener, connector]
```

**`cli-doc/*.md`** - Primary source (you update from skupper repo)

---

### ❌ Don't Edit These (Being Phased Out)

**`config/commands/connector.yaml`** - Old command definitions  
**`config/commands/site.yaml`** - Old command definitions  
**`config/commands/listener.yaml`** - Old command definitions  
etc.

**Why?** These are only used as fallback. cli-doc is the source of truth now.

---

### ⏳ Not Used Yet (Phase 2)

**`config/commands/metadata/*.yaml`** - Enhanced metadata

These files exist (extracted from old YAML) but the code doesn't load them yet.

**Phase 2 will implement**:
```python
# Get metadata for enhanced examples
metadata = self._get_metadata()  # This helper exists but isn't called yet
if metadata and metadata.get("examples"):
    self.enhanced_examples = metadata["examples"]
```

---

## Your Workflow (Current System)

### Every Release

```bash
# 1. Update cli-doc (you already do this)
cp /path/to/skupper/cli-doc/*.md cli-doc/

# 2. Regenerate
./plano generate

# 3. Commit
git add cli-doc/ input/commands/
git commit -m "Update CLI docs for Skupper vX.Y.Z"
```

**Don't touch**:
- ❌ Old YAML (config/commands/*.yaml) - being phased out
- ❌ Metadata YAML (config/commands/metadata/*.yaml) - not used yet

**OK to touch**:
- ✅ cli-doc files (primary source)
- ✅ options.yaml (shared options)
- ✅ groups.yaml (command grouping)

---

## Future: Phase 2 (Not Implemented Yet)

When Phase 2 is implemented, the priority will change to:

```
For each command:
  1. cli-doc/*.md ← Technical facts (options, types, defaults)
  2. metadata/*.yaml ← Enhancements (examples, descriptions)
  3. Old YAML ← Removed completely
```

**Benefits of Phase 2**:
- Rich examples from metadata
- Enhanced descriptions
- Cross-references
- Error documentation
- No more old YAML

**Estimated effort**: 2-3 hours to implement

---

## Clean-Up Plan (Future)

Once metadata integration is implemented (Phase 2):

### Step 1: Verify metadata is being used
```bash
./plano generate
# Check that examples from metadata/*.yaml appear in output
```

### Step 2: Remove old YAML
```bash
# Remove old command definitions (keep options.yaml and groups.yaml)
rm config/commands/connector.yaml
rm config/commands/debug.yaml
rm config/commands/link.yaml
rm config/commands/listener.yaml
rm config/commands/site.yaml
rm config/commands/system.yaml
rm config/commands/token.yaml
rm config/commands/version.yaml
```

### Step 3: Update code
```python
# Remove fallback to old YAML in commands.py
# Only use cli-doc + metadata
```

**Don't do this yet!** Old YAML is still the fallback.

---

## Summary Table

| YAML Files | Location | Status | Edit? | Used For |
|------------|----------|--------|-------|----------|
| **Old command YAML** | `config/commands/*.yaml` | ⚠️ Fallback | ❌ No | Fallback when cli-doc missing |
| **options.yaml** | `config/commands/options.yaml` | ✅ Active | ✅ Yes | Shared options definitions |
| **groups.yaml** | `config/commands/groups.yaml` | ✅ Active | ✅ Yes | Command grouping |
| **Metadata YAML** | `config/commands/metadata/*.yaml` | ⏳ Prepared | ⏳ Not yet | Phase 2 (not implemented) |

---

## Questions & Answers

**Q: Can I delete the old YAML files (connector.yaml, site.yaml, etc.)?**  
A: Not yet. They're still used as fallback. Delete after Phase 2.

**Q: Should I edit metadata/*.yaml files?**  
A: Not yet. The code doesn't read them yet. Wait for Phase 2.

**Q: What if I want better examples NOW?**  
A: Currently, examples come from old YAML as fallback. To change them, you'd have to edit the old YAML (not recommended) or wait for Phase 2.

**Q: Which YAML files do I touch every release?**  
A: None! Just update cli-doc and regenerate. YAML files are static.

**Q: What about options.yaml and groups.yaml?**  
A: These are still active and can be edited (rarely needed).

---

## Bottom Line

**Current state**:
- ✅ cli-doc is primary source (38 commands)
- ⚠️ Old YAML is fallback (1 command + shared options)
- ⏳ Metadata YAML exists but not used

**Your action**:
- ✅ Update cli-doc each release
- ✅ Run `./plano generate`
- ❌ Don't edit old YAML command files
- ❌ Don't edit metadata files yet (Phase 2)

**Simple, right?** You only touch cli-doc files. Everything else stays static.
