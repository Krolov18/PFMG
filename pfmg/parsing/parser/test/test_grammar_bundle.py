"""Tests for GrammarBundle (YAML directory loader)."""

from pfmg.parsing.grammar_bundle import GrammarBundle
from pfmg.parsing.parser import KParser
from pfmg.utils.paths import get_project_path


def test_grammar_bundle_loads_examples_data() -> None:
    path = get_project_path() / "examples" / "data"
    bundle = GrammarBundle.from_directory(path)

    assert bundle.path == path
    assert bundle.lexicon.lexemes
    assert bundle.grammar.translator.productions
    assert bundle.grammar.validator.productions


def test_grammar_bundle_from_bundle_matches_from_yaml() -> None:
    path = get_project_path() / "examples" / "data"
    bundle = GrammarBundle.from_directory(path)
    from_bundle = KParser.from_bundle(bundle)
    from_yaml = KParser.from_yaml(path)

    assert isinstance(from_bundle, KParser)
    assert isinstance(from_yaml, KParser)
    assert (
        from_bundle.translator.grammar.productions
        == from_yaml.translator.grammar.productions
    )
    assert len(bundle.lexicon.lexemes) == len(from_yaml.translator.lexique.lexemes)
