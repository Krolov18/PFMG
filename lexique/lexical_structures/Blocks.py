from ast import literal_eval
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import yaml
from frozendict import frozendict

from lexique.lexical_structures.interfaces.Reader import Reader
from lexique.lexical_structures.Factory import create_morpheme
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.interfaces.Display import Display
from lexique.lexical_structures.interfaces.Selector import Selector


@dataclass
class Blocks(Reader, Selector):
    data: dict[str, list[list[Display]]]
    phonology: Phonology

    @classmethod
    def from_disk(cls, path: Path) -> 'Blocks':
        """
        :param path: Chemin du dossier qui contient Phonology.yaml et Blocks.yaml
        :return: un struct Blocks
        """
        assert path.name.endswith("Blocks.yaml")

        with open(path, mode="r", encoding="utf8") as file_handler:
            data: dict[str, list[dict[str, str]]] = yaml.load(file_handler, Loader=yaml.Loader)

        phonology_from_disk = Phonology.from_disk(path.parent / "Phonology.yaml")
        return cls(data={category: list(cls.__rulify(block=rules, phonology=phonology_from_disk))
                         for category, rules in data.items()},
                   phonology=phonology_from_disk)

    @staticmethod
    def __rulify(block: dict[str, str] | list[dict[str, str]], phonology: Phonology) -> Iterator[list[Display]]:
        """
        :param block: Bloc ou liste de blocs de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        method_name = f"_{Blocks.__name__}__rulify_{block.__class__.__name__.lower()}"
        return getattr(Blocks, method_name)(block=block, phonology=phonology)

    @staticmethod
    def __rulify_dict(block: dict[str, str], phonology: Phonology) -> Iterator[list[Display]]:
        """
        :param block: Bloc de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        if not block:
            raise ValueError()

        output: list[Display] = []

        for key, value in block.items():
            _sigma = Blocks.__dictify_str(key)
            output.append(create_morpheme(rule=value, sigma=_sigma, phonology=phonology))

        yield output

    @staticmethod
    def __rulify_list(block: list[dict[str, str]], phonology: Phonology) -> Iterator[list[Display]]:
        """
        :param block: Liste de blocs de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        if not block:
            raise ValueError()

        for i_block in block:
            yield from Blocks.__rulify_dict(block=i_block, phonology=phonology)

    @staticmethod
    def __dictify_str(chars: str) -> frozendict:
        """
        :param chars: Une chaine de caractère prête à être parsée et convertie en frozendict.
        :return: Transforme une chaine de caractère en un frozendict python.
        """
        return frozendict(
            {} if chars == "" else literal_eval("{\"" + chars.replace("=", "\":\"").replace(",", "\",\"") + "\"}")
        )

    def select_morphemes(self, pos: str, sigma: frozendict) -> list[Display]:
        """
        :param pos:
        :param sigma:
        :return:
        """
        if pos not in self.data:
            raise KeyError(f"'{pos}' n'est pas dans les catégories disponibles {list(self.data.keys())}.")

        output: list[Display] = []

        for bloc in self.data[pos]:
            if (morpheme := Blocks.__select_morpheme(sigma, bloc)) is not None:
                output.append(morpheme)
        return output

    @staticmethod
    def __select_morpheme(sigma: frozendict, morphemes: list[Display]) -> Display | None:
        """
        :param sigma:
        :param morphemes:
        :return:
        """
        winner: Display | None = None
        for morpheme in morphemes:
            if morpheme.get_sigma().items() <= sigma.items():
                winner = morpheme
        return winner
