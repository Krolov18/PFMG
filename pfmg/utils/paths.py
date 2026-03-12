"""Helpers to resolve project and schema paths."""

import os
from pathlib import Path


def get_project_path() -> Path:
    """Return the project root directory (parent of parent of utils).

    Returns:
        Path: The project root directory.

    """
    return Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def get_validation_file_path(project_path: Path | None = None) -> Path:
    """Return the path to the grammar config schema directory.

    Args:
        project_path: Optional project root; if None, uses get_project_path().

    Returns:
        Path: Path to the schemas directory.

    """
    return (project_path or get_project_path()) / "schemas"
