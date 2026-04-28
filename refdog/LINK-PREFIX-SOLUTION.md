# Link Prefix Solution: Configurable Output for Multiple Platforms

## Current Situation

Refdog generates links with `{{site.prefix}}` template syntax:
- **Works for**: Transom/Jekyll (template engine substitutes the variable)
- **Breaks**: MkDocs (no template substitution, literal `{{site.prefix}}` appears)

## Root Cause

**3 locations in Python code**:

1. `python/common.py:254` - `ModelObject.href`:
   ```python
   @property
   def href(self):
       type = self.__class__.__name__.lower()
       return f"{{{{site.prefix}}}}/{plural(type)}/{self.id}.html"
   ```

2. `python/commands.py:473` - `Command.href` override:
   ```python
   @property
   def href(self):
       if self.subcommands:
           return f"{{{{site.prefix}}}}/commands/{self.id}/index.html"
       return super().href
   ```

3. `python/common.py:120` - `generate_attribute_links()`:
   ```python
   if url.startswith("/"):
       url = "{{site.prefix}}" + url
   ```

## Solutions

### Option 1: Environment Variable (Simplest)

Add at top of `python/common.py`:

```python
import os

# Configure link prefix based on output format
SITE_PREFIX = os.getenv('REFDOG_SITE_PREFIX', '{{site.prefix}}')
```

Then replace hardcoded `{{site.prefix}}` with the variable:

**`common.py:120`**:
```python
if url.startswith("/"):
    url = SITE_PREFIX + url
```

**`common.py:254`**:
```python
@property
def href(self):
    type = self.__class__.__name__.lower()
    return f"{SITE_PREFIX}/{plural(type)}/{self.id}.html"
```

**`commands.py:473`** (add import first):
```python
from common import SITE_PREFIX

@property
def href(self):
    if self.subcommands:
        return f"{SITE_PREFIX}/commands/{self.id}/index.html"
    return super().href
```

**Usage**:
```bash
# For Transom/Jekyll (default)
./plano generate

# For MkDocs (empty prefix = relative paths)
REFDOG_SITE_PREFIX="" ./plano generate

# For specific deployment path
REFDOG_SITE_PREFIX="/reference" ./plano generate
```

**Pros**:
- ✅ Minimal code changes (3 files, ~5 lines)
- ✅ No config files needed
- ✅ Backward compatible (default keeps {{site.prefix}})
- ✅ Works for any deployment path

**Cons**:
- ⚠️ Must remember to set env var for MkDocs

---

### Option 2: Config File

Create `refdog/config/output.yaml`:

```yaml
# Output format configuration
format: transom  # or "mkdocs"

# Link prefix for different formats
prefixes:
  transom: "{{site.prefix}}"
  mkdocs: ""
  github_pages: "/refdog"
```

**`common.py`**:
```python
_output_config = read_yaml("config/output.yaml")
SITE_PREFIX = _output_config["prefixes"][_output_config["format"]]
```

**Usage**: Edit `config/output.yaml` before generating

**Pros**:
- ✅ Explicit configuration
- ✅ Can commit different configs
- ✅ Easy to see current setting

**Cons**:
- ⚠️ Must edit file before each build
- ⚠️ Can accidentally commit wrong config

---

### Option 3: Plano Command Argument

Modify `.plano.py` to accept format argument:

```python
@command
def generate(format="transom"):
    """Generate documentation
    
    Arguments:
    - format: Output format (transom, mkdocs, github_pages)
    """
    os.environ['REFDOG_SITE_PREFIX'] = {
        'transom': '{{site.prefix}}',
        'mkdocs': '',
        'github_pages': '/refdog'
    }[format]
    
    # ... existing generate code ...
```

**Usage**:
```bash
./plano generate transom  # Default
./plano generate mkdocs   # For MkDocs
```

**Pros**:
- ✅ Clean CLI interface
- ✅ Self-documenting
- ✅ Can't forget which mode

**Cons**:
- ⚠️ Requires modifying .plano.py

---

### Option 4: Use Relative Paths Always

**Insight**: Relative paths work in BOTH Transom and MkDocs!

