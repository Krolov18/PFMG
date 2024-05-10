# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Désinence."""

from dataclasses import dataclass


@dataclass
class Desinence:
    """Ensemble de morphèmes pour source/destination."""

    source: list["Morpheme"]  # noqa # type: ignore
    destination: list["Morpheme"]  # noqa # type: ignore
