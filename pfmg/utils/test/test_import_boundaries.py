"""Regression tests for package-layer import boundaries."""

import ast
from pathlib import Path

import pytest

_PACKAGE_ROOT = Path(__file__).resolve().parents[2]

_BOUNDARIES: dict[str, tuple[str, ...]] = {
    "lexique": ("pfmg.parsing",),
    "external": ("pfmg.lexique",),
}


def _python_modules(package: str) -> list[Path]:
    root = _PACKAGE_ROOT / package
    return sorted(root.rglob("*.py"))


def _imported_modules(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
    return modules


def _relative_module(path: Path) -> str:
    return path.relative_to(_PACKAGE_ROOT).with_suffix("").as_posix().replace("/", ".")


@pytest.mark.parametrize("package,forbidden", _BOUNDARIES.items())
def test_package_import_boundaries(package: str, forbidden: tuple[str, ...]) -> None:
    """Domain packages must not import forbidden higher-level modules."""
    violations: list[str] = []
    for module_path in _python_modules(package):
        module_name = _relative_module(module_path)
        for imported in _imported_modules(module_path):
            if any(
                imported == prefix or imported.startswith(f"{prefix}.")
                for prefix in forbidden
            ):
                violations.append(f"{module_name} imports {imported}")
    assert not violations, "Import boundary violations:\n" + "\n".join(violations)
