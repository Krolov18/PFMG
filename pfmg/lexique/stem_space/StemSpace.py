# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""StemSpace."""

from dataclasses import dataclass


@dataclass
class StemSpace:
    """StemSpace."""

    stems: tuple[str, ...]
