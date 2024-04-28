# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass

from pfmg.parsing.features.utils import FeatureReader


@dataclass
class Features:
    """TODO : Write some doc."""

    data: list[dict]

    @staticmethod
    def broadcast(data: str, i: int) -> str:
        """TODO : Write some doc."""
        assert (data.count(";") == 0) or (data.count(";") != (i - 1))
        return ((data + ";") * i).rstrip(";")

    @classmethod
    def from_string(
        cls,
        data: str,
        target: str
    ) -> "Features":
        """TODO : Write some doc."""
        return cls(
            data=FeatureReader().parse(
                data=data,
                target=target
            )
        )

    def to_nltk(self) -> list[str]:
        result: list[str] = []

        for i_x in self.data:
            result.append(
                ",".join([f"{key}={value}" for key, value in i_x.items()])
            )

        return result

    def add_translation(self, translations: list[str]) -> None:
        """Ajoute les champs traductions aux parties de la RHS.

        :param translations:
        :return:
        """
        assert len(translations) == len(self.data)
        for i in range(len(translations)):
            self.data[i]["Traduction"] = f"?{translations[i]}{i}"

    def get_translations(self) -> tuple[str, ...]:
        return tuple(x["Traduction"] for x in self.data)
