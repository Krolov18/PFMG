from lexique.structures import Circumfix, Forme, Gabarit, Prefix, Radical, Suffix, Morpheme


def glose(term: Morpheme | Forme, accumulator: str) -> str:
    match term:
        case Prefix():
            assert term.sigma is not None
            return f"{accumulator}-{'.'.join(term.sigma.values())}"
        case Suffix():
            assert term.sigma is not None
            return f"{'.'.join(term.sigma.values())}-{accumulator}"
        case Circumfix():
            features = '.'.join(term.sigma.values())
            return f"{features}+{accumulator}+{features}"
        case Gabarit():
            # TODO
            pass
        case Radical():
            # TODO
            pass
        case Forme():
            # TODO
            pass
        case _:
            # TODO
            pass
