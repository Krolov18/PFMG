# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Implementation of a Trie."""

from collections.abc import Callable
from typing import TypeVar

_special_chars_map = {
    i: "\\" + chr(i) for i in b"()[]{}?*+-|^$\\.&~#\t\n\r\v\f"
}

T = TypeVar("T")
# type_memory = dict[str, "type_memory | Literal[1] | str"]


def identity(param: T) -> T:
    """Fonction d'identité.

    :param param: n'importe quoi
    :return: param
    """
    return param


def __escape(pattern: str) -> str:
    """Échappe les caractères de regex + quelques autres.

    :param pattern: Chaîne dans laquelle appliquer l'échappement.
    :return: Échappement à l'instar de celui du module re.
    """
    return pattern.translate(_special_chars_map)


def add_word(memory: dict, word: str) -> None:
    """Ajoute un mot dans le Trie.

    :param memory: Mapping mettant en mémoire les entrées déjà 'parsée'
    :param word: une nouvelle entrée à ajouter à memory
    """
    ref = memory
    for char in word:
        ref = ref.setdefault(char, ref.get(char, {}))
    ref[""] = 1


def add_words(memory: dict, words: list[str]) -> None:
    """Ajoute une liste de mots dans le Trie.

    :param memory: Mapping mettant en mémoire les entrées déjà 'parsée'
    :param words: entrées à ajouter à memory
    """
    for word in words:
        add_word(memory, word)


def __build_pattern(
    memory_data: dict,
    escape: Callable[[str], str] = identity,
) -> str | None:
    """Build a regular expression pattern from a dictionary.

    :param escape: function to escape characters,
                   default is the identity function
    :param memory_data: mapping storing entries that have already been parsed
    :return: pattern ready to be compiled
    """
    if not memory_data:
        return ""

    if "" in memory_data and len(memory_data) == 1:
        return None

    alternatives: list[str] = []
    characters: list[str] = []
    has_quantifier: bool = False

    for char, value in sorted(memory_data.items()):
        if isinstance(value, dict):
            dict_str = __build_pattern(value)
            match dict_str:
                case str():
                    alternatives.append(escape(char) + dict_str)
                case None:
                    characters.append(escape(char))
                case _:
                    raise ValueError
        else:
            has_quantifier = True

    is_characters_only = not alternatives

    if len(characters) > 0:
        alternatives.append(
            characters[0]
            if len(characters) == 1
            else f"[{''.join(characters)}]",
        )

    result = (
        alternatives[0]
        if len(alternatives) == 1
        else f"(?:{'|'.join(alternatives)})"
    )

    if has_quantifier:
        result = f"{result}?" if is_characters_only else f"(?:{result})?"

    return result


def dict2str(
    memory: dict,
    escape: Callable[[str], str] = identity,
) -> str | None:
    """Exploite un arbre de préfixes pour construire une tegex.

    :param escape: Fonction pour échapper les caractères
                   liés aux expressions régulières.
                   (fonction d'identité par défaut)
    :param memory: Mapping storing entries that have already been parsed
    :return: pattern ready to be compiled
    """
    return __build_pattern(memory, escape)


def to_pattern(words: list[str]) -> str:
    """Contruis et remplis un Trie avec une liste de mots.

    :param words: Liste de mots à convertir en un pattern optimisé.
    :return: Le pattern représente 'words' exactement. Ni plus, ni moins.
             Tous les mots, et uniquement ceux-là,
             présents dans 'words' sont reconnus
             par le pattern après compilation du pattern.
    """
    memory = {}
    add_words(memory, words)
    dict_str = dict2str(memory)
    assert dict_str is not None
    return dict_str


__all__ = ["add_word", "add_words", "to_pattern", "dict2str"]
