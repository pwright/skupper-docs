# Simplifying Refdog for DITA conversion

Refdog can take a simpler route to DITA than the authored documentation tree: retain the command and resource structure **before it becomes presentation HTML**. Extend the existing generation models to produce a reviewable intermediate model, then generate Markdown and, later, DITA from that model. Parsing the generated Markdown remains useful for verification, but should not be the main way to recover information the generators already possess.

This is an outline of proposed changes for **`input/refdog/`**. No generator, upstream source, generated page, or DITA writer was changed. The recommendations complement [the authored-input report](report.md), but do not assume that generated files should be edited by hand.

## Current structure and evidence

The tree contains 88 Markdown files:

| Area | Files, including indexes | Likely conversion role |
| --- | ---: | --- |
| `commands/` | 44 | Command references and command-group navigation |
| `resources/` | 11 | Resource references and resource navigation |
| `concepts/` | 13 | Concepts and concept navigation |
| `topics/` | 19 | Individually reviewed authored/supporting topics |
| Root | 1 | Collection navigation |

A read-only run of both analyzers found the same file set after removing IWE's `refdog/` path prefix. Both counted 262 Markdown headings, 176 list items, 82 code blocks, and 3 Markdown tables. These totals omit the semantic structure embedded in HTML: the AST contains 799 HTML blocks, and the current classifier emits 695 `RAW_HTML` warnings. HTML `<h3>` property/option titles are not Markdown headings, and HTML tables are not mdast table nodes.

The heuristic topic guesses—1 task, 48 references, and 39 concepts—are not reviewed types. Refdog knows more about its generated objects than those guesses express. The repeated HTML output is the main obstacle, rather than inconsistent editing across hundreds of independent pages.

### What actually feeds the output

The active `refdog/./plano generate` path uses [refdog/python/generate.py](../refdog/python/generate.py) and its command, resource, and concept models. There is also a separate root `python/` directory with similarly named generators; changes should target the active entry point rather than assuming those copies are interchangeable.

| Content | Inspected generation behavior | Consequence |
| --- | --- | --- |
| Commands | [commands.py](../refdog/python/commands.py) loads configured command trees and can use parsed CLI Markdown for descriptions and options, with YAML fallback. | CLI facts and editorial additions need an explicit merge contract. |
| Resources | [resources.py](../refdog/python/resources.py) builds objects from resource YAML; CRDs supply checks and selected property fallbacks, including type/format/description and required membership. | This is not yet a pipeline that derives all resource facts directly from CRDs. |
| Concepts | [concepts.py](../refdog/python/concepts.py) renders configured descriptions and relationships. | Authored prose and figures need preservation, not schema extraction. |
| Supporting topics | The inspected orchestration does not generate `topics/`. Several pages are very short. | Establish ownership and completeness per page before conversion; do not treat these as disposable generator output. |

The resource `metadata/` directory already contains extracted editorial information, but the active resource constructor still reads the older resource configuration. Command metadata is loaded into a local variable in the inspected constructor, without a corresponding merge there. Existing metadata files therefore do not establish that the proposed metadata-driven pipeline is complete.

Two checkout-specific facts matter when validating a migration:

- **`refdog/input` is a symlink to `../input/refdog`.** Generation writes into the published input tree directly here. The older README's separate mirror/copy description does not match this checkout. A pilot should write to a separate output directory, not run regeneration expecting an isolated staging tree.
- **`refdog/cli-doc/` currently contains no Markdown files.** The present output cannot be proven reproducible from local CLI Markdown alone. Capture a pinned upstream CLI documentation snapshot before using regeneration as a correctness check. Missing upstream input should be reported explicitly rather than silently treated as authoritative YAML fallback.

## 1. Keep one reviewed model before rendering

Build on the existing `Command`, `Option`, `Resource`, `Property`, and `Concept` objects. Add a small, versioned export rather than a second set of Markdown-to-reference heuristics.

A proposed flow is:

```text
Pinned CLI source/export ──┐
                          ├─ normalized objects + editorial metadata
Pinned CRD schemas ───────┤          │
                          │          ├─ review JSON and validation findings
Authored concepts/examples┘          ├─ Markdown for the current website
                                     └─ DITA and maps, after model review
```

Keep long descriptions as supported Markdown fragments initially. Preserve their source location and parse their block structure with remark when reviewing or rendering them. Do not flatten rich descriptions into a single table-cell string.

