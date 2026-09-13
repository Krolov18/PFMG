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
| [`schemas/phonology.cue`](schemas/phonology.cue) | `Phonology.yaml` | Consonants, vowels, apophonies, derives and mutations |
| [`schemas/literals.cue`](schemas/literals.cue) | — | Shared character-class patterns used by other schemas |

## Schema vs runtime YAML

The schemas track the runtime YAML format loaded by `pfmg`, as illustrated by the
grammars under [`examples/data`](../examples/data) and documented in the Antora book
under [`doc/`](../doc/):

* **`gloses.cue`** — per category, a `source` / `destination` attribute inventory and
  an optional `alignments` table.
* **`morphosyntax.cue`** — a `Start` symbol plus one rule per category, each with a
  `Source` (`phrases`, `agreements`, `percolations`, `translations`) and a
  `Destination` (same, without `translations`).
* **`blocks.cue`** — per category, ordered `source` / `destination` realization blocks.
* **`stems.cue`** — the recursively nested stem inheritance tree.
* **`phonology.cue`** — the fields read by the runtime loader, kept open for the
  extended phonology fields (`translations`, `gabarits`, `nom_classe`, `syllabes`, …).

The legacy flat/PascalCase grammars under `pfmg/data/kalaba` predate this format and
are not covered by these schemas.

[`data.cue`](data.cue) is a small CUE fixture used for schema development.

## Validating YAML with `cue vet`

Install the [CUE CLI](https://cuelang.org/docs/install/) (see the root [`README.md`](../README.md)).

From this directory, vet a grammar file against its schema (example for
`MorphoSyntax.yaml`):

```bash
cd schemas
cue vet schemas/morphosyntax.cue ../examples/data/MorphoSyntax.yaml
```

Repeat with the matching schema for each YAML file (`gloses.cue`, `blocks.cue`,
`stems.cue`, `morphosyntax.cue`, `phonology.cue`).

## Runtime validation

Runtime CUE validation is **enabled** through `check_yaml_files_with_cue` in
[`pfmg/lexique/main/actions.py`](../pfmg/lexique/main/actions.py): the `lexicon`
command vets every grammar YAML file against its schema (via the `pycue` runtime
dependency). Schema paths are resolved with
[`pfmg/utils/paths.py`](../pfmg/utils/paths.py) (`get_validation_file_path()` →
`schemas/`). Validation is skipped when the `cue` binary is not on `PATH`, so the
library stays usable without it; set `CUE_EXE` to point at a specific `cue` binary.
