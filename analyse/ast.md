# Remark AST analysis

A read-only Markdown analyzer that uses remark to propose semantic classifications and DITA elements for review. It does not generate DITA or change source files.

## Run the DITA analyzer

Requires Node.js 20.11+ and npm. From the repository root:

```bash
npm --prefix analyse ci --ignore-scripts
node analyse/dita-report.mjs
node analyse/dita-report.mjs --format json
```

The default scan is **`input/`, excluding `input/refdog/`**. All directories named `refdog` are pruned, along with hidden entries, `node_modules`, and symlinked files and directories. Files ending in `.md` (case insensitive) are included. This tool operates directly on Markdown; it does not require an IWE workspace or query IWE.

Reports go to stdout by default. To save review artifacts, create an output directory and select new filenames:

```bash
mkdir -p output/dita-review
node analyse/dita-report.mjs --format json -o output/dita-review/input-model.json
node analyse/dita-report.mjs -o output/dita-review/input-report.md
```

Output paths must be outside the scanned tree. Existing output files are refused, including symlinks and hard links, so choose a new filename for each review. `output/` is ignored by Git. `--scan DIR` selects a different tree; repeat `--exclude-dir NAME` to prune additional directory names. Unlike the IWE tool, exclusions here are literal names, not glob patterns. Reads or writes that fail produce a nonzero exit and an error on stderr.

## Model and classification rules

`analyzeMarkdown(markdown, path)` in `dita-analyzer.mjs` is the pure interface: Markdown in, a document model out. `renderReport(model)` renders the combined model as a Markdown review report. Filesystem discovery and report output belong to the CLI.

Parsing uses unified with remark-parse, remark-gfm, and remark-frontmatter. Headings and recognized standalone bold labels start sections. Each section has a stable document-local ID, heading parent ID, source range, classification, confidence, evidence, warnings, positioned mdast blocks, original Markdown slices, and candidate DITA elements with source ranges. Section ranges cover their own blocks rather than overlapping descendant sections. Frontmatter is retained separately without interpreting its YAML values. Positions are one-based, inclusive line ranges; mdast also retains columns and offsets into the original string. HTML headings inside raw HTML are not promoted to Markdown sections.

The top-level JSON contains `schemaVersion`, `analyzer`, `root`, `summary`, and `documents`. Each document contains `path`, `title`, `source`, `hasFrontmatter`, `frontmatter`, `topic`, `warnings`, and `sections`. Paths are relative to the scan root. Output order is deterministic. There is no generated timestamp.

Classifications are `prerequisites`, `procedure`, `result`, `example`, `reference`, or `unknown`. Signals, strongest first:

1. Explicit heading or bold labels, such as **Prerequisites**, **Procedure**, **Results**, **Examples**, or **Additional resources** (0.95).
2. `<!--PROCEDURE-->` and `<!--REFERENCE-->` comments (0.90).
3. A direct ordered list (procedure, 0.60) or GFM table (reference, 0.55).
4. Otherwise unknown (0.20), with a review warning.

Procedure evidence suggests a task; otherwise reference evidence suggests a reference; otherwise the topic is provisionally a concept. A `<!--CONCEPT-->` marker supports the concept fallback. **Confidence is an explainable rule weight, not a calibrated probability or an assessment of DITA validity.** One procedure in a large reference file can therefore trigger a task inference; mixed-topic warnings call attention to this.

Element candidates include `prereq`, `steps`, `step`, `cmd`, `info`, `steps-informal`, `result`, `example`, `section`, `ul`, `ol`, `codeblock`, `table`, and `note`. Nested list items are not counted as additional top-level steps. These are review hints: for example, a blockquote may need `lq` rather than `note`, and ordered items may be rankings rather than instructions. No XML is emitted and no DITA content model is validated.

A procedure section directly inside another procedure gets `NESTED_PROCEDURE`, whether introduced by a heading or a bold label. The warning names the parent line for review as a possible authoring mistake or intentional grouping. Every procedure without its own ordered list retains `NO_ORDERED_STEPS`; the analyzer does not silently reinterpret it as context.

Warnings identify unknown sections, tentative topic types, raw HTML, template/include/admonition syntax, procedures without direct ordered steps, mixed topic evidence, multiple procedures, and assembly markers. Nested step examples and results remain within the step's positioned AST; they are not separately assigned semantic classifications. Link targets and includes are not resolved, and macros are not expanded.

## Review before adding a writer

The initial scoped run covered 32 files and 285 sections. It inferred 20 tasks, 7 references, and 5 concepts, with 177 warnings. These counts are a baseline, not reviewed labels. After adding explicit nested-procedure warnings and retaining missing-step warnings, the report contains 270 warnings, including 47 `NESTED_PROCEDURE` warnings.

Start review with these real documents:

- `input/kube-cli/site-linking.md`: multiple procedures, prerequisites, and code examples. The task inference needs topic splitting because the file is an assembly.
- `input/install/cli.md`: an explicit procedure with prose and commands but no ordered list; `steps-informal` needs editorial review.
- `input/console/configuration.md`: reference tables alongside an embedded procedure. Review the mixed-topic warning before deciding whether to split it.
- `input/overview/index.md`: conceptual content with macros and an assembly marker; review unknown sections and unresolved template syntax.

Record corrections against document paths, section IDs, and lines. Review all six classes, especially ambiguous ordered lists, additional-resource sections, nested examples, and raw HTML. Use the corrections to refine rules or establish explicit overrides. Only then design a DITA writer against the reviewed model, including topic splitting, valid content ordering, IDs, links, and validation. The writer is deliberately deferred.

## Tests

```bash
npm --prefix analyse test
python3 -m unittest discover -s analyse/tests -v
```

The Node tests cover positioned procedure classifications, nested lists, frontmatter, GFM tables, raw HTML warnings, unknown content, assemblies, informal steps, deterministic traversal, refdog exclusion, symlink skipping, and refusal to overwrite sources. The Python command runs the existing IWE tests.
