"""TODO : Doc to write."""

from dataclasses import dataclass
from pathlib import Path

from frozendict import frozendict

from pfmg.external.reader import ABCReader


@dataclass
class ConstrainedGlose(ABCReader):
    """TODO : Doc to write."""

    gloses: dict[str, list[frozendict]]
    alignments: dict

    @classmethod
    def from_yaml(cls, path: Path) -> "ConstrainedGlose":
        """TODO : Doc to write."""
        raise NotImplementedError

    def __call__(
        self,
        pos: str,
    ) -> list[frozendict]:
        """Rècupère un ensemble de sigma, soit un sigma par case.

        :param item: un POS valide
        :return: Les cases du paradigmes de 'item'
        """
        return self.__filter(self.gloses[pos], self.alignments[pos])

    def __filter(
        self, pos_sigmas: list[frozendict], wrongs: list[frozendict]
    ) -> list[frozendict]:
        """Filtre les glose d'une catégorie syntaxique.

        Filtre sur des alignements morphosyntaxiques
        entre la source et la destination.

        :param pos_sigmas:
        :param wrongs: sigmas refusés
        :return: listes des sigmas filtrée
        """
        output: list[frozendict] = []
        for i_sigma in pos_sigmas:
            i_source = i_sigma["source"]
            i_destination = i_sigma["destination"]
            for j_sigma in wrongs:
                j_source = j_sigma["source"]
                j_destination = j_sigma["destination"]
                s_cond = j_source.items() <= i_source.items()
                d_cond = j_destination.items() <= i_destination.items()
                if s_cond and d_cond:
                    continue
                output.append(i_sigma)
        return output
