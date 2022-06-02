from multimethod import multimethod

from lexique.structures import Circumfix, Forme, Gabarit, Prefix, Radical, Suffix


@multimethod
def decoupe(term: Prefix, accumulator: str) -> str:
    return f"{term.rule.group(1)}-{accumulator}"


@multimethod
def decoupe(term: Suffix, accumulator: str) -> str:
    return f"{accumulator}-{term.rule.group(1)}"


@multimethod
def decoupe(term: Circumfix, accumulator: str) -> str:
    return f"{term.rule.group(1)}+{accumulator}+{term.rule.group(2)}"


@multimethod
def decoupe(term: Gabarit, accumulator: str) -> str:
    # TODO : quelle stratégie appliquons nous pour les gabarits ?
    pass


@multimethod
def decoupe(term: Radical, accumulator: str) -> str:
    return term.stem


@multimethod
def decoupe(term: Forme) -> str:
    result = ""
    for morpheme in term.morphemes:
        result = decoupe(morpheme, result)
    return result
