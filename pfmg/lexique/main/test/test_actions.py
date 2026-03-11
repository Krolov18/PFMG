import argparse
from argparse import Namespace
from pathlib import Path

import pytest

from pfmg.lexique.main.actions import action


def test_unknown_path_to_grammar(tmp_path) -> None:
    datapath = tmp_path / "unknown_grammar"
    namespace = Namespace(name="lexicon", datapath=datapath)
    with pytest.raises(argparse.ArgumentTypeError):
        action(namespace=namespace)


def test_no_gloses_grammar(tmp_path) -> None:
    datapath = tmp_path / "no_gloses_grammar"
    datapath.mkdir()
    blocks = datapath / "Blocks.yaml"
    blocks.write_text("")
    stems = datapath / "Stems.yaml"
    stems.write_text("")
    phonology = datapath / "Phonology.yaml"
    phonology.write_text("")
    morpho = datapath / "Morphosyntax.yaml"
    morpho.write_text("")
    namespace = Namespace(name="lexicon", datapath=datapath)
    with pytest.raises(argparse.ArgumentTypeError,
                       match=".*does not contain Gloses.*"):
        action(namespace=namespace)


def test_no_blocks_grammar(tmp_path) -> None:
    datapath = tmp_path / "no_blocks_grammar"
    datapath.mkdir()
    gloses = datapath / "Gloses.yaml"
    gloses.write_text("")
    stems = datapath / "Stems.yaml"
    stems.write_text("")
    phonology = datapath / "Phonology.yaml"
    phonology.write_text("")
    morpho = datapath / "Morphosyntax.yaml"
    morpho.write_text("")
    namespace = Namespace(name="lexicon", datapath=datapath)
    with pytest.raises(argparse.ArgumentTypeError,
                       match=".*does not contain Blocks.*"):
        action(namespace=namespace)


def test_no_phonology_grammar(tmp_path) -> None:
    datapath = tmp_path / "no_phonology_grammar"
    datapath.mkdir()
    blocks = datapath / "Blocks.yaml"
    blocks.write_text("")
    gloses = datapath / "Gloses.yaml"
    gloses.write_text("")
    stems = datapath / "Stems.yaml"
    stems.write_text("")
    phonology = datapath / "Morphosyntax.yaml"
    phonology.write_text("")
    namespace = Namespace(name="lexicon", datapath=datapath)
    with pytest.raises(argparse.ArgumentTypeError,
                       match=".*does not contain Phonology.*"):
        action(namespace=namespace)


def test_no_stems_grammar(tmp_path) -> None:
    datapath = tmp_path / "no_stems_grammar"
    datapath.mkdir()
    blocks = datapath / "Blocks.yaml"
    blocks.write_text("")
    gloses = datapath / "Gloses.yaml"
    gloses.write_text("")
    phonology = datapath / "Phonology.yaml"
    phonology.write_text("")
    morpho = datapath / "Morphosyntax.yaml"
    morpho.write_text("")
    namespace = Namespace(name="lexicon", datapath=datapath)
    with pytest.raises(argparse.ArgumentTypeError,
                       match=".*does not contain Stems.*"):
        action(namespace=namespace)


def test_no_morphosyntax_grammar(tmp_path) -> None:
    datapath = tmp_path / "no_morphosyntax_grammar"
    datapath.mkdir()
    blocks = datapath / "Blocks.yaml"
    blocks.write_text("")
    gloses = datapath / "Gloses.yaml"
    gloses.write_text("")
    stems = datapath / "Stems.yaml"
    stems.write_text("")
    phonology = datapath / "Phonology.yaml"
    phonology.write_text("")
    namespace = Namespace(name="lexicon", datapath=datapath)
    with pytest.raises(argparse.ArgumentTypeError,
                       match=".*does not contain MorphoSyntax.*"):
        action(namespace=namespace)


def test_validate_gloses(tmp_path):
    datapath = tmp_path / "no_morphosyntax_grammar"
    datapath.mkdir()
    blocks = datapath / "Blocks.yaml"
    blocks.write_text("")
    gloses = datapath / "Gloses.yaml"
    gloses.write_text("")
    stems = datapath / "Stems.yaml"
    stems.write_text("")
    phonology = datapath / "Phonology.yaml"
    phonology.write_text("")
    # morpho = datapath / "MorphoSyntax.yaml"
    # morpho.write_text("")
    namespace = Namespace(name="lexicon", datapath=datapath)
    with pytest.raises(argparse.ArgumentTypeError,
                       match=".*does not contain MorphoSyntax.*"):
        action(namespace=namespace)


def get_data_test_grammar() -> Path:
    return Path(__file__).parent / "data2_for_test"


def test_actions_not_valid_files():
    action(
        namespace=Namespace(
            name="lexicon",
            datapath=get_data_test_grammar() / "grammar"
        )
    )
