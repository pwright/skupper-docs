# CRD Update Workflow

**Purpose**: Instructions for updating resource documentation when Skupper CRDs are updated.

**Status**: ⏳ **Not Yet Implemented** - This describes the planned workflow

---

## Overview

When Skupper releases a new version, the CRD definitions may change. This guide explains how to update the refdog resource documentation to reflect those changes.

**Key Principle**: The CRD files (`crds/*.yaml`) are the **source of truth** for resource documentation. When they update, regenerate the docs automatically.

---

## When to Update

Update refdog resource documentation whenever:
- ✅ New Skupper version is released
- ✅ CRD schemas change (new properties, changed descriptions, etc.)
- ✅ New resources are added
- ✅ Resources are deprecated/removed

---

## Step-by-Step Process (Planned)

### 1. Update CRD Files

**You already do this!** The CRD files are updated from the Skupper repository.

```bash
# This is what you do each release (already done):
# - Copy updated crds/*.yaml files from skupper repo
# - Or pull from upstream skupper repository
```

**Verify the update**:
```bash
# Check how many files you have
ls crds/*.yaml | wc -l

# Should be 9-12 files (as of 2026-04-27)

# Check a sample to see if it looks current
head -50 crds/skupper_site_crd.yaml
```

---

### 2. Regenerate Documentation

Run the generation script to rebuild all resource docs from the updated CRDs:

```bash
./plano generate
```

**What will happen** (once implemented):
1. Loads all CRD files from `crds/`
2. Parses OpenAPI v3 schema from each CRD
3. Merges with metadata (examples, cross-references)
4. Generates markdown files in `input/resources/`

**Expected output** (once implemented):
```
plano: notice: Loading CRD files...
plano: notice: Loaded 9 CRD files
--> generate
plano: notice: Generating resources
plano: notice: Generating input/resources/site.md
plano: notice: Generating input/resources/connector.md
...
<-- generate
OK (0s)
```

---

### 3. Review Changes

Check what changed in the generated documentation:

```bash
# See which files changed
git status --short input/resources/

# See summary of changes
git diff --stat input/resources/

# Review specific changes (pick a few key resources)
git diff input/resources/site.md
git diff input/resources/connector.md
git diff input/resources/listener.md
```

**What to look for**:

✅ **New properties** - CRD added new spec/status fields  
✅ **Removed properties** - CRD removed fields  
✅ **Changed descriptions** - Property descriptions updated  
✅ **Changed types** - Property types changed  
✅ **Changed enums** - Allowed values changed  

