# Making the input tree easier to analyze and validate

The largest simplification would be to use real headings for semantic sections and distinguish a document's topic type from the roles of its sections. That would let IWE and remark describe the same outline, and let the classifier check explicit structure rather than infer intent from formatting.

This report covers **`input/`, excluding `input/refdog/`**. It proposes changes; no source documentation or analyzer behavior was changed for this report. The current tools are described in [iwe.md](iwe.md) and [ast.md](ast.md).

## What the current tree shows

A fresh run of both analyzers found the same 32 files. The existing `.iwe/config.toml` sets the IWE library root to `input`, so IWE's `--scan .` and the AST analyzer's default `--scan input` cover the same tree when `refdog` is excluded.

| Structure | IWE | Remark AST |
| --- | ---: | ---: |
| Files | 32 | 32 |
| Markdown headings | 156 | 156 |
| List items, including nested items | 451 | 451 |
| Fenced code blocks | 282 | 282 |
| Markdown tables | 31 | 31 |

The parsers already agree on these structural totals. IWE's item count combines ordered and unordered items; it does not establish a procedure-step count. Equal totals also do not establish equal semantics or correct nesting.

The AST analyzer additionally recognizes **98 bold-label sections** and **31 preambles**, for 285 sections in total. Bold labels are paragraphs rather than heading entries in the IWE outline. The preambles commonly contain explicit HTML anchors before the first heading; they are not necessarily introductory prose.

The current AST run reports 270 warnings:

| Warning | Count | Interpretation |
| --- | ---: | --- |
| `UNKNOWN_SECTION` | 74 | Includes ordinary conceptual prose and anchor-only preambles; not necessarily missing content. |
| `NO_ORDERED_STEPS` | 54 | Includes procedure introductions and actual procedures written as prose. |
| `EXTENDED_MARKDOWN` | 49 | Often template expressions; requires awareness of the rendering layer. |
| `NESTED_PROCEDURE` | 47 | May be intentional title/section grouping or an authoring mistake. |
| `ASSEMBLY` | 19 | A file contains multiple topics or is marked as an assembly. |
| `MULTIPLE_PROCEDURES` | 16 | More than one procedure group in a file. |
| `MIXED_TOPIC` | 9 | Procedure and reference evidence coexist. |
| `RAW_HTML` | 1 | Substantive HTML flagged by the current rule, excluding recognized anchors and comments. |
| `LOW_TOPIC_CONFIDENCE` | 1 | Tentative concept fallback. |

These are rule findings, not 270 confirmed writing mistakes. Several can describe the same underlying structure. Do not use zero warnings as the immediate acceptance criterion.

## 1. Make section boundaries real headings

Use `## Prerequisites`, `## Procedure`, `## Result`, `## Examples`, and `## Related information` where those are actual sections. Keep bold text for emphasis or labels within a paragraph or list item.

For a topic currently embedded under an H2 assembly heading, use H3 for its semantic sections. For a standalone topic with an H1 title, use H2. Keep headings subordinate to the section they describe and avoid skipped levels.

Examples in the current tree:

- [Link sites using the CLI](../input/kube-cli/site-linking.md) uses bold prerequisites, procedure, and additional-resource labels underneath procedure headings. These boundaries are visible to the AST classifier but absent from the IWE heading report.
- [Set site resources using YAML](../input/kube-yaml/site-configuration.md) places `### Router CPU allocation` between bold **Prerequisites** and **Procedure** labels. The classifier attaches the later bold procedure to the most recent real heading. Explicit prerequisite and procedure headings would make the intended ownership visible to both parsers.
- [Upgrade sites](../input/install/upgrade.md) goes from an H1 title to H3 procedure headings. Choosing consistent levels would make the hierarchy easier to validate.

This removes the need for the AST analyzer's special case that treats selected bold paragraphs as section boundaries. It also makes a section-outline comparison with IWE possible. It does **not** automatically resolve the distinction between a topic and its procedure section; that needs the next change.

## 2. Declare topic type once, separately from section roles

Currently `<!--PROCEDURE-->` can mark a topic heading, while **Procedure** marks a section within it. The analyzer classifies both as procedures, producing the nested-procedure ambiguity discussed during review.

