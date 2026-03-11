"""Factory for Gloses (StraightPos2Sigmas or ConstrainedPos2Sigmas)."""

from pathlib import Path

from pfmg.utils.abstract_factory import factory_class


def new_gloses(path: Path):
    """Load Gloses from YAML; returns StraightPos2Sigmas or ConstrainedPos2Sigmas.

    Args:
        path: Path to the Gloses YAML file.

    Returns:
        StraightPos2Sigmas | ConstrainedPos2Sigmas: Gloses instance.

    """
    assert __package__ is not None

    for name in ("Constrained", "Straight"):
        try:
            result = factory_class(
                concrete_product=f"{name}Pos2Sigmas", package=__package__
            ).from_yaml(path=path)
        except KeyError:
            continue
        else:
            return result
    else:
        raise NameError
