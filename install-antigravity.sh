#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/dexterjin/explain-diff.git"
DEST="${HOME}/.gemini/config/skills/explain-diff"
PARENT="$(dirname "$DEST")"

mkdir -p "$PARENT"

if [ -d "$DEST/.git" ]; then
  echo "Updating explain-diff in $DEST"
  git -C "$DEST" pull --ff-only
  exit 0
fi

if [ -e "$DEST" ]; then
  echo "Cannot install: $DEST already exists and is not a git checkout." >&2
  echo "Move or remove that directory, then run this installer again." >&2
  exit 1
fi

echo "Installing explain-diff to $DEST"
git clone --depth 1 "$REPO_URL" "$DEST"
echo "Installed. Antigravity global skill path: $DEST"
