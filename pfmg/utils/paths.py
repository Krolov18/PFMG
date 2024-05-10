# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Helpers pour récupérer certains fichiers."""

import os
from pathlib import Path


def get_project_path() -> Path:
    """Récupère le chemin du projet.

    :return:
    """
    return Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def get_validation_file_path(project_path: Path | None = None) -> Path:
    """Récupère le chemin vers le schema des fichiers de config d'une grammaire.

    :param project_path:
    :return:
    """
    return (project_path or get_project_path()) / "schemas"
