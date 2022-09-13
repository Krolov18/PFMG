"""
    Fonctions permettant de réaliser les différentes structures définies dans structures.py
"""
from typing import Any

from frozendict import frozendict  # type: ignore

from lexique.applier import format_stem, apply
from lexique.structures import (Circumfix, Forme, Gabarit,
                                Lexeme, Prefix, Suffix,
                                Radical, Condition, Selection, Morpheme, Term)


def realize(term: Term | Morpheme, **kwargs: Any) -> str | tuple[str, ...] | list[Forme]:
    match term:
        case Lexeme(_, pos, sigma, traduction):
            assert traduction is not None
            output: list[Forme] = []
            for i_sigma, i_func in kwargs.get("paradigm", {})[pos].items():
                if not i_sigma:
                    output.append(i_func(term))
                    continue
                if (sigma.items() <= i_sigma["source"].items()) and (traduction.sigma.items() <= i_sigma["destination"].items()):  # and (term.sigma["destination"].items() <= sigma["destination"].items()):
                    output.append(i_func(term))
            return output
        case Forme(_, morphemes, sigma, _) as t:
            result = ""
            for morpheme in morphemes:
                assert morpheme.sigma is not None, morpheme
                m_sigma = dict(sigma)
                m_sigma.update(dict(morpheme.sigma))
                t.sigma = frozendict(m_sigma)
                result = realize(term=morpheme, accumulator=result, phonology=kwargs["phonology"])
            return result
        case Suffix(rule, _):
            assert rule is not None
            accumulator = kwargs.get("accumulator", "")
            return f"{accumulator}{rule.group(1)}"
        case Prefix(rule, _):
            assert rule is not None
            accumulator = kwargs.get("accumulator", "")
            return f"{rule.group(1)}{accumulator}"
        case Circumfix(rule, _):
            assert rule is not None
            accumulator = kwargs.get("accumulator", "")
            return f"{rule.group(1)}{accumulator}{rule.group(2)}"
        case Radical(_, _, stem):
            match stem:
                case str() as a:
                    return a
                case [a]:
                    return a
                case tuple() as s:
                    return s
                case _:
                    raise TypeError()
        case Gabarit(rule, _):
            accumulator = kwargs.get("accumulator", "")
            phonology = kwargs.get("phonology", "")
            return apply(rule.string,
                         format_stem(accumulator, phonology),
                         phonology)
        case Selection(rule, _):
            assert rule is not None
            accumulator = kwargs.get("accumulator", "")
            return accumulator[int(rule.group(1)) - 1]
        case Condition(_, _, cond, true, false):
            accumulator = kwargs.get("accumulator", "")
            try:
                _ = realize(term=cond, accumulator=accumulator)
            except IndexError:
                return realize(term=false, accumulator=accumulator)
            return realize(term=true, accumulator=accumulator)
        case _:
            raise TypeError()
