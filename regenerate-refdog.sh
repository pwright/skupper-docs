#!/bin/bash
# regenerate-refdog.sh
# Regenerate refdog documentation for MkDocs

set -e

cd refdog

# Determine the correct SITE_PREFIX based on where refdog is mounted
#
# For MkDocs with site_dir: output/docs and refdog at /docs/refdog/:
#   REFDOG_SITE_PREFIX="/docs/refdog"
#
# For refdog at root:
#   REFDOG_SITE_PREFIX=""
#
# Override by setting REFDOG_SITE_PREFIX environment variable
SITE_PREFIX="${REFDOG_SITE_PREFIX:-/docs/refdog}"

echo "Regenerating refdog with SITE_PREFIX='$SITE_PREFIX'"
echo "  (Set REFDOG_SITE_PREFIX env var to override)"

REFDOG_SITE_PREFIX="$SITE_PREFIX" ./plano generate

echo ""
echo "✓ Refdog regenerated successfully"
echo ""
echo "Sample links generated:"
grep -m 3 'href=' input/commands/index.md | sed 's/.*href="\([^"]*\)".*/  \1/'
echo ""
echo "Verify these links resolve correctly in your MkDocs site"
