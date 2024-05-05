# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import TypedDict

from frozendict import frozendict

d_grid = dict[str, list[str]]
l_grid = list[d_grid]
d_or_l_grid = d_grid | l_grid
SubGlose = dict[str, list[frozendict]]


class GlosesStruct(TypedDict):
    """Typage stricte du dictionnaire Gloses."""

    source: frozendict[str, str]
    destination: frozendict[str, str]
