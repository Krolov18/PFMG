# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Actions du main du package parsing."""

import sys

from pfmg.parsing.parser import KParser
from pfmg.utils.abstract_factory import factory_function


def action(
    namespace: dict,
) -> None:
    """Factory qui lance n'importe quelle action disponible.

    :param namespace: namespace généré par ArgumentParser.parse_args()
    """
    name = namespace.pop("name")
    assert name is not None

    factory_function(
        concrete_product=f"{name}_action",
        package=__name__,
        namespace=namespace,
    )


def parsing_action(namespace: dict) -> None:
    """Construit un KParser et parse des data.

    :param namespace: paramètres de KParser et de parse
    """
    parser = KParser.from_yaml(namespace.pop("path"))

    result = parser.parse(**namespace)

    if isinstance(result, str):
        result = [result]

    sys.stdout.write("\n".join(result) + "\n")
