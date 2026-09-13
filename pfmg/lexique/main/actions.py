"""CLI actions for the lexique package main."""

import argparse
import os
import shutil
from pathlib import Path

import cue

from pfmg.utils.abstract_factory import factory_function
from pfmg.utils.paths import get_validation_file_path


def action(
    namespace: argparse.Namespace,
) -> None:
    """Dispatch to the requested action (namespace.name and args).

    Args:
        namespace: Result of ArgumentParser.parse_args() (must have "name").

    """
    factory_function(
        concrete_product=f"{namespace.name}_action",
        package=__name__,
        namespace=namespace,
    )


def check_if_datapath_exists(
    namespace: argparse.Namespace,
) -> None:
    """Validate that the grammar config directory exists.

    Args:
        namespace: Must have "datapath" attribute (path to config directory).

    """
    path = Path(namespace.datapath)
    if not (path.exists() and path.is_dir()):
        raise argparse.ArgumentTypeError(path)


def check_if_datapath_contains_all_files(
    namespace: argparse.Namespace,
) -> None:
    """Check that all required config files are present in the directory.

    Required files: Gloses.yaml, Blocks.yaml, Stems.yaml, Phonology.yaml,
    MorphoSyntax.yaml.

    Args:
        namespace: Must have "datapath" attribute pointing to the config directory.

    """
    message = f"{namespace.datapath} does not contain Gloses.yaml"
    if not (namespace.datapath / "Gloses.yaml").exists():
        raise argparse.ArgumentTypeError(message)

    message = f"{namespace.datapath} does not contain Blocks.yaml"
    if not (namespace.datapath / "Blocks.yaml").exists():
        raise argparse.ArgumentTypeError(message)

    message = f"{namespace.datapath} does not contain Stems.yaml"
    if not (namespace.datapath / "Stems.yaml").exists():
        raise argparse.ArgumentTypeError(message)

    message = f"{namespace.datapath} does not contain Phonology.yaml"
    if not (namespace.datapath / "Phonology.yaml").exists():
        raise argparse.ArgumentTypeError(message)

    message = f"{namespace.datapath} does not contain MorphoSyntax.yaml"
    if not (namespace.datapath / "MorphoSyntax.yaml").exists():
        raise argparse.ArgumentTypeError(message)


def check_yaml_files_with_cue(namespace: argparse.Namespace) -> None:
    """Validate the grammar YAML files against their CUE schemas.

    Each YAML file in the config directory is vetted against the matching
    schema under ``schemas/schemas`` with the ``cue`` CLI (through ``pycue``).
    Validation is skipped when the ``cue`` binary is not installed so the
    library stays usable without it.

    Args:
        namespace: Must have "datapath" (path to the config directory).

    Raises:
        argparse.ArgumentTypeError: When a YAML file does not satisfy its schema.

    """
    if shutil.which(cue.cue_exe) is None:
        return

    datapath = Path(namespace.datapath).resolve()
    schema_by_file = {
        "Gloses.yaml": "gloses.cue",
        "Blocks.yaml": "blocks.cue",
        "Stems.yaml": "stems.cue",
        "MorphoSyntax.yaml": "morphosyntax.cue",
        "Phonology.yaml": "phonology.cue",
    }

    previous = Path.cwd()
    os.chdir(get_validation_file_path())
    try:
        for yaml_name, schema_name in schema_by_file.items():
            schema = Path("schemas") / schema_name
            data = datapath / yaml_name
            try:
                cue.vet.files(str(schema), str(data))
            except cue.Error as error:
                message = f"{data} does not satisfy {schema_name}:\n{error}"
                raise argparse.ArgumentTypeError(message) from error
    finally:
        os.chdir(previous)


def lexicon_action(
    namespace: argparse.Namespace,
) -> None:
    """Run lexicon action: realization, lexical rules, and Polars DataFrame output.

    Args:
        namespace: Must have "datapath" (path to lexicon config directory).

    """
    from pfmg.lexique.lexicon import Lexicon

    path = Path(namespace.datapath)
    # vérifier que l'archive namespace.datapath existe
    # et que seuls les fichiers suivants sont présents
    # - Gloses.yaml
    # - Blocks.yaml
    # - Stems.yaml
    # - Phonology.yaml
    check_if_datapath_exists(namespace)
    check_if_datapath_contains_all_files(namespace)
    check_yaml_files_with_cue(namespace)

    Lexicon.from_yaml(path)