❌ **Watch out for**:
- Massive deletions (might indicate parsing error)
- All files unchanged (might mean CRDs weren't updated)
- Generation errors (check `plano generate` output)

---

### 4. Handle New/Removed Resources

#### If a NEW resource was added:

```bash
# 1. Generate will create the basic file automatically
./plano generate

# 2. Optionally create metadata for richer examples
# (Create config/resources/metadata/<resource-name>.yaml)

# Example: config/resources/metadata/certificate.yaml
cat > config/resources/metadata/certificate.yaml <<EOF
name: Certificate
examples:
  - description: A minimal certificate
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: Certificate
      metadata:
        name: my-cert
        namespace: default

related_resources: [site]
links: [skupper/certificates]

properties:
  issuer:
    group: frequently-used
    updatable: true
EOF

# 3. Regenerate to include the metadata
./plano generate
```

#### If a resource was REMOVED:

```bash
# 1. The generated file will be outdated (CRD missing)
# 2. Manually delete the file
rm input/resources/removed-resource.md

# 3. Delete the metadata file if it exists
rm config/resources/metadata/removed-resource.yaml

# 4. Update groups.yaml if needed
vim config/resources/groups.yaml
```

---

### 5. Commit Changes

Commit both the updated CRD files AND the regenerated documentation:

```bash
# Add the updated CRD files
git add crds/

# Add the regenerated documentation
git add input/resources/

# Add any new metadata files you created
git add config/resources/metadata/

# Commit with descriptive message
git commit -m "Update resource documentation for Skupper vX.Y.Z

- Updated CRD files from skupper vX.Y.Z
- Regenerated resource documentation
- Added metadata for new resources: <list>
- Removed deprecated resources: <list>
"
```

---

## Common Scenarios

### Scenario 1: New CRD Property Added

**Example**: Skupper adds `observer` property to Listener spec

**What happens automatically** (once implemented):
1. Updated `crds/skupper_listener_crd.yaml` has the new property
2. Run `./plano generate`
3. `input/resources/listener.md` now documents `observer`
4. No manual editing needed!

**Verify**:
```bash
./plano generate
git diff input/resources/listener.md | grep -A5 "observer"
```

---

### Scenario 2: CRD Property Removed

**Example**: Skupper removes deprecated property

**What happens automatically** (once implemented):
1. Updated CRD no longer has the property
2. Run `./plano generate`
3. Resource doc no longer shows the property
4. Users can't accidentally use removed property!

---

### Scenario 3: Property Description Changed

**Example**: Skupper team improves description for `linkAccess`

**What happens automatically** (once implemented):
1. Updated CRD has new description in OpenAPI schema
2. Run `./plano generate`
3. `input/resources/site.md` gets new description
4. Documentation stays current!

---

### Scenario 4: Want Better Examples

**What to do**: Add/update metadata file

The CRD files have **technical schema** (types, required fields, validation).  
For **rich examples and enhanced descriptions**, add them to metadata:

```bash
# Edit the metadata file
vim config/resources/metadata/site.yaml

# Add or improve examples:
examples:
  - description: A minimal site
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: Site
      metadata:
        name: east
        namespace: hello-world-east
  
  - description: A site configured to accept links
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: Site
      metadata:
        name: west
        namespace: hello-world-west
      spec:
        linkAccess: default

# Add property enhancements:
properties:
  linkAccess:
    group: frequently-used
    updatable: true
    choices:
      - name: none
        description: No linking to this site is permitted.
      - name: default
        description: Use the default link access for the current platform.

# Regenerate
./plano generate
```

The generated docs will have:
- **Technical schema** from CRD (types, required, validation)
- **Rich examples** from metadata
- **Enhanced descriptions** from metadata

---

## Current vs Future State

### Current State (Before Implementation)

```
config/resources/*.yaml (All-in-one YAML)
    ↓
python/resources.py (Generation)
    ↓
input/resources/*.md (Generated docs)
```

**Problems**:
- ❌ Duplicate effort (schema in CRD, schema in YAML)
- ❌ Can get out of sync
- ❌ Manual updates required

---

### Future State (After Implementation)

```
crds/*.yaml (Schema - source of truth)
    +
config/resources/metadata/*.yaml (Documentation enhancements)
    ↓
python/resources.py (Merge + generate)
    ↓
input/resources/*.md (Generated docs)
```

**Benefits**:
- ✅ Single source of truth (CRDs)
- ✅ Auto-sync with schema changes
- ✅ Smaller metadata files
- ✅ Less maintenance

---

## Data Sources

### From CRDs (Authoritative)

**File**: `crds/skupper_site_crd.yaml`

```yaml
spec:
  versions:
    - name: v2alpha1
      schema:
        openAPIV3Schema:
          description: "A site is a place on the network..."
          properties:
            spec:
              properties:
                linkAccess:
                  type: string
                  description: "Configure external access..."
                  enum: [none, default, route, loadbalancer]
                  default: none
```

**Provides**:
- Resource name, description
- Property names, types, formats
- Required fields
- Default values
- Enum values
- Validation rules

---

### From Metadata (Enhancements)

**File**: `config/resources/metadata/site.yaml`

```yaml
name: Site
examples:
  - description: A minimal site
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: Site
      ...

related_resources: [link]
links: [skupper/site-configuration]

properties:
  linkAccess:
    group: frequently-used
    updatable: true
    choices:
      - name: none
        description: No linking to this site is permitted.
      - name: default
        description: Use the default link access...
```

**Provides**:
- Examples (YAML snippets)
- Cross-references (related resources, concepts)
- Property grouping (frequently-used, advanced)
- Choice descriptions (enum value explanations)
- Updatable flags
- Platform notes

---

## What Gets Updated Automatically

When you run `./plano generate` after updating CRDs:

✅ Resource descriptions (from CRD schema)  
✅ Property names (from CRD schema)  
✅ Property types (from CRD schema)  
✅ Property descriptions (from CRD schema)  
✅ Required fields (from CRD schema)  
✅ Default values (from CRD schema)  
✅ Enum values (from CRD schema)  
✅ Validation rules (from CRD schema)  

❌ **Not updated automatically** (preserved from metadata):  
- Examples (kept from metadata)  
- Cross-references (kept from metadata)  
- Property grouping (kept from metadata)  
- Choice descriptions (kept from metadata)  
- Updatable flags (kept from metadata)

---

## Files You Touch

**Every release**:
- `crds/*.yaml` - Update from skupper repo (you already do this)

**Run every release**:
- `./plano generate` - Regenerates all docs

**Sometimes** (only if adding metadata):
- `config/resources/metadata/*.yaml` - Examples, enhanced descriptions

**Never touch**:
- `input/resources/*.md` - These are GENERATED, don't edit by hand!
- `python/resources.py` - Generation code (will be updated in implementation)
- `config/resources/*.yaml` - Old all-in-one files (will be phased out)

---

## Validation

The system will validate (once implemented):

1. **Enum mismatches**: Warn if metadata describes enum values not in CRD
2. **Missing properties**: Info if CRD has properties not documented in metadata
3. **Type conflicts**: Error if metadata contradicts CRD schema

**Example validation output**:
```
plano: warning: Site.linkAccess: Metadata describes choice 'custom' not in CRD enum
plano: info: Connector.useClientCert: Property in CRD but not documented in metadata
```

---

## Troubleshooting

### Problem: Property descriptions are too technical

**Cause**: CRD descriptions are written for API consumers, may be terse

**Solution**: Add enhanced descriptions in metadata:

```yaml
# config/resources/metadata/site.yaml
properties:
  linkAccess:
    description: |
      Configure external access for links from remote sites.
      
      Sites and links are the basis for creating application networks.
      In a simple two-site network, at least one of the sites must have
      link access enabled.
```

The metadata description will be used instead of (or in addition to) the CRD description.

---

### Problem: Enum values have no descriptions

**Cause**: CRD only has enum values, not descriptions

**Solution**: Add choice descriptions in metadata:

```yaml
# config/resources/metadata/site.yaml
properties:
  linkAccess:
    choices:
      - name: none
        description: No linking to this site is permitted.
      - name: default
        description: Use the default link access for the current platform.
      - name: route
        description: Use an OpenShift route. _OpenShift only._
      - name: loadbalancer
        description: Use a Kubernetes load balancer.
```

---

### Problem: Examples needed

**Cause**: CRDs don't include usage examples

**Solution**: Add examples in metadata:

```yaml
# config/resources/metadata/connector.yaml
examples:
  - description: Basic connector to backend service
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: Connector
      metadata:
        name: backend
      spec:
        routingKey: backend
        host: backend.default.svc.cluster.local
        port: 8080
```

---

## Quick Reference (Once Implemented)

**Every release**:

```bash
# 1. Update CRD files (you do this from skupper repo)
cp /path/to/skupper/api/crds/*.yaml crds/

# 2. Regenerate documentation
./plano generate

# 3. Review changes
git diff --stat input/resources/
git diff input/resources/site.md  # spot check

# 4. Commit
git add crds/ input/resources/
git commit -m "Update resource docs for Skupper vX.Y.Z"
```

**That's it!** The whole process should take < 5 minutes.

---

## Summary

**The new workflow will be simpler**:

### Old way (current):
1. Update CRD files
2. Manually edit config/resources/*.yaml to match
3. Hunt for inconsistencies
4. Run ./plano generate
5. Fix errors
6. Repeat until docs match CRDs

### New way (once implemented):
1. Update CRD files
2. Run `./plano generate`
3. Done! ✅

**The docs will automatically stay in sync with the CRDs.**

---

## Implementation Status

**Status**: ⏳ **Design complete, implementation pending**

- ✅ Design documented (crd-generation-proposal.md)
- ✅ Merge logic specified (generation-merge-logic.md)
- ✅ Metadata files prepared (config/resources/metadata/*.yaml)
- ✅ Validation strategy defined
- ⏳ Code implementation needed (python/resources.py changes)
- ⏳ Testing needed

**Estimated effort**: 16-24 hours to implement

**See**: `crd-generation-proposal.md` and `generation-merge-logic.md` for technical details

---

## Next Steps

1. **Implement** the CRD + metadata merge logic (see implementation plan)
2. **Test** with one resource (Site)
3. **Validate** output matches current docs or improves them
4. **Migrate** all resources
5. **Use this workflow** for future updates

---

**Note**: This workflow doc describes the PLANNED system. The implementation still needs to be completed. See the simplified implementation plan for next steps.