Each exported object should have a stable ID, object kind, title, description, version context, relationships, and source provenance. Options and fields should retain their own identities and origins. Record both the source path and a structured locator, such as a command path or CRD schema pointer; generated Markdown line numbers are useful diagnostics but unstable source identities.

This model makes confidence simpler: a declared command is a reference candidate by construction, while uncertain extraction or conflicting facts produce specific warnings. Do not attach high confidence merely because an upstream parser returned a value.

## 2. Give CLI facts and documentation metadata distinct ownership

Prefer a structured export from the upstream CLI generator if it can be added. If Markdown remains the available interface, isolate [cli_parser.py](../refdog/python/cli_parser.py) as an extraction step with fixtures covering the upstream format. That parser currently depends on exact headings and code-fence conventions; its success should be validated before its output replaces YAML data.

| Fact | Proposed authority |
| --- | --- |
| Command path, arguments, flags, types, defaults, inherited flags, usage | Pinned CLI export or validated CLI Markdown extraction |
| Examples, platform notes, related concepts/resources, error explanations, display grouping | Editorial metadata keyed by command/option identity |
| A conflicting override | Explicit exception with reason and provenance, rather than an accidental merge result |

Preserve positional arguments separately from flags, and locally declared options separately from inherited/global options. Keep absent defaults distinct from empty strings, zero, and `false`. Do not rebuild usage from a lossy option list if authoritative usage is available: the parser extracts usage, but the current Markdown writer constructs usage through `generate_usage`.

The rendered [site-create page](../input/refdog/commands/site/create.md) provides a useful pilot: its `--help` description contains fence markers and namespace/platform option text. That is an extraction/output defect to trace back through the pipeline. Editing the generated paragraph would hide the symptom until the next generation run.

Structured examples already appear in [site-create metadata](../refdog/config/commands/metadata/site-create.yaml): description, command, and output are separate fields. Use that form consistently. A reference example is not a task solely because it contains a command; keep a terminal transcript explicit when it is intentionally shown as one.

## 3. Derive resource facts from the selected CRD schema

Use CRDs for the API facts they actually declare, with editorial metadata for examples, grouping, related information, and explanations not present in the schema. This follows the direction of [the existing CRD-generation proposal](../refdog/crd-generation-proposal.md), but should be implemented and validated incrementally.

The inspected lookup uses `spec.versions[0]`. Replace that implicit choice with an explicit documented version selection. Include API group, version, kind, and the full property path in field identity. Traverse nested objects and array items rather than documenting only top-level `spec` and `status` names.

Preserve these distinctions in the model:

- Schema-required membership versus editorial “frequently used” grouping.
- A declared default versus no schema default; in particular, do not invent `false` merely because a field is boolean.
- Enum values and constraints versus editorial explanations of those values.
- `spec`, `status`, and metadata fields with the same short name.
- Validation expressions and Kubernetes schema extensions versus plain prose descriptions.

The current property implementation defaults booleans to `false` when no configured default exists, and its enum lookup is not used by the returned `choices` value. These are reasons to validate field semantics before producing DITA, rather than assume that converting the rendered “Default” and “Choices” tables preserves the CRD contract.

Key editorial additions by full field path, such as `spec.linkAccess`, rather than a short name alone. Reject or report metadata pointing at missing schema fields, and require an explicit reason for omitting schema fields from documentation. The existing [validation scripts](../refdog/scripts/validate_metadata_vs_crds.py) are starting points, not proof of coverage: this script inspects a different metadata shape from the flat `properties` mapping in the extracted Site metadata.

## 4. Generate semantic Markdown instead of structural HTML

Update shared writers, not individual generated pages.

| Current generated structure | Simpler representation |
| --- | --- |
| `<div class="attribute">` containing an HTML `<h3>` | A Markdown H3 per option or property, under its owning H2 section |
| Small HTML fields tables | Explicit model fields rendered as a Markdown list or simple table |
| Nested HTML enum-choice tables | A choice list or table with descriptions retained as blocks when needed |
| Index HTML tables | Markdown lists/tables backed by an explicit navigation model |
| Raw HTML figures in concept descriptions | Structured figure/image/caption data or a documented Markdown representation |
| Collapsed/advanced CSS classes | Editorial grouping metadata; presentation applies collapse behavior at rendering time |

Keep current deep-link identities, such as `spec-link-access` and `option-enable-link-access`, even if headings change. A generated compatibility anchor may remain in Markdown. Removing every HTML node is less valuable than making semantic boundaries visible without losing URLs, captions, or rich descriptions.

