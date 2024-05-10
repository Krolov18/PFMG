# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass

from pfmg.parsing.features.FeatureMixin import FeatureMixin
from pfmg.parsing.features.utils import FeatureReader


@dataclass
class Features(FeatureMixin):
    """TODO : Write some doc."""

    data: list[dict]

    def __setitem__(self, key: int, value: dict):
        """TODO : Write some doc."""
        self.data[key] = value

    def __getitem__(self, item: int):
        """TODO : Write some doc."""
        return self.data[item]

    def __iter__(self):
        """TODO : Write some doc."""
        return iter(self.data)

    @classmethod
    def from_string(cls, data: str, target: str, phrase_len: int) -> "Features":
        """TODO : Write some doc."""
        data = Features.broadcast(data, phrase_len)
        return cls(data=FeatureReader().parse(data=data, target=target))

    def to_nltk(self) -> list[str]:
        """TODO : Write some doc."""
        result: list[str] = []

        for i_x in self.data:
            result.append(
                ",".join([f"{key}={value}" for key, value in i_x.items()])
            )

        return result

    def add_translation(self, translations: list[str]) -> None:
        """Ajoute les champs 'translation' aux parties de la RHS.

        :param translations:
        :return:
        """
        assert len(translations) == len(self.data)
        for i in range(len(translations)):
            self.data[i]["translation"] = f"?{translations[i]}{i}"

    def get_translations(self) -> tuple[str, ...]:
        """TODO : Write some doc."""
        return tuple(x["translation"] for x in self.data)
