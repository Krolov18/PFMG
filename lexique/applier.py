"""
    Fonctions gérant les gabarits
"""
from multimethod import overload

from frozendict import frozendict

from lexique.structures import Phonology


def is_123(char: str) -> bool:
    return char in "123"


def is_456(char: str) -> bool:
    return char in "456"


def is_789(char: str) -> bool:
    return char in "789"


def is_a(char: str) -> bool:
    return char == "A"


def is_u(char: str) -> bool:
    return char == "U"


def is_v(char: str) -> bool:
    return char == "V"


@overload
def verify(char: str, stem: frozendict, phonology: Phonology) -> str:
    assert char
    return char


@overload
def verify(char: is_u, stem: frozendict, phonology: Phonology) -> str:
    assert char
    return phonology.apophonies[phonology.apophonies[stem['V']]]


@overload
def verify(char: is_a, stem: frozendict, phonology: Phonology) -> str:
    assert char
    return phonology.apophonies[stem[phonology.derives[char]]]


@overload
def verify(char: is_v, stem: frozendict, phonology: Phonology) -> str:
    assert char
    return stem[char]


@overload
def verify(char: is_789, stem: frozendict, phonology: Phonology) -> str:
    assert char
    return phonology.mutations[phonology.mutations[stem[str(int(char) - 6)]]]


@overload
def verify(char: is_456, stem: frozendict, phonology: Phonology) -> str:
    assert char
    return phonology.mutations[stem[str(int(char) - 3)]]


@overload
def verify(char: is_123, stem: frozendict, phonology: Phonology) -> str:
    assert char
    return stem[char]


def apply(rule: str, stem: frozendict, phonology: Phonology) -> str:
    result = ""
    for char in rule:
        result += verify(char, stem, phonology)
    return result


def format_stem(stem: str, phonology: Phonology) -> frozendict:
    """

    input: glak
    output: {
        1: g
        2: l
        3: k
        V: a
    }
    TODO: Créer différents types de racines pour brasser plus de possibilités.
          De plus, il faut restreindre le format du stem
          par un assert pour n'accepter que cette structure de racine.
    :param stem: chaine de caractère au format CCVC
    :param phonology:
    :return:
    """
    assert stem

    c = 1
    result = {
        "1": "",
        "2": "",
        "V": "",
        "3": ""
    }

    for lettre in stem:

        if lettre in phonology.consonnes:
            result[str(c)] = lettre
            c += 1

        elif lettre in phonology.voyelles:
            if not result["V"]:
                result['V'] = lettre

    return frozendict(result)