Adopt one document-level declaration with a small vocabulary: `task`, `concept`, `reference`, or `assembly`. A proposed field is `topic_type` in YAML frontmatter. Keep existing fields such as `skip`, `navtitle`, and `type: module`; they serve other purposes.

A proposed standalone task structure is:

```markdown
---
topic_type: task
---
# Link two sites

Explain the goal and context.

## Prerequisites

- Two sites are available.

## Procedure

1. Issue a token on the first site.
2. Redeem the token on the second site.

## Result

The sites are linked.

## Related information

- [Site configuration](site-configuration.md)
```

**This is a proposed convention, not functionality already supported.** The AST analyzer preserves frontmatter but does not interpret `topic_type`; the IWE wrapper does not project topic metadata. The AST analyzer would need to read the declaration and validate the sections under it. IWE can continue checking the heading outline; metadata agreement would require an additional metadata projection if supported, or a separate metadata check.

Under that convention, an H1 title is a topic title, and `## Procedure` is a section role. Only a procedure nested inside another procedure *section* should trigger the semantic nesting check. A normal task title containing its procedure section should not. Keep the current ambiguity warnings until that distinction is implemented and reviewed.

Do not infer the topic type from **Related information** or from the mere presence of a table. A conceptual topic can legitimately contain both. Explicit type would let those heuristics become fallback behavior for legacy files.

## 3. Keep a single task together; separate independently usable tasks

After section headings are consistent, extract topics where a file contains several independently usable procedures. Keep assembly pages as short introductions and links, rather than classifying an entire collection as one task.

For example:

- [CLI site linking](../input/kube-cli/site-linking.md) contains token linking, link-resource linking, proxy linking, certificate guidance, and link-cost configuration. Those are candidates for separate topics linked from the current page.
- [Network Observer configuration](../input/console/configuration.md) primarily contains reference tables but also a persistent-storage procedure. Extracting that procedure would allow the remaining file to have a clear reference purpose.

This would make one file a useful unit for topic-type review and later DITA writing. It would reduce the need to infer topic boundaries, inherit prerequisites across unrelated procedures, or choose a single type for mixed content.

File splitting has a higher cost than heading cleanup. Preserve existing URLs and anchor destinations through an explicit compatibility plan, update relative links and navigation, and check rendered pages. Do not split every example or explanatory table into a separate file. Pilot a small group before reorganizing the tree.

## 4. Make steps and supporting content unambiguous

Use an ordered list for a sequence of actions. Keep each action's explanation, example, command, and expected output inside that list item through consistent indentation. Use unordered lists for prerequisites and options.

For [Install the Skupper CLI](../input/install/cli.md), decide whether the prose describes a sequence, alternative installation methods, or an intentionally informal procedure. Turn it into steps only if order matters. Explicitly allow an informal form when that better represents the instructions; do not manufacture a sequence merely to silence a warning.

Follow the existing [style guide](../style.md) for command and output separation. In [Check the Skupper CLI](../input/kube-cli/site-configuration.md), one `bash` block currently contains both `skupper version` and its output. Separate command and output blocks would make their roles clearer. Elsewhere in that file, unindented explanatory prose interrupts a numbered step; reviewing ownership would prevent examples or explanations from being interpreted outside their intended step.

With these conventions, AST checks can establish that a procedure has an ordered list, identify its direct steps, and verify that supporting blocks belong to those steps. IWE can cross-check list-item and code-block inventories, but its current projection cannot independently verify ordered-step semantics. A command's correctness and the accuracy of its expected output still need editorial or execution-based review.

## 5. Keep source structure independent of rendering conveniences

Prefer Markdown images and tables when they express the same content. The substantive HTML warning in this scope is the `<img>` in [Explore the Network console](../input/console/index.md); the file already has a commented Markdown image nearby. Review whether the inline width styling is necessary before replacing it.

Treat explicit anchors and content markers separately from substantive HTML. There is little benefit in rewriting all anchors to remove warnings: they preserve link targets and are also consumed by repository tooling. Instead, the analyzer can attach recognized anchor-only preambles to their topic and avoid treating them as unknown prose.

Keep template expressions out of structural labels such as `Procedure` and `Prerequisites`. Product names in titles and prose can remain parameterized. [The overview](../input/overview/index.md) uses `{{skupper_name}}`, and the MkDocs configuration enables a macros plugin. Analyze source structure first; use a separate rendered-page check for expanded values and links. Expanding templates before source analysis would make source positions harder to preserve.

