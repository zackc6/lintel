#!/usr/bin/env bash
# Run from a machine with rights to create repos under your GitHub user:
#   ./scripts/publish-to-github.sh zackc6/lintel
set -euo pipefail
DEST="${1:-zackc6/lintel}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "not a git repo: $ROOT" >&2
  exit 1
fi
gh repo create "$DEST" --public --source=. --remote=origin --push \
  --description "Year-1 commercial plan: compiler control plane (hybrid agents + classical compilers)"
echo "Published https://github.com/${DEST}"
