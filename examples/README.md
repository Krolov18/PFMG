# Examples

This directory contains sample Kalaba grammars and a notebook demonstrating parsing
with morphological and syntactic ambiguity.

## Prerequisites

Install project dependencies from the repository root:

```bash
uv sync --all-groups
```

Run commands from this directory (`examples/`) so that relative paths such as `./data`
resolve correctly.

## Grammar directories

Each subdirectory (`data/`, `data2/`) is a complete grammar: the five required YAML
files (`Gloses.yaml`, `Blocks.yaml`, `Stems.yaml`, `Phonology.yaml`,
`MorphoSyntax.yaml`).

| Directory | Purpose |
|-----------|---------|
| `data/` | Simpler grammar used by the notebook; basic noun-phrase translation (`"des garçons"` → Kalaba forms). |
| `data2/` | Extended variant with additional morphosyntax rules (e.g. optional numeral `'deux'`, richer agreement on destination phrases). Differs in `Blocks.yaml`, `Stems.yaml`, and `MorphoSyntax.yaml`. |

`Gloses.yaml` and `Phonology.yaml` are identical between the two directories.

## Jupyter notebook

[`execution_grammaire.ipynb`](execution_grammaire.ipynb) demonstrates parsing French
input with morphological and syntactic ambiguity. It calls `parsing_action` with the
`data/` grammar:

```python
from pfmg.parsing.main.actions import parsing_action

parsing_action(
    {
        "data": "des garçons",
        "path": "./data",
        "keep": "all",
    }
)
```

Launch Jupyter from this directory:

```bash
cd examples
uv run jupyter notebook execution_grammaire.ipynb
```

(`jupyter` is not a project dependency; install it in your environment if needed.)

## CLI equivalents

From the repository root:

```bash
# Parse with the default grammar (data/)
uv run python -m pfmg.parsing.main parsing examples/data "des garçons" -k all

# List lexical forms from the grammar
uv run python -m pfmg.lexique.main.main lexicon examples/data
```

Swap `examples/data` for `examples/data2` to use the extended grammar.
