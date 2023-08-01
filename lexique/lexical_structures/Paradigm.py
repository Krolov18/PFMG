from dataclasses import dataclass
from pathlib import Path

from lexique.lexical_structures.interfaces.Reader import Reader
from lexique.lexical_structures.Blocks import Blocks
from lexique.lexical_structures.Forme import Forme
from lexique.lexical_structures.Gloses import Gloses
from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.Morphemes import Morphemes
from lexique.lexical_structures.interfaces.Realizer import Realizer


@dataclass
class Paradigm(Realizer, Reader):
    """
    Classe qui permet de réaliser un paradigme.
    """
    gloses: Gloses
    blocks: Blocks

    def realize(self, lexeme: Lexeme) -> list[Forme]:
        """
        Méthode qui permet de réaliser un lexème donné.

        :param lexeme: Lexème à réaliser.
        :return: Liste des réalisations du lexème.
        """
        formes: list[Forme] = []

        for i_sigma in self.gloses.data[lexeme.pos]:
            if lexeme.sigma.items() <= i_sigma.items():
                formes.append(
                    Forme(
                        pos=lexeme.pos,
                        morphemes=Morphemes(
                            radical=lexeme.to_radical(),
                            others=self.blocks.select_morphemes(
                                pos=lexeme.pos,
                                sigma=i_sigma)),
                        sigma=i_sigma)
                )
        return formes

    @classmethod
    def from_disk(cls, path: Path) -> 'Paradigm':
        """
        Méthode permettant de charger un paradigme à partir d'un chemin donné.

        :param path: Chemin à partir duquel charger le paradigme.
        :return: Instance de Paradigm.
        """
        return cls(gloses=Gloses.from_disk(
            path=path / "Gloses.yaml"),
                   blocks=Blocks.from_disk(
                       path=path / "Blocks.yaml")
        )
