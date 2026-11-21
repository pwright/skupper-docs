#!/usr/bin/env python3
"""Read-only, IWE-backed reports for Markdown directory trees.

Source of structure: `iwe find --project 'key=$key,title=$title,blocks=$blocks' -f json`.
Directory traversal chooses document keys; it never parses Markdown content.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import io
import json
import logging
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tomllib
from collections import Counter
from typing import Any, Iterable, Mapping

LOG = logging.getLogger("iwe-report")
COLUMNS = ("files", "headings", "items", "code", "paragraphs", "tables", "lists", "blocks")
TYPE_TO_COLUMN = {
    "header": "headings",
    "item": "items",
    "code": "code",
    "paragraph": "paragraphs",
    "table": "tables",
    "list": "lists",
}


class ReportError(Exception):
    """Expected failure that should be reported without a traceback."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report on IWE-parsed Markdown, with directory exclusions."
    )
    parser.add_argument(
        "--workspace", type=Path, default=Path.cwd(),
        help="IWE project root containing .iwe/config.toml (default: cwd)",
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--scan", default=".", metavar="SUBDIR",
        help="Directory beneath IWE library root to scan (default: .)",
    )
    selection.add_argument(
        "--keys-from", metavar="FILE",
        help="Read IWE document keys, one per line; '-' reads stdin",
    )
    parser.add_argument(
        "--exclude-dir", action="append", default=[], metavar="NAME_OR_GLOB",
        help="Exclude directory by name anywhere, or library-relative glob; repeatable",
    )
    parser.add_argument(
        "--exclude-from", type=Path, metavar="FILE",
        help="Text file of directory exclusions (one per line; # comments)",
    )
    parser.add_argument("--report", choices=("summary", "files", "headings"), default="summary")
    parser.add_argument("--format", choices=("markdown", "csv", "json"), default="markdown")
    parser.add_argument("--output", "-o", default="-", metavar="FILE", help="Output path or '-' for stdout")
    parser.add_argument("--iwe", default="iwe", help="IWE executable (default: iwe)")
    parser.add_argument("--batch-size", type=int, default=64, help="Keys per IWE query (default: 64)")
    parser.add_argument("--strict", action="store_true", help="Fail if IWE omits an eligible key")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Progress/debug logs to stderr")
    return parser.parse_args(argv)


def library_root(workspace: Path) -> Path:
    config = workspace / ".iwe" / "config.toml"
    if not config.is_file():
        raise ReportError(f"No IWE project at {workspace}: missing {config}. Run 'iwe init' first.")
    try:
        data = tomllib.loads(config.read_text(encoding="utf-8"))
        section = data.get("workspace", data.get("library", {}))
        rel = section.get("path", "")
    except (OSError, ValueError, TypeError) as exc:
        raise ReportError(f"Cannot read IWE configuration {config}: {exc}") from exc
    if not isinstance(rel, str):
        raise ReportError("[workspace].path (or legacy [library].path) must be a string")
    root = (workspace / rel).resolve()
    if not root.is_dir() or not root.is_relative_to(workspace):
        raise ReportError("Configured Markdown path must point to a directory inside the workspace")
    return root


def read_exclusions(args: argparse.Namespace) -> list[str]:
    items = list(args.exclude_dir)
    if args.exclude_from:
        try:
            with args.exclude_from.open(encoding="utf-8") as stream:
                items.extend(line.strip() for line in stream if line.strip() and not line.lstrip().startswith("#"))
        except OSError as exc:
            raise ReportError(f"Cannot read exclusions: {exc}") from exc
    return [pattern.strip().strip("/") for pattern in items if pattern.strip().strip("/")]


def is_excluded(relative_dir: PurePosixPath, rules: list[str]) -> bool:
    """Exclude a directory and all descendants; patterns are library-relative."""
    parts = relative_dir.parts
    if any(part.startswith(".") for part in parts):
        # IWE's library scanner skips hidden folders, so mirror that rule.
        return True
    path = relative_dir.as_posix()
    for rule in rules:
        if "/" not in rule and fnmatch.fnmatchcase(relative_dir.name, rule):
            return True
        prefix = rule.removesuffix("/**")
        if "/" in rule or rule.endswith("/**"):
            if fnmatch.fnmatchcase(path, rule) or path == prefix or path.startswith(prefix + "/"):
                return True
    return False


