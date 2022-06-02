from multimethod import multimethod

from lexique.structures import Circumfix, Forme, Gabarit, Prefix, Radical, Suffix


@multimethod
def glose(term: Prefix, accumulator: str) -> str:
    return f"{'.'.join(term.sigma.values())}-{accumulator}"


@multimethod
def glose(term: Suffix, accumulator: str) -> str:
    return f"{accumulator}-{'.'.join(term.sigma.values())}"


@multimethod
def glose(term: Circumfix, accumulator: str) -> str:
    features = '.'.join(term.sigma.values())
    return f"{features}+{accumulator}+{features}"


@multimethod
def glose(term: Gabarit, accumulator: str) -> str:
    pass


@multimethod
def glose(term: Radical, accumulator: str) -> str:
    pass


@multimethod
def glose(term: Forme) -> str:
    pass
