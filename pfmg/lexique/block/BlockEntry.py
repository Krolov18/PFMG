# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Entry d'un Bloc. Structure de données contenant les règles d'un Bloc."""

from collections.abc import Iterator
from dataclasses import dataclass

from frozendict import frozendict

from pfmg.lexique.display.ABCDisplay import ABCDisplay
from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.selector.ABCSelector import ABCSelector
from pfmg.lexique.utils import dictify


@dataclass
class BlockEntry(ABCSelector):
    """Entry d'un Bloc. Structure de données contenant les règles d'un Bloc."""

    data: dict[str, list[list[ABCDisplay]]]

    def __post_init__(self):
        """Vérfication de base sur 'data'."""
        assert self.data
        assert all(self.data.values())
        assert all(all(x) for x in self.data.values())

    def __call__(
        self,
        pos: str,
        sigma: frozendict,
    ) -> list[ABCDisplay]:
        """Calcule les morphèmes disponible pour le couple POS/sigma.

        :param pos: un POS disponible
        :param sigma: un sigma associé à ce POS
        :return: les morphèmes existant dans les blocs
        """
        if pos not in self.data:
            message = (
                f"'{pos}' n'est pas dans les catégories disponibles "
                f"{list(self.data.keys())}."
            )
            raise KeyError(message)

        output: list[ABCDisplay] = []

        for bloc in self.data[pos]:
            morpheme = BlockEntry.__select_morpheme(sigma, bloc)
            if morpheme is not None:
                output.append(morpheme)
        return output

    @classmethod
    def from_dict(
        cls,
        data: dict[str, list[dict[str, str]]],
        phonology: Phonology,
    ) -> "BlockEntry":
        """Construit un BlockEntry depuis un dictionnaire.

        TODO : changer le type de 'data' en un TypedDict ou équivalent.

        :param data:
        :param phonology:
        :return:
        """
        return cls(
            data={
                category: list(cls.__rulify(block=rules, phonology=phonology))
                for category, rules in data.items()
            },
        )

    @staticmethod
    def __rulify(
        block: dict[str, str] | list[dict[str, str]],
        phonology: Phonology,
    ) -> Iterator[list[ABCDisplay]]:
        """Factory qui met en forme 'block' pour être facilement interrogé.

        :param block: Bloc ou liste de blocs de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        method_name = (
            f"_{BlockEntry.__name__}__rulify_"
            f"{block.__class__.__name__.lower()}"
        )
        return getattr(
            BlockEntry,
            method_name,
        )(
            block=block,
            phonology=phonology,
        )

    @staticmethod
    def __rulify_dict(
        block: dict[str, str],
        phonology: Phonology,
    ) -> Iterator[list[ABCDisplay]]:
        """Met en forme un bloc.

        :param block: Bloc de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        if not block:
            raise ValueError

        output: list[ABCDisplay] = []

        for key, value in block.items():
            _sigma = dictify(key)
            output.append(
                create_morpheme(
                    rule=value,
                    sigma=_sigma,
                    phonology=phonology,
                ),
            )

        yield output

    @staticmethod
    def __rulify_list(
        block: list[dict[str, str]],
        phonology: Phonology,
    ) -> Iterator[list[ABCDisplay]]:
        """Met en forme une liste de blocs.

        :param block: Liste de blocs de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        if not block:
            raise ValueError

        for i_block in block:
            yield from BlockEntry.__rulify_dict(
                block=i_block,
                phonology=phonology,
            )

    @staticmethod
    def __select_morpheme(
        sigma: frozendict,
        morphemes: list[ABCDisplay],
    ) -> ABCDisplay | None:
        """Sélectionne un morphème si sigma contient morphemes[i].sigma.

        :param sigma: sigma d'un léxème
        :param morphemes: liste de morphèmes
        :return: le morphème le plus général lors du "<="
        """
        winner: ABCDisplay | None = None
        for morpheme in morphemes:
            if morpheme.get_sigma().items() <= sigma.items():
                winner = morpheme
        return winner
