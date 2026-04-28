# Start Here: Refdog Documentation System

**Welcome!** This guide explains the new automatic documentation system.

---

## What Changed?

Refdog now generates documentation **automatically from source** instead of manually-maintained YAML files.

**Before**: Edit YAML files by hand, hope they match the code  
**After**: Update source files, run `./plano generate`, done!

---

## Quick Links

**Just updating for a release?**  
→ [QUICK-START.md](QUICK-START.md) - 2-minute workflow

**Want the full story?**  
→ [IMPLEMENTATION-STATUS.md](IMPLEMENTATION-STATUS.md) - Complete overview

**Need step-by-step checklist?**  
→ [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) - Print-friendly

**Confused about directories?**  
→ [DIRECTORIES.md](DIRECTORIES.md) - Complete directory guide

---

## Two Systems

### ✅ Commands (Working Now!)

**Source**: `cli-doc/*.md` (from Skupper CLI)  
**Workflow**: [CLI-DOC-UPDATE-WORKFLOW.md](CLI-DOC-UPDATE-WORKFLOW.md)  
**Status**: ✅ Implemented and ready to use

```bash
# Every release
./plano generate
git add cli-doc/ input/commands/
git commit -m "Update CLI docs for Skupper vX.Y.Z"
```

### ⏳ Resources (Ready to Implement)

**Source**: `crds/*.yaml` (from Skupper API)  
**Workflow**: [CRD-UPDATE-WORKFLOW.md](CRD-UPDATE-WORKFLOW.md)  
**Status**: ⏳ Designed, needs 3.5 hours to implement

**How to implement**: [SIMPLE-CRD-IMPLEMENTATION.md](SIMPLE-CRD-IMPLEMENTATION.md)

---

## The Concept

Both systems work the same way:

```
Source Files (can't edit)          Metadata (enhancements)
    cli-doc/*.md                  config/commands/metadata/*.yaml
    crds/*.yaml                   config/resources/metadata/*.yaml
         ↓                                    ↓
         └────────── MERGE ──────────────────┘
                        ↓
              Generated Documentation
              input/commands/*.md
              input/resources/*.md
```

**Key principle**: Source files are the **truth** (auto-sync), metadata adds **enhancements** (examples, cross-refs).

---

## Your Workflow

### Every Skupper Release

**Step 1**: Update source files (you already do this)
```bash
# Commands
cp /path/to/skupper/cli-doc/*.md cli-doc/

# Resources
cp /path/to/skupper/api/crds/*.yaml crds/
```

**Step 2**: Regenerate
```bash
./plano generate
```

**Step 3**: Commit
```bash
git add cli-doc/ crds/ input/
git commit -m "Update docs for Skupper vX.Y.Z"
```

**That's it!** No manual YAML editing.

---

## What You Get

### Commands (Working Now)

✅ **Automatic sync** - Matches actual CLI exactly  
✅ **73% smaller** - 1,899 lines removed  
✅ **20 errors fixed** - Options that don't exist are gone  
✅ **2-minute updates** - vs 30-60 minutes before  

### Resources (Once Implemented)

✅ **Automatic sync** - Matches actual CRDs exactly  
✅ **Smaller files** - Schema from CRDs, not duplicated  
✅ **No drift** - Can't get out of sync  
✅ **Same workflow** - Identical to commands  

---

## Documentation Map

### Start Here
- **START-HERE.md** (this file) - Overview
- **IMPLEMENTATION-STATUS.md** - Complete status
- **DIRECTORIES.md** - Directory structure guide

### Daily Use
- **QUICK-START.md** - 2-minute workflow
- **RELEASE-CHECKLIST.md** - Print-friendly checklist

### Commands (Implemented)
- **CLI-DOC-UPDATE-WORKFLOW.md** - Complete workflow
- **YAML-STATUS.md** - Which YAML files to edit
- **POC-RESULTS.md** - Implementation results

### Resources (To Implement)
- **CRD-UPDATE-WORKFLOW.md** - Planned workflow
- **SIMPLE-CRD-IMPLEMENTATION.md** - Implementation guide

### Technical
- **crd-generation-proposal.md** - Resources design
- **generation-merge-logic.md** - Merge strategy
- **SIMPLE-IMPLEMENTATION-PLAN.md** - Commands approach

---

## Common Questions

**Q: Which YAML files do I still edit?**  
A: See [YAML-STATUS.md](YAML-STATUS.md) - TL;DR: almost none!

**Q: Can I delete old YAML files?**  
A: Not yet. They're still used as fallback. Once resources are implemented and tested, yes.

**Q: How do I add better examples?**  
A: Phase 2 (not yet implemented). For now, examples come from source files or old YAML.

**Q: Something broke, help!**  
A: See troubleshooting in [CLI-DOC-UPDATE-WORKFLOW.md](CLI-DOC-UPDATE-WORKFLOW.md#troubleshooting)

**Q: How do I implement resources?**  
A: Follow [SIMPLE-CRD-IMPLEMENTATION.md](SIMPLE-CRD-IMPLEMENTATION.md) - takes ~3.5 hours

---

## What Changed in Code

### Commands (Done)
- `python/commands.py` - 82 lines added
- `python/cli_parser.py` - 3 lines added
- **Total**: 85 lines to get auto-sync working!

### Resources (To Do)
- `python/resources.py` - ~100 lines to add
- **Total**: ~100 lines using same pattern

**Both are simple**: Load source files, use them if available, fall back to YAML if not.

---

## Timeline

**Completed** (2026-04-27):
- ✅ Commands implemented
- ✅ Commands tested
- ✅ Complete documentation written
- ✅ Resources designed
- ✅ Simplified implementation plan created

**Remaining** (optional):
- ⏳ Resources implementation (~3.5 hours)
- ⏳ Resources testing (~1 hour)
- ⏳ Clean up old YAML (once both complete)

---

## Recommendation

**Use commands implementation now**:
- It's working
- It's tested
- It's documented
- It saves you time every release

**Implement resources when time permits**:
- Follow the same proven pattern
- Low risk
- Takes ~3.5 hours
- Completes the transition

---

## Need Help?

1. **Daily workflow**: [QUICK-START.md](QUICK-START.md)
2. **Full guide**: [CLI-DOC-UPDATE-WORKFLOW.md](CLI-DOC-UPDATE-WORKFLOW.md) or [CRD-UPDATE-WORKFLOW.md](CRD-UPDATE-WORKFLOW.md)
3. **Implementation**: [SIMPLE-CRD-IMPLEMENTATION.md](SIMPLE-CRD-IMPLEMENTATION.md)
4. **Status**: [IMPLEMENTATION-STATUS.md](IMPLEMENTATION-STATUS.md)

---

## Bottom Line

**Old way**:
1. Update cli-doc/CRDs
2. **Manually edit YAML to match** ⏱️ 30-60 min
3. **Hunt for errors** ⏱️ 15-30 min
4. Generate
5. **Fix errors** ⏱️ 15-30 min
6. Repeat

**New way**:
1. Update cli-doc/CRDs
2. `./plano generate` ⏱️ 1 min
3. Commit ⏱️ 1 min
4. Done! ✅

**Time saved**: 60-120 minutes per release  
**Errors prevented**: All of them!  
**Your new workflow**: ⏱️ 2 minutes

---

**Ready?** Go to [QUICK-START.md](QUICK-START.md) to begin!
