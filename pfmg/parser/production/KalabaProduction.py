# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""KalabaProduction."""

from dataclasses import dataclass

from nltk.grammar import Production


@dataclass
class KalabaProduction:
    """Production de Kalaba.

    source: Production pour la traduction
    destination: productionpour la validation
    """

    source: Production
    destination: Production
