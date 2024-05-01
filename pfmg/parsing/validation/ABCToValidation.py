# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from abc import abstractmethod
from typing import Self


class ABCToValidation:
    """TODO : Write some doc."""

    @abstractmethod
    def to_validation(self) -> Self:
        """TODO : Write some doc."""
