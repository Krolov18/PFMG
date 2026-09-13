# PFMG

**PFMG** (package name `pfmg`) is a Python library for morphological and grammatical
processing. It provides lexicon management (paradigm-based realization), FCFG parsing
with NLTK, and French-to-invented-language translation (Kalaba and similar grammars).

Grammars are defined as YAML configuration files described by CUE schemas in
[`schemas/`](schemas/). The `lexicon` CLI validates them at runtime when the CUE
CLI is available (see [CUE schemas](#cue-schemas)). See the [`doc/`](doc/) Antora
book for the runtime format used by `examples/data/`.

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

# examples/data3 handles full sentences
uv run python -m pfmg.parsing.main parsing examples/data3 "la maman donne une banane à la fille"
```

Use `-k all` to keep all parse results instead of only the first:

```bash
uv run python -m pfmg.parsing.main parsing examples/data "des petites autruches" -k all
```

## Examples

The [`examples/`](examples/) directory contains sample grammars and a Jupyter notebook.
Start with [`examples/README.md`](examples/README.md).

## CUE schemas

Grammar YAML files are described by CUE schemas in [`schemas/`](schemas/).
See [`schemas/README.md`](schemas/README.md) for the schema layout.

**Manual check** with the [CUE](https://cuelang.org/) CLI:

```bash
cd schemas
cue vet schemas/morphosyntax.cue ../examples/data/MorphoSyntax.yaml
```

**Runtime validation**: the `lexicon` command runs `check_yaml_files_with_cue` in
[`pfmg/lexique/main/actions.py`](pfmg/lexique/main/actions.py) when the `cue` binary
is on `PATH` (via `pycue`). Without `cue`, validation is skipped and the command
still runs. Set `CUE_EXE` to point at a specific `cue` binary.

Install the CUE CLI from <https://github.com/cue-lang/cue/releases> or
`nix run nixpkgs#cue`.

## Roadmap / planned features

Features described in older design notes but **not implemented** in the current code:

- `contractions` token splitting in `MorphoSyntax.yaml` (pre-parse French tokenization)
- `defaut` field (automatic determiner injection)
- Kalaba → French reverse translation pipeline
- Loading extended `Phonology.yaml` fields (`translations`, `gabarits`, `nom_classe`, …)

## Development

```bash
make install       # uv sync --all-groups
make check         # lint + format-check + type + test
make docker-test   # pytest inside the Python Docker image
make docker-check  # lint + format-check + type + test inside Docker
```

See [`AGENTS.md`](AGENTS.md) for contributor and AI-agent guidelines.

The Kalaba grammar book (French and English) is built with Antora under [`doc/`](doc/).
Run `make docs` (Docker) after `docker compose build`.

## License

BSD — see [`LICENSE`](LICENSE).
