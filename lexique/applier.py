"""
    Fonctions gérant les gabarits
"""
from frozendict import frozendict

from lexique.structures import Phonology


def verify(char: str, stem: frozendict, phonology: Phonology) -> str:
    assert char
    match char:
        case "U":
            return phonology.apophonies[phonology.apophonies[stem['V']]]
        case "A":
            return phonology.apophonies[stem[phonology.derives[char]]]
        case "V":
            return stem[char]
        case "1" | "2" | "3":
            return stem[char]
        case "4" | "5" | "6":
            return phonology.mutations[stem[str(int(char) - 3)]]
        case "7" | "8" | "9":
            return phonology.mutations[phonology.mutations[stem[str(int(char) - 6)]]]
        case _:
            return char


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
        match lettre:
            case l if l in phonology.consonnes:
                result[str(c)] = lettre
                c += 1
            case l if l in phonology.voyelles:
                if not result["V"]:
                    result['V'] = lettre

    return frozendict(result)
