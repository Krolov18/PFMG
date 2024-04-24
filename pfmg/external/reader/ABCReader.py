# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Reader."""

from abc import ABC, abstractmethod
from pathlib import Path


class ABCReader[T](ABC):
    """Construit un type depuis des infos sur le disque."""

    @classmethod
    @abstractmethod
    def from_yaml(cls, path: Path) -> T:
        """Construit un type depuis un fichier sur le disque.

        :param path: Chemin du fichier
        :return: une instance T
        """
