# Merge drivers

Custom merge behaviour for `dev` → `main` merges where version bumps differ (patch on dev, minor on main).

| File             | Driver             | Behaviour |
|------------------|--------------------|-----------|
| `uv.lock`        | `ourslock`         | Always keep **current** (ours) version. No conflict. |
| `pyproject.toml` | `pyprojectversion` | Keep **current** for `[project]` `version`; other conflicts stay as markers. |

## Setup (once per clone)

From the repo root:

```bash
./scripts/merge-drivers/setup.sh
```

Or manually:

```bash
git config merge.ourslock.driver true
git config merge.pyprojectversion.driver "python3 $(git rev-parse --show-toplevel)/scripts/merge-drivers/pyproject_version.py %O %A %B %P"
```

## Testing

From the repo root, after configuring the drivers:

```bash
./scripts/merge-drivers/setup.sh
./scripts/merge-drivers/test-merge-drivers.sh
```

The test creates temporary branches `test-merge-main` and `test-merge-dev` with different versions and lockfile content, merges dev into main, then checks that `pyproject.toml` version and `uv.lock` are the "ours" (main) version. Branches are deleted unless you pass `--no-cleanup`.
