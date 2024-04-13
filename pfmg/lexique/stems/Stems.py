"""Itérateur de Lexèmes."""
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.reader.Reader import Reader
from pfmg.lexique.stem_space.StemSpace import StemSpace
from pfmg.lexique.utils import dictify


@dataclass
class Stems(Reader, Iterable):
    """Itérateur de Lexèmes."""

    data: Iterator[Lexeme]

    @classmethod
    def from_disk(cls, path: Path) -> "Stems":
        """Construit l'Itérateur à partir d'un fichier YAML.

        :param path: Chemin vers le fichier YAML.
        :return: Objet Stems
        """
        assert path.name.endswith("Stems.yaml")
        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)
            return cls(data=iter(Stems.__read_stems(data, data.keys())))

    @staticmethod
    def __read_stems(
        data: dict[str, dict[str, list[str]] | dict[str, dict]],
        posses: set,
        accumulator: dict | None = None,
    ) -> Iterator[Lexeme]:
        """Parse le fichiers stems.

        Fonction récursive.

        :param data: Contenu du fichier YAML en dictionnaire
        :param posses: Ensemble des POS de la Grammaire
        :param accumulator: Structure interne pour gérer les POS et les sigmas
        :return: Itérateur de Lexèmes
        """
        for key, value in data.items():
            match value:
                case str():
                    _acc = accumulator.copy()
                    accumulator = {"pos": _acc.pop("pos")}
                    pos = (key
                           if accumulator is None
                           else accumulator["pos"])
                    t_stems, t_sigma = Stems.__parse_traduction(value)
                    yield Lexeme(
                        source=LexemeEntry(
                            stems=t_stems,
                            pos=pos,
                            sigma=t_sigma,
                        ),
                        destination=LexemeEntry(
                            stems=StemSpace(stems=tuple(key.split(","))),
                            pos=pos,
                            sigma=frozendict(_acc),
                        ),
                    )
                case dict():
                    if key in posses:
                        accumulator = {"pos": key}
                    else:
                        accumulator.__setitem__(*key.split("="))
                    yield from Stems.__read_stems(value, posses, accumulator)

    @staticmethod
    def __parse_traduction(token: str) -> tuple[StemSpace, frozendict]:
        """Méthode privée qui parse la traduction.

        :param token: string + POS + inhérence
        :return: un StemSpace et ses traits inhérents (sigma)
        """
        str_stems, str_sigma = token.split(".") if "." in token else (token, "")
        return StemSpace(stems=tuple(str_stems.split(","))), dictify(str_sigma)

    def __iter__(self):
        """Récupère l'itérateur de Lexèmes."""
        return self.data