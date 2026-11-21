#!/usr/bin/env python3
"""Validate only input Markdown, pruning refdog directories before traversal.

Run: python3 python/validate_input_docs.py --format json > schema-report.json
Requires schematter on PATH, or --schematter /path/to/schematter.
The schema is a proposal; this runner is not wired into CI or a write hook.
"""

import argparse
import os
from pathlib import Path
import subprocess
import sys


def input_documents(root: Path) -> list[Path]:
    documents = []
    for directory, subdirs, filenames in os.walk(root, followlinks=False):
        current = Path(directory)
        subdirs[:] = sorted(
            name for name in subdirs
            if name != "refdog" and not name.startswith(".")
            and not (current / name).is_symlink()
        )
        documents.extend(
            current / name for name in sorted(filenames)
            if name.lower().endswith(".md") and not name.startswith(".")
            and not (current / name).is_symlink()
        )
    return sorted(documents)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schematter", default="schematter")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    documents = input_documents(repo / "input")
    if not documents:
        print("No input Markdown documents selected", file=sys.stderr)
        return 2
    print(f"Validating {len(documents)} input documents; refdog excluded", file=sys.stderr)
    command = [args.schematter, "validate", "--schema", str(repo / "schemas/input-document.yaml"),
               "--format", args.format, *(str(path) for path in documents)]
    try:
        return subprocess.run(command, check=False).returncode
    except OSError as exc:
        print(f"Cannot run schematter: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
