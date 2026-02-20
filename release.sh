#!/usr/bin/env bash
set -euo pipefail

# Guardrail: run from repo root.
if [[ ! -f "pyproject.toml" ]]; then
  echo "Run this from your project root (where pyproject.toml lives)."
  exit 1
fi

echo "==> Cleaning up existing distributions"
rm dist/*.whl dist/*.tar.gz

echo "==> Current version:"
uv version

echo "==> Bumping patch"
uv version --bump patch

echo "==> New version:"
uv version

echo "==> Building distributions"
uv build --no-sources

echo "==> Publishing to index"
uv publish

echo "==> Release complete."
