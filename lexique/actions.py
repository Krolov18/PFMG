import argparse
import os.path
from pathlib import Path
from cue import vet

from lexique.lexical_structures.Paradigm import Paradigm
from lexique.lexical_structures.Stems import Stems
from utils.abstract_factory import factory_function
from utils.paths import get_validation_file_path


def action(
        namespace: argparse.Namespace
) -> None:
    """
    Factory permettant de construire les actions du "main".

    Plutôt que de créer des sous-classes de "argparse.Namespace"
    On choisit d'utiliser le champ

    :param namespace : namespace généré par ArgumentParser.parse_args()
    :return:
    """
    factory_function(
        concrete_product=f"{namespace.name}_action",
        package=__name__,
        namespace=namespace
    )


def check_if_datapath_exists(
        namespace: argparse.Namespace
) -> None:
    path = Path(namespace.datapath)
    if not (path.exists() and path.is_dir()):
        raise argparse.ArgumentTypeError(
            f"{namespace.datapath} is not a valid path"
        )


def check_if_datapath_contains_all_files(
        namespace: argparse.Namespace
) -> None:
    """
    Vérifie que le dossier contient bien les fichiers suivants :
    - Gloses.yaml
    - Blocks.yaml
    - Stems.yaml
    - Phonology.yaml
    :param namespace: namespace généré par ArgumentParser.parse_args()
    :return: True si le dossier contient bien les fichiers
             Sinon il lève une exception
    """
    if not (namespace.datapath / "Gloses.yaml").exists():
        raise argparse.ArgumentTypeError(
            f"{namespace.datapath} does not contain Gloses.yaml"
        )
    if not (namespace.datapath / "Blocks.yaml").exists():
        raise argparse.ArgumentTypeError(
            f"{namespace.datapath} does not contain Blocks.yaml"
        )
    if not (namespace.datapath / "Stems.yaml").exists():
        raise argparse.ArgumentTypeError(
            f"{namespace.datapath} does not contain Stems.yaml"
        )
    if not (namespace.datapath / "Phonology.yaml").exists():
        raise argparse.ArgumentTypeError(
            f"{namespace.datapath} does not contain Phonology.yaml"
        )


def check_yaml_files_with_cue(namespace: argparse.Namespace) -> None:
    """
    Comme "schemas" est un package cue, 
    il faut placer le cwd dans le package,
    puis le remettre là où il était en sortant.
    :param namespace: chemin de l'archive des fichiers yaml
    """
    path = os.getcwd()
    os.chdir(get_validation_file_path())
    vet.files(os.path.join(
        "schemas", "gloses.cue"), namespace.datapath / "Gloses.yaml"
    )
    vet.files(os.path.join(
        "schemas", "blocks.cue"), namespace.datapath / "Blocks.yaml"
    )
    vet.files(os.path.join(
        "schemas", "stems.cue"), namespace.datapath / "Stems.yaml"
    )
    # vet.files(
    #     os.path.join("schemas", "phonology.cue"),
    #     namespace.datapath / "Phonology.yaml"
    # )
    os.chdir(path)


def lexicon_action(
        namespace: argparse.Namespace
) -> None:
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

    paradigm = Paradigm.from_disk(path)

    for lexeme in Stems.from_disk(path / "Stems.yaml"):
        for forme in paradigm.realize(lexeme):
            print(forme.to_unary())
