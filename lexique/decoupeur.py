from lexique.structures import Morpheme, Circumfix, Forme, Gabarit, Prefix, Radical, Suffix


def decoupe(term: Morpheme | Forme, accumulator: str) -> str:
    match term:
        case Forme():
            result = ""
            for morpheme in term.morphemes:
                result = decoupe(morpheme, result)
            return result
        case Prefix():
            assert term.rule is not None
            return f"{term.rule.group(1)}-{accumulator}"
        case Circumfix():
            assert term.rule is not None
            return f"{term.rule.group(1)}+{accumulator}+{term.rule.group(2)}"
        case Suffix():
            assert term.rule is not None
            return f"{accumulator}-{term.rule.group(1)}"
        case Gabarit():
            # TODO : quelle stratégie appliquons nous pour les gabarits ?
            pass
        case Radical():
            return term.stem
        case _:
            pass
