# PFMG

**PFMG** (package name `pfmg`) is a Python library for morphological and grammatical
processing. It provides lexicon management (paradigm-based realization), FCFG parsing
with NLTK, and French-to-invented-language translation (Kalaba and similar grammars).

Grammars are defined as YAML configuration files. Their intended shape is described by
CUE schemas in [`schemas/`](schemas/) (manual validation with `cue vet` only — the
library does not validate YAML at runtime). See the
[`doc/`](doc/) Antora book for the runtime format used by `examples/data/`.

## Requirements

- Python 3.14 (`>=3.14,<3.15`)
- [uv](https://docs.astral.sh/uv/) for dependency management

## Installation

```bash
uv sync --all-groups
```

NLTK data (`wordnet`) is downloaded automatically on first parse (when a
`Parser` or `KParser` is built). To install it manually or in CI:

```bash
uv run python -m nltk.downloader wordnet
```

## Grammar configuration

A grammar consists of five YAML files in a single directory:

| File | Role |
|------|------|
| `Gloses.yaml` | Attribute–value pairs used in the grammar |
| `Blocks.yaml` | Morphological realization rules |
| `Stems.yaml` | Lexical stems and inheritance |
| `Phonology.yaml` | Phonological transformation rules |
| `MorphoSyntax.yaml` | Syntactic rules, agreements, and translations |

See [`examples/README.md`](examples/README.md) for runnable examples,
[`schemas/README.md`](schemas/README.md) for CUE schema details, and
[`doc/`](doc/) for the full Kalaba grammar book (French and English).

## Command-line usage

**Lexicon realization** (build and list lexical forms from a grammar directory):

```bash
uv run python -m pfmg.lexique.main.main lexicon examples/data
```

**Parsing / translation** (parse French input and produce target-language output):

```bash
uv run python -m pfmg.parsing.main parsing examples/data "des garçons"
```

Use `-k all` to keep all parse results instead of only the first:

```bash
uv run python -m pfmg.parsing.main parsing examples/data "des garçons" -k all
```

## Examples

The [`examples/`](examples/) directory contains sample grammars and a Jupyter notebook.
Start with [`examples/README.md`](examples/README.md).

## CUE schemas

Grammar YAML files can be checked manually with the [CUE](https://cuelang.org/) CLI.
See [`schemas/README.md`](schemas/README.md) for the schema layout and `cue vet` usage.

The `pfmg` library does **not** validate grammar files at import time
(`check_yaml_files_with_cue` in `pfmg/lexique/main/actions.py` is commented out).

To install the CUE CLI manually, download a release binary from
<https://github.com/cue-lang/cue/releases> and place it on your `PATH`.

## Roadmap / planned features

Features described in older design notes but **not implemented** in the current code:

- `contractions` token splitting in `MorphoSyntax.yaml` (pre-parse French tokenization)
- `defaut` field (automatic determiner injection)
- Kalaba → French reverse translation pipeline
- Runtime CUE validation on grammar load
- CUE schema for `Phonology.yaml`
- Loading extended `Phonology.yaml` fields (`translations`, `gabarits`, `nom_classe`, …)
- Aligning `morphosyntax.cue` with the runtime YAML format (`phrases`, `agreements`, …)

## Development

```bash
make install   # uv sync --all-groups
make check     # lint + format-check + type + test
```

See [`AGENTS.md`](AGENTS.md) for contributor and AI-agent guidelines.

The Kalaba grammar book (French and English) is built with Antora under [`doc/`](doc/).
Run `make docs` (Docker) after `docker compose build`.

## License

BSD — see [`LICENSE`](LICENSE).