def valid_key(value: str) -> str:
    value = value.strip().removesuffix(".md")
    path = PurePosixPath(value)
    if not value or value.startswith("/") or "\\" in value or ".." in path.parts or "." in path.parts:
        raise ReportError(f"Invalid IWE key: {value!r}")
    return path.as_posix()


def discover_keys(root: Path, scan: str, rules: list[str]) -> list[str]:
    scan_path = (root / scan).resolve()
    if not scan_path.is_relative_to(root) or not scan_path.is_dir():
        raise ReportError(f"Scan path must be an existing directory inside {root}: {scan}")
    keys: list[str] = []
    for directory, subdirs, files in os.walk(scan_path, topdown=True, followlinks=False):
        current = Path(directory)
        rel = current.relative_to(root)
        if rel != Path(".") and is_excluded(PurePosixPath(rel.as_posix()), rules):
            subdirs.clear()
            continue
        subdirs[:] = sorted(
            sub for sub in subdirs
            if not (current / sub).is_symlink()
            and not is_excluded(PurePosixPath((rel / sub).as_posix()), rules)
        )
        for filename in sorted(files):
            if filename.startswith(".") or not filename.lower().endswith(".md"):
                continue
            fpath = current / filename
            if fpath.is_symlink() or not fpath.is_file():
                continue
            keys.append(fpath.relative_to(root).with_suffix("").as_posix())
    return keys


def read_keys(file: str, rules: list[str]) -> list[str]:
    try:
        if file == "-":
            raw = sys.stdin.read()
        else:
            raw = Path(file).read_text(encoding="utf-8")
    except OSError as exc:
        raise ReportError(f"Cannot read key list: {exc}") from exc
    selected = []
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key = valid_key(line)
        parents = PurePosixPath(key).parents
        if any(str(parent) != "." and is_excluded(parent, rules) for parent in parents):
            continue
        selected.append(key)
    return sorted(set(selected))


def query_iwe(workspace: Path, binary: str, keys: list[str], batch_size: int) -> list[dict[str, Any]]:
    if batch_size < 1:
        raise ReportError("--batch-size must be a positive integer")
    records: dict[str, dict[str, Any]] = {}
    for first in range(0, len(keys), batch_size):
        batch = keys[first:first + batch_size]
        cmd = [binary, "find", "--project", "key=$key,title=$title,blocks=$blocks", "-f", "json"]
        for key in batch:
            cmd.extend(("-k", key))
        LOG.info("Querying IWE for %d keys (%d/%d)", len(batch), first + len(batch), len(keys))
        LOG.debug("IWE arguments: %r", cmd)
        try:
            result = subprocess.run(cmd, cwd=workspace, text=True, capture_output=True, check=False)
        except FileNotFoundError as exc:
            raise ReportError(f"IWE executable not found: {binary!r}") from exc
        except OSError as exc:
            raise ReportError(f"Cannot launch IWE: {exc}") from exc
        if result.returncode != 0:
            raise ReportError(
                f"IWE find failed (exit {result.returncode}) for {batch[0]}: "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )
        if result.stderr.strip():
            LOG.warning("IWE stderr: %s", result.stderr.strip())
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise ReportError(f"Invalid JSON from IWE: {exc}") from exc
        if not isinstance(payload, list):
            raise ReportError("Expected an array from 'iwe find -f json'")
        for row in payload:
            if not isinstance(row, dict) or not isinstance(row.get("key"), str) or not isinstance(row.get("blocks"), list):
                raise ReportError("IWE result must include 'key' and 'blocks' fields")
            if row["key"] in batch:
                records[row["key"]] = row
            else:
                LOG.warning("Ignoring unexpected key from IWE: %r", row["key"])
    return [records[key] for key in keys if key in records]


