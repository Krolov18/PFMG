from pathlib import Path

from pfmg.utils.abstract_factory import factory_class


def new_gloses(path: Path):
    """Constructeur de Gloses.

    :param path: Chemin du fichier YAML
    :return: Gloses ou CGloses
    """
    assert __package__ is not None

    for name in ("Constrained", "Straight"):
        try:
            result = factory_class(
                concrete_product=f"{name}Pos2Sigmas",
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
