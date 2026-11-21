#!/usr/bin/env python3
"""Deterministic fake IWE for contract-testing report orchestration.

Use the real `iwe` executable for actual structure parsing.
"""
import json
import sys


def block(kind, text, path=None):
    return {"type": kind, "text": text, "path": path or []}


ROWS = {
    "guides/intro": {
        "title": "Guide",
        "blocks": [
            block("header", "Guide"),
            block("header", "Install", ["Guide"]),
            block("paragraph", "Run these commands", ["Guide", "Install"]),
            block("list", "", ["Guide", "Install"]),
            block("item", "Run the command", ["Guide", "Install"]),
            block("item", "Check status", ["Guide", "Install"]),
            block("code", "kubectl get listener", ["Guide", "Install"]),
        ],
    },
    "reference/service": {
        "title": "Service reference",
        "blocks": [
            block("header", "Service reference"),
            block("paragraph", "This document explains the service", ["Service reference"]),
            block("header", "Example", ["Service reference"]),
            block("paragraph", "A command follows", ["Service reference", "Example"]),
            block("code", "kind: Listener", ["Service reference", "Example"]),
        ],
    },
    "archive/old": {
        "title": "Old content",
        "blocks": [
            block("header", "Old content"),
            block("list", ""),
            block("item", "Ignore this item"),
        ],
    },
}


def main():
    args = sys.argv[1:]
    if not args or args[0] != "find" or "--project" not in args or "-f" not in args or args[args.index("-f") + 1] != "json":
        print("fake_iwe only supports 'find --project ... -f json'", file=sys.stderr)
        return 1
    if args[args.index("--project") + 1] != "key=$key,title=$title,blocks=$blocks":
        print("unexpected projection", file=sys.stderr)
        return 1
    keys = [args[i+1] for i, arg in enumerate(args[:-1]) if arg == "-k"]
    result = [{"key": key, **ROWS[key]} for key in keys if key in ROWS]
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
