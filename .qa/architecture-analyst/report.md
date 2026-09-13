---
skill: architecture-analyst
status: complete
target: /home/korantin/Documents/PFMG
stack: python
tools_used:
  - pytest pfmg/utils/test/test_import_boundaries.py
  - find/wc (module size survey)
  - ast import graph (test_import_boundaries.py rules)
tools_missing: []
severity_max: medium
generated_at: 2026-09-10T21:30:00+02:00
---

# Architecture analyst report

## Guiding question

Are there responsibility, coupling, or architectural testability issues?

## Executive summary

PFMG has **clear package layering** with **enforced import boundaries** (`pfmg/utils/test/test_import_boundaries.py`). Modules are small; no god classes. Main tension: **`lexique` domain types inherit presentation behavior from `external`** (display, glose, decoupe, YAML reader ABCs). Works today, but inverts strict clean-architecture separation and makes pure-domain unit tests harder.

Secondary issues: **`external` name misleading** (partially documented since this report), parsing boundary was leaky in tests (addressed by actionist). Overall posture: **healthy** — import-boundary tests are strong guardrails; optional refactor = decouple lexique domain from presentation mixins.

## Layer map

```
┌─────────────────────────────────────────────────────────┐
│  CLI / entry points                                     │
│  lexique/main/, parsing/main/                           │
└────────────┬───────────────────────────────┬────────────┘
             │                               │
┌────────────▼──────────┐         ┌──────────▼────────────┐
│  parsing              │         │  lexique (domain)     │
│  grammar, parser,     │──forme/ │  morpheme, paradigm,  │
│  tokenizer, backends  │ lexicon │  lexicon, phonology   │
└────────────┬──────────┘         └──────────┬────────────┘
             │                               │
             │         ┌─────────────────────┤
             │         │                     │
┌────────────▼─────────▼──┐         ┌────────▼────────────┐
│  external (ports)       │         │  utils (foundation) │
│  ABCDisplay, ABCReader, │────────▶│  StemSpace, paths,  │
│  mixins                 │         │  FeatureReader, …   │
└─────────────────────────┘         └─────────────────────┘

schemas/ (CUE) — outside Python import graph; validated in lexique CLI only
```

| Layer | Role | Allowed dependencies |
|-------|------|----------------------|
| `utils` | Shared primitives | stdlib + third-party only |
| `external` | Behavioral protocols (ports) | `utils` only |
| `lexique` | Morphology, lexicon, realization | `external`, `utils` — **not** `parsing` |
| `parsing` | Grammar, parser, tokenizer | `lexique.lexicon`, `lexique.forme`, `utils`, `external.reader` |
| `*/main` | CLI orchestration | respective package + cross-package where needed |

Boundary rules are encoded in `pfmg/utils/test/test_import_boundaries.py` and enforced in CI via pytest.

## Findings

| ID | Severity | Location | Evidence | Recommendation |
|----|----------|----------|----------|----------------|
| F1 | medium | `pfmg/lexique/forme/`, `pfmg/lexique/morpheme/`, `pfmg/lexique/sentence/` | Core types (`Forme`, `FormeEntry`, `Morphemes`, morpheme rules via `PresentableRule`) inherit `external` ABCs/mixins directly | Extract morpheme core from presentation mixins (composition over inheritance); keep public `to_string` / `to_glose` API |
| F2 | low | `pfmg/external/` | Package name suggests third-party integrations; role is behavioral ports. `AGENTS.md` still describes it as "Integrations" | Document role (done: `pfmg/external/__init__.py`); optionally rename to `ports` or update `AGENTS.md` |
| F3 | low | `pfmg/parsing/test/test_lexical_grammar.py` (was) | Parsing tests imported `Morphemes`/`Radical` — deeper than allowed prod boundary | **Resolved:** `pfmg/lexique/forme/builders.py` + boundary test covers test dirs |
| F4 | info | `pfmg/parsing/backends/`, `pfmg/parsing/parser/test/test_nltk_isolation.py` | NLTK loaded lazily via `ParseBackend`; import of `pfmg` does not touch NLTK | Keep pattern; inject backend in tests |
| F5 | low | `pfmg/parsing/main/actions.py` (was) | Parsing CLI used `dict`; lexique CLI used `argparse.Namespace` | **Resolved:** parsing CLI unified on `Namespace` |
| F6 | info | `pfmg/lexique/lexicon/Lexicon.py` | Eager realization in `__post_init__` precomputes all forms at load | Acceptable for parsing terminals; document trade-off (already in docstring) |
| F7 | info | `pfmg/` (~4k LOC prod) | Largest modules ~150 lines; domain split by concept | No consolidation needed |
| F8 | info | `pfmg/utils/stem_space.py`, `pfmg/lexique/stem_space/` | Canonical `StemSpace` in utils; lexique re-exports | Correct; keep |

## Architectural testability

| Area | Without framework? | Test doubles at boundary? | Grade |
|------|-------------------|---------------------------|-------|
| Morpheme phonology/rules | Partial — mixin bases required | No | C |
| Paradigm / Lexicon | Yes | In-memory objects | B |
| Grammar / Features | Yes | N/A | A |
| Parser | Yes — `ParseBackend` injectable | `RealizedLexicon` mock | A |
| KParser | Needs YAML or `GrammarBundle` | Constructible bundle | B |

Weakest point: morpheme/forme presentation mixins (`F1`). Strongest: parsing backend + protocol boundary (`F4`).

## Coupling hotspots

| Hotspot | From → To | Severity |
|---------|-----------|----------|
| Morpheme rule hierarchy | `lexique/morpheme/*` → `external/*` mixins | medium |
| YAML loaders | `Lexicon`, `Paradigm`, `Phonology`, `KParser` → `ABCReader` | low |
| Feature sharing | `lexique/block/Blocks`, `parsing/features/*` → `utils.features` | none |

**No circular imports.** Boundaries prevent `lexique ↔ parsing` and `external → lexique`.

## Suggested boundary moves (for actionist)

1. Clarify `external` role in docs (`AGENTS.md` alignment) — low effort
2. Composition over mixin inheritance for morphemes — medium effort, biggest testability win
3. Promote `RealizedLexicon` + minimal `forme` surface as explicit parsing API
4. ~~Unify CLI action signatures~~ — done
5. ~~Extend boundary test to test dirs~~ — done
6. Extract CUE validation to shared module only if parsing CLI gains schema checks

## Artifacts

- command: `uv run pytest pfmg/utils/test/test_import_boundaries.py -q`
- output: 4 passed (import boundary regression)
- command: `find pfmg -name '*.py' ! -path '*/test/*' -exec wc -l {} + | sort -n | tail -25`
- output: largest prod modules ~150 LOC (`KParser.py`, `Parser.py`, `abstract_factory.py`)

## Handoff

- actionist: `architectural-actionist`
- priority_findings: [F1, F2]