## What should change in the tools instead of the documentation

Several complications belong in the analyzers or comparison logic:

| Complication | Simpler handling |
| --- | --- |
| Topic title and procedure section both classified as procedures | Interpret declared topic type separately from heading section roles. |
| Ordinary conceptual prose classified as unknown | Distinguish unclassified prose from a structural violation; allow context within a declared topic. |
| Anchor-only preambles counted as unknown sections | Preserve anchors as topic metadata rather than prose sections. |
| Different heading strings for inline code | Compare normalized text while retaining original Markdown for display. |
| Assembly files forced into task/reference/concept | Add an explicit assembly review path before topic extraction. |
| Valid extension syntax reported generically | Recognize the small set of approved template and admonition forms; retain warnings for unsupported forms. |

Five files had heading-text differences in the current comparison, all explained by inline-code formatting in the inspected outlines. For example, IWE retains the backticks in “Link sites using a `link` resource”, whereas the AST title is “Link sites using a link resource”. Do not remove useful inline code from documentation to make raw strings equal. Normalize the IWE text through Markdown parsing for comparison, or compare the AST heading's original source with IWE's Markdown representation.

The current AST analyzer also reports a possible `note` for any blockquote. Source cleanup alone cannot establish whether a quotation is a note. Recognizing an explicit note label or retaining ambiguity is a tool responsibility.

## A practical validation workflow

1. **Freeze scope and establish a baseline.** Compare the same file set in both tools and record current outlines and counts. Use paths as document identities; AST section IDs depend on document order and can change when sections are inserted. Track review findings by path, heading, and current source lines.
2. **Pilot one assembly and one standalone task.** Use CLI site linking and CLI installation. First convert genuine section labels into headings. Review nesting and rendered output before extracting topics.
3. **Review an expected model by hand.** Record each pilot's topic type, expected section order, direct procedure-step count, examples, and accepted exceptions. Agreement between two parsers is supporting evidence, not the expected model itself.
4. **Compare like with like.** Join IWE's `file` and AST's `documents[].path`. Compare normalized heading outlines and matching block inventories per file. Compare actual heading blocks, not the AST's broader section count. Do not equate IWE items with AST procedure steps.
5. **Add explicit structural checks.** After agreeing on the conventions, validate one H1, orderly heading levels, allowed topic types, required task sections, ordered steps or an approved informal form, and duplicate or conflicting section roles. These are proposed checks; the current analyzers do not enforce this entire contract.
6. **Validate publication compatibility.** Build the documentation and check navigation, old anchor targets, relative links, images, and macro expansion. Accept intentional count changes with an explanation. Splitting files or converting labels to headings should change counts.

Commands for the current read-only baseline, from the repository root:

```bash
mkdir -p output/structure-review

python3 analyse/iwe_report.py --workspace . --scan . \
  --exclude-dir refdog --report files --format json --strict \
  -o output/structure-review/iwe-files.json

python3 analyse/iwe_report.py --workspace . --scan . \
  --exclude-dir refdog --report headings --format json --strict \
  -o output/structure-review/iwe-headings.json

node analyse/dita-report.mjs --scan input --format json \
  -o output/structure-review/ast-model.json
```

The AST command excludes `refdog` automatically and requires a new output filename on subsequent runs. The IWE wrapper permits replacing its report output. These commands produce evidence for comparison; they do not implement an automatic cross-validator.

## Compatibility work before adopting the conventions

[generate-job-mapping.py](../python/generate-job-mapping.py) currently recognizes H1/H2 headings, explicit HTML anchors, and content-type comments immediately after headings. Changing labels to H3 headings, replacing markers with frontmatter, or extracting files requires reviewing that script, its category mappings, the job mapping CSV, and generated MkDocs navigation. The current conventions are inputs to that tooling, not just presentation choices.

Start with semantic headings and consistent step ownership. Next introduce a distinct topic declaration with compatible tooling changes. Split selected assemblies only after that pilot is reviewed. The measurable outcome should be fewer ambiguous classifications and a simpler set of explicit structural checks, while preserving useful prose, examples, and published links. A DITA writer remains a later step.
