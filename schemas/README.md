# CUE schemas

Grammar YAML files are described by CUE schemas in this directory. The module path is
`pfmg.com/pkg` (see [`cue.mod/module.cue`](cue.mod/module.cue)).

## Schema files

| CUE file | YAML file | Description |
|----------|-----------|-------------|
| [`schemas/gloses.cue`](schemas/gloses.cue) | `Gloses.yaml` | Source and destination attribute–value glosses per category |
| [`schemas/blocks.cue`](schemas/blocks.cue) | `Blocks.yaml` | Morphological realization blocks (prefix, suffix, template, …) |
| [`schemas/stems.cue`](schemas/stems.cue) | `Stems.yaml` | Stem inventory and recursive inheritance |
| [`schemas/morphosyntax.cue`](schemas/morphosyntax.cue) | `MorphoSyntax.yaml` | Syntactic rules, agreements, percolations, translations |
| [`schemas/literals.cue`](schemas/literals.cue) | — | Shared character-class patterns used by other schemas |

There is no dedicated CUE schema for `Phonology.yaml` yet.

## Schema vs runtime YAML

The CUE schemas do not fully match the YAML format loaded by `pfmg` today:

* **`morphosyntax.cue`** — uses legacy PascalCase keys (`Syntagmes`, `Accords`, …);
  the runtime format in `examples/data/MorphoSyntax.yaml` uses `Start`, `Source` /
  `Destination`, `phrases`, `agreements`, `percolations`, `translations`.
* **`stems.cue`** — flat inheritance map; real `Stems.yaml` files are deeply nested.
* **`blocks.cue`** — rule patterns only; does not model the `source` / `destination`
  list wrapper.

Aligning CUE with the runtime format is on the [README roadmap](../README.md#roadmap--planned-features).
The Antora book under [`doc/`](../doc/) documents the **runtime** format.

[`data.cue`](data.cue) is a small CUE fixture used for schema development.

## Validating YAML with `cue vet`

Install the [CUE CLI](https://cuelang.org/docs/install/) (see the root [`README.md`](../README.md)).

From the repository root, export a grammar directory as JSON and validate against a
schema (example for `MorphoSyntax.yaml`):

```bash
cd schemas
cue export ../examples/data/MorphoSyntax.yaml | cue vet schemas/morphosyntax.cue -
```

Repeat with the matching schema for each YAML file (`gloses.cue`, `blocks.cue`,
`stems.cue`, `morphosyntax.cue`).

## Runtime validation

Runtime CUE validation is **not enabled** in the library. The hook
`check_yaml_files_with_cue` in [`pfmg/lexique/main/actions.py`](../pfmg/lexique/main/actions.py)
is present but commented out. Schema paths are resolved via
[`pfmg/utils/paths.py`](../pfmg/utils/paths.py) (`get_validation_file_path()` →
`schemas/`).

The `pycue` package is a runtime dependency for future validation support.
