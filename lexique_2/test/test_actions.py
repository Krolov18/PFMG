import argparse
import os
from argparse import Namespace
from pathlib import Path

import cue  # type: ignore
import pytest

from lexique_2.actions import action
from utils.paths import get_project_path


def get_data_test_grammar() -> Path:
    return Path(__file__).parent / "test" / "data_for_test"


@pytest.mark.parametrize("namespace", [
    Namespace(name="lexicon", datapath=get_data_test_grammar() / "empty_grammar"),
    Namespace(name="lexicon", datapath=get_data_test_grammar() / "no_blocks_grammar"),
    Namespace(name="lexicon", datapath=get_data_test_grammar() / "no_glosses_grammar"),
    Namespace(name="lexicon", datapath=get_data_test_grammar() / "no_phonology_grammar"),
    Namespace(name="lexicon", datapath=get_data_test_grammar() / "no_stems_grammar"),
])
def test_actions(namespace):
    with pytest.raises(argparse.ArgumentTypeError):
        action(namespace=namespace)


@pytest.mark.skip
def test_actions_not_valid_files():
    # with pytest.raises(cue.Error):
    action(namespace=Namespace(
        name="lexicon",
        datapath=get_data_test_grammar() / "gloses_grammar")
    )
