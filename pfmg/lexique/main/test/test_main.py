"""Tests for the lexique CLI entry point."""

import argparse
import pathlib
from contextlib import redirect_stdout
from io import StringIO

import pytest

from pfmg.lexique.main.main import build_parser, main
from pfmg.utils.paths import get_project_path


def get_example_grammar() -> pathlib.Path:
    return get_project_path() / "examples" / "data"


def test_build_parser_defaults() -> None:
    namespace = build_parser().parse_args(["lexicon", "some/path"])
    assert namespace.name == "lexicon"
    assert namespace.datapath == pathlib.Path("some/path")
    assert namespace.list == "to_string"


def test_build_parser_list_option() -> None:
    namespace = build_parser().parse_args(
        ["lexicon", "some/path", "-l", "to_lexical"]
    )
    assert namespace.list == "to_lexical"


def test_build_parser_rejects_unknown_list_option() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(["lexicon", "some/path", "-l", "unknown"])


def test_main_loads_the_lexicon_without_stdout() -> None:
    """Lexicon subcommand validates config and loads without printing grammar."""
    buffer = StringIO()
    with redirect_stdout(buffer):
        main(["lexicon", str(get_example_grammar())])

    assert buffer.getvalue() == ""


def test_main_rejects_an_unknown_datapath(tmp_path) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        main(["lexicon", str(tmp_path / "missing_grammar")])
