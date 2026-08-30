# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project overview

**PFMG** (package name `pfmg`) is a Python library for morphological and grammatical processing. It includes lexicon management, parsing, and grammar tooling. The project also ships CUE schemas (`schemas/`) and example data under `pfmg/data/` (including Kalaba).

Primary language: **Python 3.14** (strict: `>=3.14,<3.15`).

## Repository layout

| Path | Purpose |
|------|---------|
| `pfmg/` | Main Python package |
| `pfmg/lexique/` | Lexicon, morphology, stems, paradigms |
| `pfmg/parsing/` | Grammar, parser, tokenizer, indexer |
| `pfmg/external/` | Integrations (gloser, reader, display, etc.) |
| `schemas/` | CUE schema definitions |
| `examples/` | Usage examples |
| `doc/` | Antora AsciiDoc book (Kalaba, FR + EN) |
| `docker-compose.yml` | Docker services (documentation build) |
| `scripts/` | Utility scripts |
| `package.json` | Commitlint and Antora (documentation build) |

## Setup

Use **uv** for Python dependencies:

```bash
uv sync --all-groups
```

NLTK data (`wordnet`) is downloaded automatically on first parse (when a
`Parser` or `KParser` is built). For CI or manual setup:

```bash
uv run python -m nltk.downloader wordnet
```

For commit message linting:

```bash
npm install
```

On NixOS, install `nodejs` via `configuration.nix` (not `npm install -g`). Global npm upgrades do not work against the read-only Nix store.

## Development commands

Prefer **Makefile** targets:

```bash
make install       # uv sync --all-groups
make lint          # pylint + ruff check
make format        # ruff format
make format-check  # ruff format --check
make type          # ty check
make test          # pytest with coverage
make check         # lint + format-check + type + test
make docs          # Antora site via Docker (docker compose build first)
```

Equivalent direct commands:

```bash
uv run ruff check
uv run ruff format
uv run ty check
uv run pytest
```

Pre-commit hooks run ruff, ty, pytest, pylint, and commitlint. Install with:

```bash
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

## Code conventions

- **Language**: write new code, comments, docstrings, and user-facing strings in **English**.
- **Formatter**: Ruff (Black-compatible, line length 88, 4-space indent).
- **Linter**: Ruff + Pylint. Google-style docstrings (`ruff.toml`).
- **Type checker**: `ty` (not mypy).
- **Tests**: pytest. Test files live next to code under `test/` directories.
- **Scope**: keep changes minimal and focused. Match existing naming and patterns.
- **Formatting**: Ruff does not format files under `**/test/**`; do not reformat test files unless asked.

## Testing

```bash
make test
# or
uv run pytest -vv --showlocals
```

Add tests for real behavior. Avoid trivial tests that only assert the obvious. Test data is often YAML under `**/test/data*/`.

## Git and CI

- **Branches**: CI runs on `dev` and `main`.
- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) enforced by commitlint (`feat:`, `fix:`, `chore:`, etc.).
- **Commits**: do not create git commits unless the user explicitly asks.
- **PRs**: use the template in `.github/PULL_REQUEST_TEMPLATE.md`.

CI runs on changed Python files: ruff check, ruff format (non-test files only), pylint, ty, and full pytest.

## Updating dependencies

**Python** (updates `pyproject.toml` and `uv.lock`):

```bash
uv lock --upgrade
uv sync --all-groups
```

**Node** (commitlint and Antora; updates `package.json` and `package-lock.json`):

```bash
npx npm-check-updates -u
npm install
```

Do not use `npm install -g` on NixOS.

## External tools

- **CUE**: schemas in `schemas/`. The `cue` CLI may be required for schema work (see `README.md`).
- **pycue**: Python CUE bindings are a runtime dependency.

## Agent guidelines

1. Read surrounding code before editing; follow existing abstractions.
2. Run `make check` (or the relevant subset) after substantive Python changes.
3. Do not edit unrelated files, lockfiles, or generated artifacts unless required.
4. Do not add markdown/docs files unless requested.
5. Prefer `uv run` over bare `python`/`pytest`/`ruff`.
6. Domain terms in French (e.g. gloses, lexique) are intentional; keep them when they match the codebase.
