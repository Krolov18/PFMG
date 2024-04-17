"""Différents utilitaires."""

from ast import literal_eval

from frozendict import frozendict


def dictify(chars: str) -> frozendict:
    """Transforme une chaine de caractères en un frozendict.

    :param chars: Une chaine de caractère prête
                  à être parsée et convertie en frozendict.
    :return: un frozendict
    """
    return frozendict(
        (
            {}
            if chars == ""
            else literal_eval(
                ('{"' + chars.replace("=", '":"').replace(",", '","') + '"}'),
            )
        ),
    )
