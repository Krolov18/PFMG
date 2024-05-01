# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc.

TODO : Tree ne doit pas être un type de sortie.
 Il faut implémenter Sentence!
"""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Self, overload

from nltk import Tree

from pfmg.external.reader import ABCReader
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable
from pfmg.parsing.parser import Parser


@dataclass
class KParser(ABCReader, MixinParseParsable):
    """Parser bipartite.

    Le KParser va parser une première pour traduire
    puis une seconde fois pour valider la traduction.
    """

    translator: Parser
    validator: Parser

    @classmethod
    def from_yaml(cls, path: str | Path) -> Self:
        """TODO : Write some doc."""
        path = Path(path)
        from pfmg.lexique.lexicon import Lexicon
        from pfmg.parsing.grammar import KGrammar

        assert path.exists() and path.is_dir()

        lexicon = Lexicon.from_yaml(path)
        grammar = KGrammar.from_yaml(path / "MorphoSyntax.yaml")
        return cls(
            translator=Parser(
                lexique=lexicon, grammar=grammar.translator, how="translation"
            ),
            validator=Parser(
                lexique=lexicon, grammar=grammar.validator, how="validation"
            ),
        )

    def to_file(
        self, path: str | Path, id_grammar: Literal["validator", "translator"]
    ) -> None:
        """Enregistre le contenu de la grammaire dans un fichier txt.

        :param path: Chemin de sortie où stocker le fichier
        :param id_grammar: Identifiant de la grammaire à exporter
        """
        getattr(self, id_grammar).to_file(path)

    @overload
    def parse(self, data: str, keep: Literal["first"]) -> str: ...

    @overload
    def parse(
        self, data: str | list[str], keep: Literal["all"]
    ) -> list[str]: ...

    @overload
    def parse(
        self, data: list[str], keep: Literal["first", "all"]
    ) -> list[str]: ...

    def parse(self, data, keep) -> str | list[str]:
        """TODO : Write some doc.

        TODO : Tree -> Sentence
         Sentence doit être une structure de données qui contient
         toutes les infos de source et de destination.
         Simplifier cette méthode.

        :param data: data à parser
        :param keep: Récupérer la première valeur trouvée ou toutes les valeurs
        :return: une Sentence ou un itérateur de Sentence
        """
        translation: str | list[str]
        try:
            tree = self.translator.parse(data, keep)
            match tree:
                case Tree():
                    translation = " ".join(tree.label()["Traduction"])
                case Iterator():
                    translation = [
                        " ".join(x.label()["Traduction"]) for x in tree
                    ]
                case _:
                    raise TypeError
        except Exception:  # noqa BLE001
            message = f"'{data}' n'est pas reconnu par le traducteur."
            raise ValueError(message) from None
        else:
            try:
                self.validator.parse(translation, keep)
            except Exception:  # noqa BLE001
                message = (
                    f"'{data}' a été correctement traduit mais le "
                    f"validateur l'a refusé. Revoyez le champ "
                    f"Traduction."
                )
                raise ValueError(message) from None
            else:
                return translation
