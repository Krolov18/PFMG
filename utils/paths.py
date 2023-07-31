import os
from pathlib import Path


def get_project_path() -> Path:
    return Path(os.path.dirname(os.path.dirname(__file__)))


def get_validation_file_path(project_path: Path = get_project_path()) -> Path:
    return project_path / "schemas"


def get_data_test_grammar() -> Path:
    return Path(__file__).parent / "test" / "data_for_test"