Instead of `{{site.prefix}}/commands/site/create.html`, calculate relative path from current page.

**Problem**: Requires knowing current page context during link generation. Complex.

**Verdict**: Skip this - too complex for small benefit.

---

## Recommended: Option 1 (Environment Variable)

**Why**:
- Simplest implementation
- No config files
- Backward compatible
- Flexible for any deployment

### Implementation

#### 1. Update `python/common.py`

Add at top (after imports):
```python
import os

# Link prefix - configurable via environment variable
# Default: {{site.prefix}} for Transom/Jekyll
# Set to "" for MkDocs relative paths
# Set to "/path" for specific base path
SITE_PREFIX = os.getenv('REFDOG_SITE_PREFIX', '{{site.prefix}}')
```

Change line 120:
```python
# OLD
if url.startswith("/"):
    url = "{{site.prefix}}" + url

# NEW
if url.startswith("/"):
    url = SITE_PREFIX + url
```

Change line 254:
```python
# OLD
@property
def href(self):
    type = self.__class__.__name__.lower()
    return f"{{{{site.prefix}}}}/{plural(type)}/{self.id}.html"

# NEW
@property
def href(self):
    type = self.__class__.__name__.lower()
    return f"{SITE_PREFIX}/{plural(type)}/{self.id}.html"
```

#### 2. Update `python/commands.py`

Add import at top:
```python
from common import SITE_PREFIX
```

Change line 473:
```python
# OLD
@property
def href(self):
    if self.subcommands:
        return f"{{{{site.prefix}}}}/commands/{self.id}/index.html"
    return super().href

# NEW
@property
def href(self):
    if self.subcommands:
        return f"{SITE_PREFIX}/commands/{self.id}/index.html"
    return super().href
```

#### 3. Update Build Scripts

**For Transom** (standalone refdog site):
```bash
# .plano.py or manual
./plano generate
# Uses default {{site.prefix}}
```

**For MkDocs**:
```bash
# docs-vale/regenerate-for-mkdocs.sh
#!/bin/bash
cd refdog
REFDOG_SITE_PREFIX="" ./plano generate
```

**For GitHub Pages at /refdog/**:
```bash
REFDOG_SITE_PREFIX="/refdog" ./plano generate
```

---

## Migration Path

### Phase 1: Make it Configurable
1. Add `SITE_PREFIX` variable to `common.py`
2. Update 3 locations to use variable
3. Test both modes work

### Phase 2: Update Build Workflow
1. Update `fix-refdog-for-mkdocs.sh` → `regenerate-for-mkdocs.sh`:
   ```bash
   #!/bin/bash
   cd refdog
   REFDOG_SITE_PREFIX="" ./plano generate
   ```
2. No more sed post-processing needed!

### Phase 3: Documentation
1. Update README.md with new workflow
2. Document env var in refdog docs

---

## Link Structure Examples

### Transom (default)
```
REFDOG_SITE_PREFIX="{{site.prefix}}"
→ {{site.prefix}}/commands/site/create.html
→ {{site.prefix}}/resources/site.html
```

### MkDocs (relative)
```
REFDOG_SITE_PREFIX=""
→ /commands/site/create.html
→ /resources/site.html
```

With `use_directory_urls: false`, MkDocs renders these as absolute paths from docs root.

### GitHub Pages
```
REFDOG_SITE_PREFIX="/refdog"
→ /refdog/commands/site/create.html
→ /refdog/resources/site.html
```

---

## Testing

```bash
# Test Transom mode
./plano generate
grep -r "{{site.prefix}}" input/  # Should find matches

# Test MkDocs mode
REFDOG_SITE_PREFIX="" ./plano generate  
grep -r "{{site.prefix}}" input/  # Should find NO matches

# Test custom path
REFDOG_SITE_PREFIX="/reference" ./plano generate
grep -r "/reference/commands" input/  # Should find matches
```

---

## Benefits

✅ **Clean**: No sed post-processing  
✅ **Flexible**: Works for any deployment  
✅ **Simple**: One env var  
✅ **Backward Compatible**: Default unchanged  
✅ **Maintainable**: Change in 3 places, affects all 500+ generated links

Want me to implement this?
