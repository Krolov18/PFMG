import argparse
from pathlib import Path

from lexique_2.lexical_structures.Paradigm import Paradigm
from lexique_2.lexical_structures.Stems import Stems
from utils.abstract_factory import factory_function


def action(namespace: argparse.Namespace) -> None:
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


def lexicon_action(namespace: argparse.Namespace) -> None:
    path = Path(namespace.datapath)
    paradigm = Paradigm.from_disk(path)
    stems = Stems.from_disk(path / "Stems.yaml")

    for lexeme in stems:
        for forme in paradigm.realize(lexeme):
            print(forme.to_unary())
