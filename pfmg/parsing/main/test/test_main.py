"""Tests for the parsing CLI entry point."""

import pathlib
import subprocess
import sys
from unittest.mock import patch

import pytest

from pfmg.parsing.main import build_parser, main
from pfmg.utils.paths import get_project_path


def test_build_parser_defaults() -> None:
    namespace = build_parser().parse_args(["parsing", "some/path", "des garçons"])
    assert namespace.name == "parsing"
    assert namespace.path == pathlib.Path("some/path")
    assert namespace.data == ["des garçons"]
    assert namespace.keep == "first"


def test_build_parser_keep_all() -> None:
    namespace = build_parser().parse_args(
        ["parsing", "some/path", "des garçons", "-k", "all"]
    )
    assert namespace.keep == "all"


def test_build_parser_rejects_unknown_keep() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(["parsing", "some/path", "x", "-k", "unknown"])


def test_build_parser_lexical_grammar_subcommand() -> None:
    namespace = build_parser().parse_args(
        ["lexical_grammar", "examples/data"]
    )
    assert namespace.name == "lexical_grammar"
    assert namespace.datapath == pathlib.Path("examples/data")


def test_main_dispatches_the_namespace_as_a_dict() -> None:
    with patch("pfmg.parsing.main.action") as mock_action:
        main(["parsing", "some/path", "des garçons", "-k", "all"])

    mock_action.assert_called_once_with(
        namespace={
            "name": "parsing",
            "path": pathlib.Path("some/path"),
            "data": ["des garçons"],
            "keep": "all",
        }
    )


def test_package_is_executable_with_dash_m() -> None:
    # regression: the CLI used to live in __init__.py, where the
    # `if __name__ == "__main__"` guard can never fire
    result = subprocess.run(
        [sys.executable, "-m", "pfmg.parsing.main", "--help"],
        capture_output=True,
        text=True,
        cwd=get_project_path(),
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "parsing" in result.stdout
