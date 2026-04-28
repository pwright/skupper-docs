# Simple Implementation Plan: CRD Integration

**Goal**: Replace current YAML-based resource docs with CRD + metadata in the simplest way possible.

**Strategy**: Follow the exact same pattern we used for commands. Make minimal changes, test with ONE resource, then expand.

---

## Why This Will Be Easy

We already did this for commands! The pattern is identical:

| Commands | Resources |
|----------|-----------|
| cli-doc/*.md | crds/*.yaml |
| Cobra-generated | Skupper-generated |
| Can't edit (source of truth) | Can't edit (source of truth) |
| 38 files | 9 files |
| Metadata prepared ✅ | Metadata prepared ✅ |
| Implemented ✅ | Not implemented ⏳ |

**It's the same approach, just parsing CRD YAML instead of cli-doc markdown.**

---

## Current System (What We're Replacing)

```
config/resources/*.yaml  →  python/resources.py  →  input/resources/*.md
     (everything)             (generation)             (output)
```

**Problem**: YAML has everything (schema, descriptions, examples). Gets out of sync with actual CRDs.

---

## New System (What We're Building)

```
crds/*.yaml (CRD truth)  ─┐
                          ├─→  python/resources.py  →  input/resources/*.md
metadata/*.yaml (extras) ─┘     (merge + generate)       (output)
```

**Better**: CRDs are authoritative for schema, metadata adds documentation enhancements.

---

## The Simplest Possible Implementation

### Phase 1: Add CRD Loading (30 minutes)

**File**: `python/resources.py`

**Change 1**: Add CRD loader at top

```python
import yaml

def load_crd(crd_file):
    """Load and parse a CRD file."""
    with open(crd_file) as f:
        crd = yaml.safe_load(f)
    return crd
```

**Change 2**: Add to `ResourceModel.__init__` (after line 148)

```python
class ResourceModel(Model):
    def __init__(self):
        super().__init__(Resource, "config/resources")
        
        self.property_data = read_yaml(join(self.config_dir, "properties.yaml"))
        
        # NEW: Load CRD files
        self.crds = {}
        crd_dir = "crds"
        if os.path.exists(crd_dir):
            notice("Loading CRD files...")
            for crd_file in list_dir(crd_dir):
                if crd_file.endswith("_crd.yaml"):
                    path = join(crd_dir, crd_file)
                    crd = read_yaml(path)
                    # Extract kind name
                    kind = crd["spec"]["names"]["kind"]
                    self.crds[kind] = crd
            notice(f"Loaded {len(self.crds)} CRD files")
        
        # Continue with existing code...
        self.init(exclude=["properties.yaml", "overview.md"])
```

**That's it for Phase 1**. Just load the CRD files into memory.

---

### Phase 2: Use CRD Data (1-2 hours)

**File**: `python/resources.py`

**Find the Resource class** and modify `__init__` to use CRD data:

**Current logic** (simplified):
```python
class Resource:
    def __init__(self, model, data):
        self.description = data.get("description")
        self.spec_properties = load_from_yaml()
```

**New logic**:
```python
class Resource:
    def __init__(self, model, data):
        # Try to get CRD data for this resource
        crd = self._get_crd_data()
        
        # Use CRD description if available, else YAML
        if crd:
            schema = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
            self.description = schema.get("description", "")
        else:
            self.description = data.get("description")
        
        # Use CRD spec properties if available, else YAML
        if crd:
            self.spec_properties = self._load_from_crd(crd, "spec")
            self.status_properties = self._load_from_crd(crd, "status")
        else:
            # Fall back to YAML
            self.spec_properties = load_from_yaml_spec()
            self.status_properties = load_from_yaml_status()
```

**Add helper method**:
```python
def _get_crd_data(self):
    """Get CRD data for this resource."""
    if not hasattr(self.model, 'crds'):
        return None
    
    # Look up by resource name (e.g., "Site")
    return self.model.crds.get(self.name)

def _load_from_crd(self, crd, section):
    """Extract properties from CRD schema."""
    schema = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
    
    if section not in schema.get("properties", {}):
        return []
    
    section_schema = schema["properties"][section]
    if "properties" not in section_schema:
        return []
    
    properties = []
    for prop_name, prop_schema in section_schema["properties"].items():
        # Create Property object from CRD schema
        prop_data = {
            "name": prop_name,
            "type": prop_schema.get("type", "string"),
            "description": prop_schema.get("description", ""),
            "required": prop_name in section_schema.get("required", []),
            "default": prop_schema.get("default"),
            "enum": prop_schema.get("enum"),
        }
        
        prop = Property(self.model, self, prop_data)
        properties.append(prop)
    
    return properties
```

**That's it for Phase 2**. Now resources use CRD when available.

---

### Phase 3: Test with ONE Resource (30 minutes)

```bash
# Generate just one resource
./plano generate

# Check the output for "site"
cat input/resources/site.md

# Compare with old version
git diff input/resources/site.md
```

**Questions to answer**:
1. Does it generate without errors?
2. Is the description from CRD?
3. Are properties from CRD?
4. Does it look reasonable?

**If yes**: Continue to Phase 4  
**If no**: Fix issues, repeat

---

### Phase 4: Expand to All Resources (30 minutes)

Remove any hard-coded checks. Make it work for all resources:

```python
# No special cases needed!
# Just use CRD if available, else YAML fallback
```

Test all resources:

```bash
./plano generate
ls input/resources/*.md
git diff --stat input/resources/
```

---

## Even Simpler: One Resource POC First

Like we did with `site create` for commands, hard-code for just `Site` resource:

```python
class Resource:
    def __init__(self, model, data):
        # HACK: Special case for Site
        if self.name == "Site":
            crd = model.crds.get("Site")
            if crd:
                schema = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
                self.description = schema.get("description", "")
                self.spec_properties = self._load_from_crd(crd, "spec")
                self.status_properties = self._load_from_crd(crd, "status")
        else:
            # Normal YAML-based logic for all other resources
            self.description = data.get("description")
            self.spec_properties = load_from_yaml()
```

Test just that one resource. If it works, remove the `if` and make it apply to all.

---

## What We're NOT Doing (Keep It Simple)

❌ **Skip validation** - No enum checking initially  
❌ **Skip metadata merge** - Don't implement Phase 2 metadata yet  
❌ **Skip complex merging** - Just use CRD directly  
❌ **Skip property grouping** - Use CRD as-is first  
❌ **Skip nested objects** - Simple properties only initially  

Get it working first, enhance later.

---

## Key Differences from Commands

### Easier:
- ✅ Fewer files (9 CRDs vs 38 cli-docs)
- ✅ Simpler parsing (YAML vs markdown)
- ✅ Already have yaml library

### Slightly harder:
- ⚠️ Nested schema (spec.properties.linkAccess)
- ⚠️ Property objects more complex
- ⚠️ Need to handle metadata properties too

**But the pattern is identical!**

---

## CRD Structure Quick Reference

```yaml
# crds/skupper_site_crd.yaml
spec:
  names:
    kind: Site  # ← Resource name
  versions:
    - name: v2alpha1
      schema:
        openAPIV3Schema:
          description: "..."  # ← Resource description
          properties:
            spec:  # ← Spec properties
              properties:
                linkAccess:  # ← Property name
                  type: string  # ← Property type
                  description: "..."  # ← Property description
                  enum: [none, default, route, loadbalancer]  # ← Choices
            status:  # ← Status properties
              properties:
                ...
```

**Access path**: `crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]`

---

## Code Structure Comparison

### Commands (Already Done)

```python
# Load source files
self.cli_docs = parse_all_cli_docs("cli-doc")

# Get data for specific command
cli_doc = self.model.cli_docs.get("site create")

# Use it
if cli_doc:
    self.description = cli_doc["synopsis"]
    self.options = cli_doc["options"]
```

### Resources (To Do)

```python
# Load source files
self.crds = load_all_crds("crds")

# Get data for specific resource
crd = self.model.crds.get("Site")

# Use it
if crd:
    schema = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
    self.description = schema["description"]
    self.spec_properties = extract_properties(schema["properties"]["spec"])
```

**Same pattern!**

---

## Estimated Time

| Phase | Time | Total |
|-------|------|-------|
| Phase 1: Load CRDs | 30 min | 0.5h |
| Phase 2: Use CRD data | 1-2 hours | 2.5h |
| Phase 3: Test one resource | 30 min | 3h |
| Phase 4: Expand to all | 30 min | 3.5h |

**Total: ~3.5 hours to working system**

Compare to original estimate: 16-24 hours  
**Savings: 12-20 hours** by following the simple approach!

---

## Success Criteria

After implementation:

1. ✅ `./plano generate` completes without errors
2. ✅ `input/resources/site.md` has description from CRD
3. ✅ Properties show correct types from CRD
4. ✅ All 9 resources generate
5. ✅ Docs are smaller and more accurate

---

## The Full Implementation (Copy-Paste Ready)

### Step 1: Import os module

At top of `python/resources.py`:
```python
from common import *
import os  # ADD THIS
```

### Step 2: Add CRD loading to ResourceModel

Replace `ResourceModel.__init__`:

```python
class ResourceModel(Model):
    def __init__(self):
        super().__init__(Resource, "config/resources")
        
        self.property_data = read_yaml(join(self.config_dir, "properties.yaml"))
        
        # NEW: Load CRD files
        self.crds = {}
        crd_dir = "crds"
        if os.path.exists(crd_dir):
            notice("Loading CRD files...")
            for crd_file in list_dir(crd_dir):
                if crd_file.endswith("_crd.yaml"):
                    path = join(crd_dir, crd_file)
                    crd_data = read_yaml(path)
                    kind = crd_data["spec"]["names"]["kind"]
                    self.crds[kind] = crd_data
            notice(f"Loaded {len(self.crds)} CRD files")
        
        self.init(exclude=["properties.yaml", "overview.md"])
```

### Step 3: Add CRD helpers to Resource class

Add these methods to the `Resource` class:

```python
def _get_crd_data(self):
    """Get CRD for this resource."""
    if not hasattr(self.model, 'crds'):
        return None
    return self.model.crds.get(self.name)

def _extract_crd_properties(self, crd, section):
    """Extract properties from CRD schema section (spec or status)."""
    schema = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
    
    if section not in schema.get("properties", {}):
        return []
    
    section_props = schema["properties"][section].get("properties", {})
    required_list = schema["properties"][section].get("required", [])
    
    properties = []
    for prop_name, prop_schema in section_props.items():
        prop_data = {
            "name": prop_name,
            "type": prop_schema.get("type", "string"),
            "description": prop_schema.get("description", ""),
            "required": prop_name in required_list,
            "default": prop_schema.get("default"),
        }
        
        # Handle enums
        if "enum" in prop_schema:
            prop_data["choices"] = [{"name": v, "description": ""} for v in prop_schema["enum"]]
        
        prop = Property(self.model, self, prop_data)
        properties.append(prop)
    
    return properties
```

### Step 4: Modify Resource.__init__ to use CRD

Find the `Resource.__init__` method and modify it to check for CRD first:

```python
def __init__(self, model, data):
    super().__init__(model, data)
    
    # NEW: Try to get CRD data
    crd = self._get_crd_data()
    
    # Use CRD description if available
    if crd:
        schema = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
        self.data["description"] = schema.get("description", "")
    
    # Load examples, links, etc. from YAML (existing code)
    self.examples = self.data.get("examples", [])
    # ... other YAML fields ...
    
    # NEW: Load properties from CRD if available, else YAML
    if crd:
        self.spec_properties = self._extract_crd_properties(crd, "spec")
        self.status_properties = self._extract_crd_properties(crd, "status")
    else:
        # Fallback to existing YAML loading
        self.spec_properties = [Property(...) for ... in spec data]
        self.status_properties = [Property(...) for ... in status data]
```

---

## Test Plan

```bash
# 1. Implement the changes above

# 2. Run generation
./plano generate

# 3. Check for CRD loading
# Should see: "Loading CRD files..." and "Loaded 9 CRD files"

# 4. Check one resource
cat input/resources/site.md | head -50

# 5. Compare with old
git diff input/resources/site.md

# 6. If good, check all
git diff --stat input/resources/
```

---

## Rollback Plan

If something breaks:

```bash
# Revert the changes
git checkout python/resources.py

# Regenerate with old code
./plano generate
```

All changes are in one file, easy to revert!

---

## Next Steps After Implementation

Once this works:

1. **Phase 2**: Add metadata merge (examples, enhanced descriptions)
2. **Phase 3**: Remove old YAML files
3. **Phase 4**: Add validation

But get Phase 1 working first!

---

## Bottom Line

**Same approach as commands**:
1. Load CRDs (like we loaded cli-doc)
2. Use CRD data when available (like we used cli-doc)  
3. Fall back to YAML if missing (like we did for commands)
4. Test with one resource first (like we did with `site create`)

**Estimated time**: 3.5 hours  
**Risk**: Low (same pattern as commands, which worked)  
**Benefit**: Auto-sync with CRD changes

**Ready to implement?**
