#!/usr/bin/env bash
# Test merge drivers: simulate dev → main merge with different versions.
# Run from repo root. Uses temporary branches; leaves repo on original branch.
# Requires: merge drivers already configured (./scripts/merge-drivers/setup.sh).
set -e
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
START_BRANCH="$(git branch --show-current)"
CLEANUP=1
while [ "$#" -gt 0 ]; do
  case "$1" in
    --no-cleanup) CLEANUP=0; shift ;;
    *) echo "Usage: $0 [--no-cleanup]"; exit 1 ;;
  esac
done

echo "=== Merge driver test (dev → main simulation) ==="
echo "Start branch: $START_BRANCH"

# Ensure merge drivers are configured
git config merge.ourslock.driver >/dev/null 2>&1 || { echo "Run ./scripts/merge-drivers/setup.sh first."; exit 1; }
git config merge.pyprojectversion.driver >/dev/null 2>&1 || { echo "Run ./scripts/merge-drivers/setup.sh first."; exit 1; }

# Create temp branches from current HEAD (common base)
git branch -D test-merge-main 2>/dev/null || true
git branch -D test-merge-dev  2>/dev/null || true
git branch test-merge-main
git branch test-merge-dev

# "main": version 2.0.0
git checkout test-merge-main
sed -i 's/^version = ".*"/version = "2.0.0"/' pyproject.toml
git add pyproject.toml uv.lock
git commit -m "test: main at 2.0.0" --no-gpg-sign 2>/dev/null || git commit -m "test: main at 2.0.0"
MAIN_LOCK_HASH=$(git show test-merge-main:uv.lock | md5sum)

# "dev": version 2.0.1 (patch bump) + change lockfile so it differs
git checkout test-merge-dev
sed -i 's/^version = ".*"/version = "2.0.1"/' pyproject.toml
# Ensure lockfile differs (append newline on dev so merge has two different contents)
printf '\n' >> uv.lock
git add pyproject.toml uv.lock
git commit -m "test: dev at 2.0.1" --no-gpg-sign 2>/dev/null || git commit -m "test: dev at 2.0.1"

# Merge dev into main (ours = main; we want to keep main's version and lockfile)
git checkout test-merge-main
echo "--- Merging test-merge-dev into test-merge-main ---"
if ! git merge test-merge-dev -m "test: merge dev into main" --no-gpg-sign 2>/dev/null; then
  git merge test-merge-dev -m "test: merge dev into main"
fi

# Checks
FAIL=0
echo ""
echo "--- Checks ---"
VERSION=$(grep '^version = ' pyproject.toml | head -1 | sed 's/.*"\(.*\)".*/\1/')
if [ "$VERSION" = "2.0.0" ]; then
  echo "  pyproject.toml version: $VERSION (expected 2.0.0, ours kept) OK"
else
  echo "  pyproject.toml version: $VERSION (expected 2.0.0) FAIL"
  FAIL=1
fi
CURRENT_LOCK_HASH=$(cat uv.lock | md5sum)
if [ "$CURRENT_LOCK_HASH" = "$MAIN_LOCK_HASH" ]; then
  echo "  uv.lock: matches main (ours) OK"
else
  echo "  uv.lock: content differs from main (driver should keep ours) FAIL"
  FAIL=1
fi
if grep -q "<<<<<<< " pyproject.toml 2>/dev/null; then
  echo "  pyproject.toml: conflict markers still present (resolve if not version-only)"
fi

if [ "$CLEANUP" -eq 1 ]; then
  git checkout "$START_BRANCH"
  git branch -D test-merge-main test-merge-dev
  echo ""
  echo "Cleaned up test branches."
fi
echo ""
[ "$FAIL" -eq 0 ] && echo "All checks passed." || { echo "Some checks failed."; exit 1; }
