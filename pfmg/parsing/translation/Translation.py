# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass, field


@dataclass
class Translation:
    """TODO : Write some doc."""

    data: list[int] = field(default_factory=list)

    def apply_translation(
        self,
        syntagme: list[str],
        f_accords: list[dict],
        f_percolation: dict,
    ) -> None:
        """TODO : Write some doc."""
        for i in range(len(syntagme)):
            f_accords[i]["Source"]["Traduction"] = f"?{i}"
        f_percolation["Source"]["Traduction"] = tuple(
            f_accords[i_trad]["Source"]["Traduction"] for i_trad in self.data
        )
