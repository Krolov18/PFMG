# Kalaba documentation (Antora)

Bilingual AsciiDoc book (French + English) for the Kalaba grammar YAML format, built
with [Antora](https://antora.org/).

User guides in Markdown also live at the repository root ([`README.md`](../README.md)),
[`examples/`](../examples/), and [`schemas/`](../schemas/).

## Design notes (outside the book)

The Kalaba rewrite prioritized **YAML input files** as the user entry point so that
grammar authors rarely need to change Python code. The codebase moved from an initial
OO style toward dataclasses and functional realization (`realise`), then toward
declarative configuration (`Gloses`, `Blocks`, `Stems`, `MorphoSyntax`, `Phonology`).
CUE schemas now describe those files.

Full background notes:

- [`notes/design-reflexions.md`](notes/design-reflexions.md) — rewrite rationale (from legacy AsciiDoc)
- [`notes/architecture-draft.md`](notes/architecture-draft.md) — architecture draft (from legacy LaTeX)

## Structure

Playbook: [`antora-playbook.yml`](../antora-playbook.yml) at the repository root.

```
antora-playbook.yml               # Antora entry point
doc/
├── kalaba/                         # Antora component
│   ├── antora.yml
│   └── modules/
│       └── ROOT/                   # Pages (fr/, en/), partials, examples
└── build/site/                     # Generated site (gitignored)
```

French and English pages live under `kalaba/modules/ROOT/pages/fr/` and
`.../pages/en/`. Shared partials and YAML examples are in the same `ROOT` module;
pages include them via `include::partial$morphosyntax/...[]`.

## Build

Documentation is built with [Antora](https://antora.org/) inside Docker (no local Node
install required). First-time setup:

```bash
docker compose build docs
```

Build the site:

```bash
make docs
# or
docker compose run --rm docs
```

Output: `doc/build/site/`. Preview locally:

```bash
make docs-preview
# or
docker compose run --rm --service-ports docs-preview
```

Then open <http://localhost:8787>.

To build without Docker (optional):

```bash
npm install
npm run docs:build
```

## Future options

- PDF export via `@antora/pdf-extension`
- CI publish to GitHub Pages
- Lunr search via `@antora/lunr-extension`

## See also

- [`../README.md`](../README.md) — project overview and CLI
- [`../examples/README.md`](../examples/README.md) — runnable examples
- [`../schemas/README.md`](../schemas/README.md) — CUE schemas
- [`../AGENTS.md`](../AGENTS.md) — contributor guidelines
