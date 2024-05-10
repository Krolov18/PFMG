# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Interface pour les tokenizers."""

from abc import ABC, abstractmethod


class ABCTokenizer(ABC):
    """Interface pour ce qui est toknisable."""

    @abstractmethod
    def tokenize(self, sentence: str) -> list[str]:
        """Split some sentence into tokens.

        :param sentence:
        :return:
        """