For [the Site resource](../input/refdog/resources/site.md), the target outline is a resource description, examples, and distinct metadata/spec/status sections with actual field headings. One topic per resource is a reasonable starting point; avoid automatically creating a topic for every property. Very large field descriptions can be extracted after review.

For [the Site concept](../input/refdog/concepts/site.md), preserve figures and captions currently authored in [concept configuration](../refdog/config/concepts/site.yaml). CRD-driven simplification should not erase this explanatory content.

## 5. Map known objects to DITA deliberately

Use a supported DITA shell and validate these choices during the pilot. The following are proposed mappings, not a writer already implemented:

| Object or content | Candidate DITA structure |
| --- | --- |
| CLI command or resource | `reference` topic with `refbody` |
| Command usage | `refsyn`, with a block representation appropriate to the chosen shell |
| Options and resource fields | Titled sections; `properties` or tables for genuinely tabular facts |
| Long descriptions and enum explanations | Block content in sections rather than forced single-line cells |
| Examples and transcripts | `example` containing suitable code or preformatted blocks |
| Concept description and figures | `concept`/`conbody` with structured figures and images |
| Collection indexes and command hierarchy | Maps/navigation, with overview topics retained where they contain useful prose |
| Supporting `topics/` pages | Individually reviewed task, concept, reference, or placeholder disposition |

DITA's reference type supports structures including `refsyn` and `properties`; the final mapping must still respect the selected content model. [OASIS DITA 1.3 reference element](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/technicalContent/reference.html).

Keep relationships as logical object references in the model instead of hard-coded `/docs/refdog/*.html` URLs. Generate website URLs for Markdown and map keys for DITA. DITA key references can address a topic or an identified element within it, allowing a property link to retain its own stable identity. [OASIS key-based addressing](https://docs.oasis-open.org/dita/dita/v1.3/os/part3-all-inclusive/archSpec/base/using-keys-for-addressing.html).

Do not treat short placeholder pages as completed topics. Review inbound links, supply the intended content, point readers to an existing equivalent, or deliberately omit the placeholder with an accounted-for link change.

## 6. Validate facts, structure, and publication separately

1. **Pin inputs and provenance.** Record the CLI revision/export, CRD revision, selected API versions, editorial metadata revision, and generator version. Treat missing or unparsed sources as an explicit validation outcome.
2. **Validate normalized facts.** Compare command and flag inventories, argument roles, inherited options, defaults, resource identities, nested field paths, required membership, and enum values against their authoritative inputs. Validate example YAML against the selected schema where practical; schema validity does not establish runtime success.
3. **Review representative objects.** Start with `site create`, the Site resource, the Site concept, and their collection indexes. Include an inherited/global option, an array/object field, a boolean without a default, an enum, a figure, and an inter-object link.
4. **Cross-check generated Markdown.** IWE and remark should see the same file manifest and heading outline after representation normalization. AST can inspect field headings and block ownership; IWE provides an independent structural inventory. Existing equal totals do not expose properties hidden inside HTML.
5. **Validate DITA only after the model is reviewed.** Check well-formed XML, the chosen DITA grammar, IDs, maps/keys, links, escaping, images, and an actual publication build. Compare the represented option/field IDs with the reviewed model, not merely the number of XML files.
6. **Check reproducibility and ownership.** Generate into an isolated directory, compare the expected file manifest, and account for removed/renamed objects. Only clean files owned by the generator; the current shared tree includes supporting topics and assets. Make a second generation produce the same artifacts from the same inputs.

Current read-only baseline commands, from the repository root:

```bash
mkdir -p output/refdog-review

python3 analyse/iwe_report.py --workspace . --scan refdog \
  --report files --format json --strict \
  -o output/refdog-review/iwe-files.json

node analyse/dita-report.mjs --scan input/refdog --format json \
  -o output/refdog-review/ast-model.json
```

Scanning `input/refdog` explicitly works with the existing AST CLI: its exclusion prunes child directories named `refdog`, not the selected root itself. AST paths are relative to that root; IWE paths include `refdog/`. Normalize that prefix before comparison. The AST output requires a new filename for each run. Neither command regenerates source documentation.

## Suggested implementation order

First document the active generation path and pin reproducible inputs. Next export and validate the existing objects, making merge precedence and omissions visible. Pilot semantic Markdown output for one command and one resource while preserving their old links. Then add concepts, figures, and navigation to the same reviewed model. A DITA writer can follow once that pilot preserves the facts and relationships in both generated structure and rendered output.

This confines most simplification to a few shared generators and source contracts, instead of maintaining edits across 88 generated/supporting Markdown files.
