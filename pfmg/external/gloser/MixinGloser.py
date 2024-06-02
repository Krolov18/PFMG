# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Doc à écrire."""

from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.stem_space.StemSpace import StemSpace


class MixinGloser(ABCGloser):
    """TODO : Doc à écrire."""

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return getattr(self, f"_to_glose__{term.__class__.__name__.lower()}")(
            term=term,
        )

    def _to_glose__nonetype(self, term: None = None) -> str:
        raise NotImplementedError

    def _to_glose__stemspace(self, term: StemSpace) -> str:
        raise NotImplementedError

    def _to_glose__str(self, term: str) -> str:
        raise NotImplementedError
