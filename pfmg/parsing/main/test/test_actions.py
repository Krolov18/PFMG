"""Tests for parsing.main.actions."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from pfmg.parsing.main.actions import action, parsing_action


def test_action_pops_name_and_calls_factory() -> None:
    with patch("pfmg.parsing.main.actions.factory_function") as mock_factory:
        namespace = {"name": "parsing", "path": "/fake", "data": ["x"], "keep": "first"}
        # parsing_action will be invoked by factory_function; we only check action() flow
        mock_factory.return_value = None
        action(namespace=namespace)
        assert "name" not in namespace
        mock_factory.assert_called_once()
        call_kw = mock_factory.call_args[1]
        assert call_kw["concrete_product"] == "parsing_action"
        assert call_kw["package"] == "pfmg.parsing.main.actions"


def test_parsing_action_stdout(tmp_path: pytest.TempPathFactory) -> None:
    mock_parser = MagicMock()
    mock_parser.parse.return_value = "result1"

    with patch("pfmg.parsing.main.actions.KParser") as MockKParser:
        MockKParser.from_yaml.return_value = mock_parser
        namespace = {"path": tmp_path, "data": ["sentence"], "keep": "first"}

        capture = []
        original_write = sys.stdout.write

        def capture_write(s: str) -> None:
            capture.append(s)
            original_write(s)

        sys.stdout.write = capture_write
        try:
            parsing_action(namespace=namespace)
        finally:
            sys.stdout.write = original_write

        MockKParser.from_yaml.assert_called_once_with(tmp_path)
        mock_parser.parse.assert_called_once_with(data=["sentence"], keep="first")
        assert "result1" in "".join(capture)


def test_parsing_action_stdout_list_result(tmp_path: pytest.TempPathFactory) -> None:
    mock_parser = MagicMock()
    mock_parser.parse.return_value = ["a", "b"]

    with patch("pfmg.parsing.main.actions.KParser") as MockKParser:
        MockKParser.from_yaml.return_value = mock_parser
        namespace = {"path": tmp_path, "data": ["x"], "keep": "all"}

        capture = []
        original_write = sys.stdout.write

        def capture_write(s: str) -> None:
            capture.append(s)
            original_write(s)

        sys.stdout.write = capture_write
        try:
            parsing_action(namespace=namespace)
        finally:
            sys.stdout.write = original_write

        out = "".join(capture)
        assert "a" in out and "b" in out
