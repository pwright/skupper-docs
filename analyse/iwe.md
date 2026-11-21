# IWE tree reports

A **read-only IWE CLI wrapper** that inventories Markdown in a directory tree and reports structural counts. It does **not** implement its own Markdown parser.

It selects Markdown file keys using the filesystem, excludes unwanted directories, obtains the block structure from IWE, and aggregates IWE's output.

## Requirements

- Python **3.11+** (standard library only)
- An installed [`iwe` CLI](https://iwe.md/docs/cli/) that supports the `find --project ... -f json` query surface
- An existing IWE workspace with `.iwe/config.toml`

IWE's query interface is [experimental](https://iwe.md/docs/concepts/query-language/), so CLI syntax can change between releases.

## Quick start

```bash
# Initialize only if this is not yet an IWE project:
cd /path/to/my-project
# iwe init

python3 /path/to/iwe_report.py --workspace . \
  --exclude-dir archive \
  --exclude-dir old-v1 \
  --report summary
```

This program **never** runs `iwe normalize`, `iwe update`, or any mutating command. It does not alter your source files.

## Examples

```bash
# All included Markdown files, showing per-file structural counts:
python3 iwe_report.py --workspace . --exclude-dir archive --report files

# Heading outline, as CSV to stdout:
python3 iwe_report.py --workspace . --report headings --format csv

# JSON report in a file, with exclusion patterns in a text file:
python3 iwe_report.py --workspace . --exclude-from exclusions.txt \
  --report files --format json -o reports/files.json

# Only a subtree under your configured IWE library root:
python3 iwe_report.py --workspace . --scan guides --exclude-dir draft

# Accept IWE document keys from stdin:
printf '%s\n' 'guides/intro' 'reference/overview' | \
  python3 iwe_report.py --workspace . --keys-from - --report files --format json | jq .

# Log progress/debug information to stderr, leaving JSON clean on stdout:
python3 iwe_report.py --workspace . --verbose --verbose --report files --format json \
  2>debug.log | tee report.json
```

`exclusions.txt` example:

```text
# Any directory named archive, at any depth
archive
# A subtree relative to the library root
legacy/v1/**
# Any directory whose name ends in _generated
*_generated
```

Exclusion patterns apply to **directories**, not individual files. They prune the script's traversal before selecting IWE keys. They are not IWE exclusion settings: IWE itself may still index the rest of its configured library internally when invoked. Hidden directories are skipped, matching IWE's default behavior. Symlinked directories and files are not followed. `--scan` is relative to `[workspace].path` (or legacy `[library].path`), not necessarily the workspace root.

## Report formats

- `--report summary`: directory tree totals, including child directories (all descendants)
- `--report files`: one row per document, with title and structural counts
- `--report headings`: all heading entries including their section paths

Formats: `--format markdown` (default), `csv`, or `json`. Reports go to stdout unless `-o` is supplied.

The counts are IWE block types: headings, list **items** (ordered and unordered combined), fenced code blocks, paragraphs, tables, lists, and total blocks. Item count is **not a procedure-step count**. Procedure semantics are intentionally left for later.

## What IWE does

For each batch of selected document keys the script runs a query of this form:

```bash
iwe find --project 'key=$key,title=$title,blocks=$blocks' -f json \
  -k guides/intro -k reference/overview
```

Each result includes a `key`, `title`, and array of `blocks`, each with an IWE `type`, `path`, and `text`. The wrapper merely counts these and groups by directory. See [IWE Find](https://iwe.md/docs/agentic/find/) and [Block projection](https://iwe.md/docs/concepts/query-language/).

## Known constraints

- IWE's source document structure, not Markdown regexes, determines the reported counts.
- IWE does not label ordered vs unordered item types in the `$blocks` projection. The `items` number combines both.
- IWE drops raw HTML blocks and may normalize content for querying, but **no files are rewritten**.
- Only `.md` documents are inventoried. The wrapper deliberately avoids special handling for prerequisites, `<!--PROCEDURE-->` markers, or escaped Markdown.
- When `--strict` is enabled, the report fails if IWE did not return all selected keys; otherwise it warns on stderr.
- The IWE binary is required for actual reports. Mock-IWE tests are included to validate the orchestration, not claim an end-to-end run against a particular installed IWE version.

## Tests

```bash
python3 -m unittest discover -s tests -v
# optional if you have `just`:
just test
```

The tests use `tests/fixtures/fake_iwe.py` to return deterministic IWE-shaped JSON. A golden test compares a complete Markdown summary against `tests/golden/summary.md`. No network access or IWE installation is required for these contract tests.
