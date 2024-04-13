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
    print(get_project_path() / "schemas")
    return (project_path or get_project_path()) / "schemas"