def count_blocks(blocks: list[Any]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    counts["files"] = 1
    for block in blocks:
        if not isinstance(block, dict) or not isinstance(block.get("type"), str):
            raise ReportError("Invalid IWE block entry (expected object with 'type')")
        counts["blocks"] += 1
        name = TYPE_TO_COLUMN.get(block["type"])
        if name:
            counts[name] += 1
    return {col: counts[col] for col in COLUMNS}


def make_rows(records: list[dict[str, Any]], report: str) -> list[dict[str, Any]]:
    if report == "headings":
        return [
            {"file": row["key"] + ".md", "section": " / ".join(block.get("path", [])), "heading": block.get("text", "")}
            for row in records
            for block in row["blocks"]
            if block.get("type") == "header"
        ]
    if report == "files":
        return [
            {"file": row["key"] + ".md", "title": row.get("title", ""), **count_blocks(row["blocks"])}
            for row in records
        ]
    totals: dict[str, Counter[str]] = {}
    for row in records:
        key = PurePosixPath(row["key"])
        counts = count_blocks(row["blocks"])
        ancestors = ["."]
        ancestors.extend(parent.as_posix() for parent in reversed(key.parents) if parent.as_posix() != ".")
        for dirname in ancestors:
            totals.setdefault(dirname, Counter()).update(counts)
    return [{"directory": d, **{c: totals[d][c] for c in COLUMNS}} for d in sorted(totals, key=lambda x: (x != ".", x))]


def columns(report: str) -> list[str]:
    return {
        "summary": ["directory", *COLUMNS],
        "files": ["file", "title", *COLUMNS],
        "headings": ["file", "section", "heading"],
    }[report]


def format_rows(rows: list[dict[str, Any]], report: str, fmt: str) -> str:
    fields = columns(report)
    if fmt == "json":
        return json.dumps(rows, indent=2, ensure_ascii=False) + "\n"
    if fmt == "csv":
        buf = io.StringIO(newline="")
        writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        return buf.getvalue()
    title = {"summary": "IWE directory summary", "files": "IWE document report", "headings": "IWE heading outline"}[report]
    lines = [f"# {title}", ""]
    lines.append("| " + " | ".join(fields) + " |")
    lines.append("| " + " | ".join("---:" if field in COLUMNS else "---" for field in fields) + " |")
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    lines.append("")
    return "\n".join(lines)


def emit(content: str, destination: str) -> None:
    if destination == "-":
        sys.stdout.write(content)
        return
    target = Path(destination)
    try:
        # Write atomically to avoid a truncated report on interruption.
        import tempfile
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent, prefix=f".{target.name}.", delete=False) as f:
            f.write(content)
            temp_name = f.name
        os.replace(temp_name, target)
    except OSError as exc:
        raise ReportError(f"Cannot write output to {destination}: {exc}") from exc
    LOG.info("Wrote report: %s", target)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose >= 2 else logging.INFO if args.verbose else logging.WARNING,
                        format="%(levelname)s: %(message)s", stream=sys.stderr)
    try:
        workspace = args.workspace.resolve()
        root = library_root(workspace)
        patterns = read_exclusions(args)
        keys = read_keys(args.keys_from, patterns) if args.keys_from is not None else discover_keys(root, args.scan, patterns)
        LOG.info("Selected %d Markdown documents beneath %s", len(keys), root)
        rows = query_iwe(workspace, args.iwe, keys, args.batch_size)
        missing = set(keys) - {row["key"] for row in rows}
        if missing:
            message = f"IWE did not return {len(missing)} selected keys: {', '.join(sorted(missing)[:5])}"
            if args.strict:
                raise ReportError(message)
            LOG.warning(message)
        data = make_rows(rows, args.report)
        emit(format_rows(data, args.report, args.format), args.output)
        LOG.info("Report complete: %d IWE documents, %d output rows", len(rows), len(data))
        return 0
    except (ReportError, BrokenPipeError) as exc:
        if isinstance(exc, BrokenPipeError):
            return 0
        LOG.error("%s", exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
