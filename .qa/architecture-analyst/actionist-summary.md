# Actionist summary

## Input

- analyst_skill: architecture-analyst
- analyst_status: complete
- report_reference: `.qa/architecture-analyst/report.md`

## Guiding outcome

Applied four targeted refactors from the architecture-analyst report: document `external` role, unify parsing CLI on `argparse.Namespace`, fix parsing→lexique boundary leak in tests, enforce boundary rules on test code. Deferred F1 (morpheme core/presentation split) and `external` rename.

## Changes

| Finding ID | File(s) | Change summary |
|------------|---------|----------------|
| F2 | `pfmg/external/__init__.py` | Added package docstring: behavioral ports, not third-party integrations |
| F3 | `pfmg/lexique/forme/builders.py`, `pfmg/parsing/test/test_lexical_grammar.py`, `pfmg/utils/test/test_import_boundaries.py` | `make_forme_entry()` hides morpheme construction; parsing tests no longer import `Morphemes`/`Radical`; boundary test includes test dirs |
| F5 | `pfmg/parsing/main/actions.py`, `pfmg/parsing/main/__init__.py`, `pfmg/parsing/main/test/test_actions.py`, `pfmg/parsing/main/test/test_main.py` | Parsing CLI actions take `argparse.Namespace` (aligned with lexique CLI) |

## Validation

- commands_run:
  - `uv run pytest pfmg/utils/test/test_import_boundaries.py pfmg/parsing/main/test/ pfmg/parsing/test/test_lexical_grammar.py -q`
  - `make test`
- results:
  - 26 passed (targeted)
  - 384 passed (full suite)

## Remaining gaps

- Findings not addressed: F1 (domain/presentation mixin coupling), F2 partial (`AGENTS.md` still says "Integrations")
- Deferred work:
  - Morpheme core/presentation split (`PresentableRule` → composition)
  - Rename `external` → `ports` (breaking)
  - `lexique.api` module (optional; `forme.builders` covers immediate need)
  - CUE validation extraction (no second consumer yet)
- Follow-up analysts recommended: none required before merge; re-run `architecture-analyst` after F1 if attempted
