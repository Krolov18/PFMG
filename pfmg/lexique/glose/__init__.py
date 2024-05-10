# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Default Factory de Gloses."""
from pathlib import Path

from pfmg.utils.abstract_factory import factory_class


def new_gloses(path: Path):
    """Constructeur de Gloses.

    :param path: Chemin du fichier YAML
    :return: Gloses ou CGloses
    """
    assert __package__ is not None

    for name in ("CGloses", "Gloses"):
        try:
            result = factory_class(
                concrete_product=name,
                package=__package__
            ).from_yaml(
                path=path
            )
        except KeyError:
            continue
        else:
            return result
    else:
        raise NameError
