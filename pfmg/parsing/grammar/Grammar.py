from dataclasses import dataclass

from pfmg.external.display import ABCDisplay
from pfmg.parsing.production import Production


@dataclass
class Grammar(ABCDisplay):
    """
    """
    start: str
    productions: list[Production]

    def to_string(self, **kwargs) -> str:
        """Convertit la Grammar en une chaîne de caractère pour NLTK.

        :param kwargs: inutile pour cette implémentation
        :return: Une grammaire parsable par FeatureGrammar.fromstring
        """
        return "\n\n".join(
            (
                f"% start {self.start}",
                "\n".join(x.to_string() for x in self.productions)
            )
        )
