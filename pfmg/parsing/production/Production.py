"""TODO : Write some doc."""
from dataclasses import dataclass
from typing import Any

import nltk
from nltk.grammar import FeatStructNonterminal

from pfmg.parsing.agreement.Agreement import Agreement
from pfmg.parsing.percolation.Percolation import Percolation
from pfmg.parsing.translation.Translation import Translation


@dataclass
class Production:
    """TODO : Write some doc."""

    lhs: str
    syntagmes: list[str]
    accords: Agreement
    percolation: Percolation
    translation: Translation

    def to_string(self) -> str:
        """TODO : Write some doc."""
        structure = "{lhs}{percolation} -> {rhs}"

        return structure.format(
            lhs=self.lhs,
            percolation=self.percolation.to_string(),  # type: ignore
            rhs=" ".join(
                [f"{s}{a}" for s, a in
                 zip(self.syntagmes, self.accords, strict=True)]  # type: ignore
            )
        )

        # source = "Destination" if self.translation is None else "Source"
        # f_accords = [
        #     nltk.FeatStruct(source=nltk.FeatStruct())
        #     for _ in range(len(self.syntagmes))
        # ]
        # self.__parse_features(
        #     self.__broadcast(
        #         self.accords,
        #         len(self.syntagmes)
        #     ),
        #     f_accords,
        # )
        # f_percolation = nltk.FeatStruct(
        #     nltk.FeatStruct(source=nltk.FeatStruct())
        # )
        # self.__parse_percolation(
        #     self.__broadcast(),
        #     f_accords,
        #     f_percolation,
        # )
        #
        # if self.translation is not None:
        #     self.__parse_translation(f_accords, f_percolation)
        #
        # return nltk.Production(
        #     lhs=FeatStructNonterminal(self.lhs, **f_percolation),
        #     rhs=[
        #         i_s if i_s.islower() else FeatStructNonterminal(i_s, **i_a)
        #         for i_s, i_a in zip(self.syntagmes, f_accords, strict=True)
        #     ],
        # )

    def __broadcast(self) -> str:
        """TODO : Write some doc."""
        if self.accords.count(";") != 0:  # type: ignore
            return self.accords  # type: ignore
        if len(self.syntagmes) < 1:
            return self.accords  # type: ignore
        return ((self.accords + ";")  # type: ignore
                * len(self.syntagmes)).strip(";")  # type: ignore

    def __parse_translation(
        self,
        f_accords: list[nltk.FeatStruct],
        f_percolation: nltk.FeatStruct
    ):
        """TODO : Write some doc."""
        from nltk.featstruct import FeatureValueTuple

        for i in range(len(self.syntagmes)):
            f_accords[i]["Source", "Traduction"] = nltk.Variable(str(i))  # type: ignore
        f_percolation["Source", "Traduction"] = FeatureValueTuple(  # type: ignore
            f_accords[i_trad]["Source", "Traduction"]  # type: ignore
            for i_trad in self.translation  # type: ignore
        )

    def add_translation(self, other: Any):
        """TODO : Write some doc."""
        self_p = self.to_nltk()
        other_p = other.to_nltk()
        assert "Traduction" in self_p.lhs()["Source"]  # type: ignore
        assert all(
            "Traduction" in x["Source"]
            for x in self_p.rhs()  # type: ignore
            if isinstance(x, FeatStructNonterminal)
        )
        assert "Traduction" not in other_p.lhs()["Destination"]
        assert not any("Traduction" in x["Destination"] for x in other_p.rhs())

        self_p.lhs().update(other_p.lhs())  # type: ignore

        for i_idx, i_x in enumerate(self_p.lhs()["Source"]["Traduction"]):  # type: ignore
            self_p.rhs()[int(i_x.name)].update(other_p.rhs()[i_idx])  # type: ignore

        return self_p

    def to_nltk(self) -> str:  # type: ignore
        """TODO : Write some doc."""
