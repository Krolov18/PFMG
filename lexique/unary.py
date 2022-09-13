from typing import Callable

from frozendict import frozendict

from lexique.realizer import realize
from lexique.structures import Forme, Lexeme, Phonology


# @multimethod
# def unary(id_unary: str,
#           term: Forme,
#           phonology: Phonology) -> str:
#     return factory_function(concrete_product=f"{id_unary}_unary",
#                             package=__name__,
#                             term=term,
#                             phonology=phonology)


# @multimethod
# def unary(id_unary: str,
#           term: List[Lexeme],
#           paradigm: Dict[str, Dict[frozendict, Callable]],
#           phonology: Phonology) -> List[str]:
#     output: List[str] = list()
#     for lexeme in term:
#         for form in realize(term=lexeme, paradigm=paradigm):
#             output.append(unary(id_unary, form, phonology))
#     return output


# def fcfg_unary(term: Forme, phonology: Phonology) -> str:
#     features = ",".join(f"{feat}='{val}'" for feat, val in term.sigma.items())
#     return (f"{term.pos}[{features},TRADUCTION='{realize(term=term.traduction, phonology=phonology)}'] -> "
#             f"'{realize(term=term, phonology=phonology)}'")


def tcfg_unary(term: Forme, phonology: Phonology) -> str:
    assert term.traduction is not None
    features = ",".join(f"{feat}='{val}'" for feat, val in term.sigma.items())
    traduction = f"TRADUCTION='{realize(term=term, phonology=phonology)}'"
    t_features = ",".join(f"{feat}='{val}'" for feat, val in term.traduction.sigma.items())

    source = "" if not features else f"SOURCE=[{t_features},{traduction}]"
    destination = "" if not t_features else f"DESTINATION=[{features}]"
    if not (source and destination):
        output = f"[{traduction}]"
    else:
        output = f"[{source}, {destination}]"
    return f"{term.pos}{output} -> '{realize(term=term.traduction, phonology=phonology)}'"
    # return f"{term.pos}[{features},Traduction='{realize(term=term, phonology=phonology)}'] ->
    # '{realize(term=term.traduction, phonology=phonology)}'"


# def cfg_unary(term: Forme, phonology: Phonology) -> str:
#     return f"{term.pos} -> '{realize(term=term, phonology=phonology)}'"


def unary(term: Lexeme | Forme,
          phonology: Phonology,
          paradigm: dict[str, dict[frozendict, Callable]] | None,
          id_unary: str = None) -> str:
    rule: str = "{lhs}{lhs_options} -> '{rhs}'"
    match term:
        case Forme(pos, _, sigma, traduction) as f:
            match id_unary:
                case "cfg":
                    return rule.format(lhs=pos,
                                       lhs_options="",
                                       rhs=realize(term=f, phonology=phonology))
                case "fcfg":
                    assert traduction is not None
                    features = "[{feats},TRADUCTION='{realisation}']"
                    feats = features.format(feats=",".join(f"{feat}='{val}'" for feat, val in sigma.items()),
                                            realisation=realize(term=traduction, phonology=phonology))
                    return rule.format(lhs=pos,
                                       lhs_options=feats,
                                       rhs=realize(term=f, phonology=phonology))
                case "tcfg":
                    assert traduction is not None
                    features = "[{feats},TRADUCTION='{realisation}']"
                    source_features = ""
                    return features
                case _:
                    raise ValueError()
        case Lexeme() as l:
            assert paradigm is not None
            result = ""
            for form in realize(term=l, paradigm=paradigm):
                result += unary(term=term, phonology=phonology, id_unary=id_unary, paradigm=paradigm)
        case _:
            raise TypeError()
