#!/usr/bin/env bash
# Configure merge drivers for this repo (run once per clone).
# See .gitattributes and scripts/merge-drivers/README.md.
set -e
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
git config merge.ourslock.driver true
git config merge.pyprojectversion.driver "python3 $ROOT/scripts/merge-drivers/pyproject_version.py %O %A %B %P"
echo "Merge drivers configured: ourslock (uv.lock), pyprojectversion (pyproject.toml)"
