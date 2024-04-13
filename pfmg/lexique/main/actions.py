"""Actions du main du package lexique."""
import argparse
import os.path
from pathlib import Path

from pfmg.utils.abstract_factory import factory_function
from pfmg.utils.paths import get_validation_file_path


def action(
    namespace: argparse.Namespace,
) -> None:
    """Factory qui lance n'importe quelle action disponible.

    :param namespace: namespace généré par ArgumentParser.parse_args()
    """
    factory_function(
        concrete_product=f"{namespace.name}_action",
        package=__name__,
        namespace=namespace,
    )


def check_if_datapath_exists(
    namespace: argparse.Namespace,
) -> None:
    """Valide l'existence du répertoire de configuration de la grammaire.

    :param namespace: namespace généré par ArgumentParser.parse_args()
    """
    path = Path(namespace.datapath)
    if not (path.exists() and path.is_dir()):
        raise argparse.ArgumentTypeError(path)


def check_if_datapath_contains_all_files(
    namespace: argparse.Namespace,
) -> None:
    """Vérifie si tous les fichiers de config sont présents dans le répertoire.

    Fichiers attendus dans l'archive:
        - Gloses.yaml
        - Blocks.yaml
        - Stems.yaml
        - Phonology.yaml
        - MorphoSyntax.yaml
    :param namespace: namespace généré par ArgumentParser.parse_args()
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
    """Valide les fichiers YAML avec avec CUE.
    
    On change temporairement le cwd, le temps de la validation.
    :param namespace: namespace généré par ArgumentParser.parse_args()
    """
    path = os.getcwd()
    os.chdir(get_validation_file_path())
    # print(os.getcwd())
    # vet.files(
    #     os.path.join("../../../projects/schemas", "gloses.cue"),
    #     namespace.datapath / "Gloses.yaml",
    # )
    # vet.files(
    #     os.path.join("../../../projects/schemas", "blocks.cue"),
    #     namespace.datapath / "Blocks.yaml",
    # )
    # vet.files(
    #     os.path.join("../../../projects/schemas", "stems.cue"),
    #     namespace.datapath / "Stems.yaml",
    # )
    # print("toto")
    # vet.files(
    #     os.path.join("../../../projects/schemas", "morphosyntax.cue"),
    #     namespace.datapath / "MorphoSyntax.yaml",
    # )
    # vet.files(
    #     os.path.join("schemas", "phonology.cue"),
    #     namespace.datapath / "Phonology.yaml"
    # )
    os.chdir(path)


def lexicon_action(
    namespace: argparse.Namespace,
) -> None:
    """Action qui gère le lexique.

    réalisation
    règles lexicales
    DataFrame contenant toutes les infos

    :param namespace: namespace généré par ArgumentParser.parse_args()
    """
    from pfmg.lexique.paradigm.Paradigm import Paradigm
    from pfmg.lexique.stems.Stems import Stems

    # print(namespace)
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
            forme.to_string()
    # getattr(forme, namespace.list)
