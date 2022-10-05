import itertools as it
import operator
import operator as op
import re
from typing import Iterator, Literal

from utils.trie import to_pattern

type_stems = dict[str, dict[str, str] | dict[str, dict[str, str]]]
type_att_vals = dict[str, list[str]]


def gridify(gloses: list[type_att_vals] | type_att_vals) -> Iterator[list[tuple[str, str | int | bool]]]:
    # assert gloses

    match gloses:
        case dict():
            yield from gridify([gloses])
        case list():
            for params in gloses:
                yield from map(lambda x: [*zip(params.keys(), x)], it.product(*params.values()))
        case _:
            raise TypeError("toto")


def cuefy(attribute_name: str, values: list[str]) -> list[str]:
    assert attribute_name
    assert values and all(values)

    if len(values) == 1:
        return [f"#{attribute_name}: \"{values[0]}\"",
                f"#{attribute_name}{values[0].capitalize()}: {{#{attribute_name}, \"{values[0]}\"}}"]

    return [f"#{attribute_name}: =~\"^{to_pattern(values)}$\"",
            *[f"#{attribute_name}{value.capitalize()}: {{#{attribute_name}, \"{value}\"}}" for value in values]]


def cuefy2(category: str, attributes: list[str]) -> list[str]:
    assert category

    if not attributes or not any(attributes):
        # assert attributes and all(attributes), f"{category}"
        return [f"#Sigma{category}: #Sigma"]

    formatted_attributes = format_attributes(attributes)

    return [f"#Sigma{category}: {{#Sigma, {formatted_attributes}}}"]


def format_attributes(attributes):
    match attributes:
        case [_]:
            formatted_attributes = f"{(attribute := attributes[0]).lower()}: #{attribute}"
        case list():
            formatted_attributes = ", ".join([f"{attribute}: #{attribute}" for attribute in attributes])
        case _:
            raise TypeError("there")
    return formatted_attributes


def read_glose(glose: dict[str, list[type_att_vals] | type_att_vals]) -> list[str]:
    assert glose

    output: list[str] = [f"#Category: =~\"^{to_pattern(list(glose.keys()))}$\""]

    for category, att_vals in glose.items():
        attributes: list[str] = []
        match att_vals:
            case list():
                for att_val in att_vals:
                    attributes.extend(att_val.keys())
                    for att, vals in att_val.items():
                        output.extend(cuefy(att, vals))
            case dict():
                attributes = list(att_vals.keys())
                for att, vals in att_vals.items():
                    output.extend(cuefy(att, vals))
            case _:
                raise TypeError("here")
        output.extend(cuefy2(category, attributes))
        output.append(f"#Forme{category}: #Forme & {{_lexeme: #Lexeme{category}, pos: \"{category}\", sigma: #Sigma{category}}}")

        formes = "#Formes{category}: {{{formes}}}"
        _formes = []
        for sigma in gridify(att_vals):
            values = "".join(list(map(str.capitalize, map(operator.itemgetter(1), sigma))))
            gg = ", ".join([f"{attribute}: #{attribute}{value.capitalize()}" for attribute, value in sigma])
            output.append(f"#Sigma{category}{values}: #Sigma{category} & {{{gg}}}")
            # output.append(f"#Forme{category}{values}: #Forme{category} & {{sigma: #Sigma{category}{values}}}")
            output.append((f"#Forme{category}{values}: #Forme{category} & {{"
                           f"sigma: #Sigma{category}{values}, "
                           f"morphemes: [for m in #Lexeme{category}.paradigm {{m & {{_sigma: #Forme{category}{values}.sigma}}}}]}}"))
            _formes.append(f"#Forme{category}{values}")
        output.append(formes.format(category=category, formes=" | ".join(_formes)))
    return output


def choose_rule(rule: str) -> str:
    assert rule
    if rule.startswith("X+"):
        return "Suffix"
    if rule.endswith("+X"):
        return "Prefix"
    if "+X+" in rule:
        return "Circumfix"
    raise TypeError(rule)


def cuefy_block(block: dict[str, str]) -> str:
    assert block

    output: list[str] = list()
    pattern = "#{RuleIdentifier} & {{sigma: {{{sigma}}}, _sigma: {{{sigma}}}, rule: \"{rule}\"}}"
    for key, value in block.items():
        assert value is not None
        rrule = pattern.format(RuleIdentifier=choose_rule(value), sigma=key.replace("=", ": \"").replace(",", "\",") + "\"", rule=value)
        assert "None" not in rrule, value
        output.append(rrule)

    return " | ".join(output)


def cuefy_blocks(blocks: dict[str, list[dict[str, str]]]) -> list[str]:
    pattern = "#Lexeme{pos}: #Lexeme & {{pos: \"{pos}\", paradigm: {morphemes}}}"
    output: list[str] = []

    for i_pos, i_blocks in blocks.items():
        morphemes = [cuefy_block(i_block) for i_block in i_blocks]
        output.append(pattern.format(pos=i_pos, morphemes=f"[{','.join(morphemes)}]"))

        # morphemes = ["#Morpheme"] + [f"#Morpheme & {{stem: #Lexeme{i_pos}.paradigm[{i}].realisation}}" for i in range((len(i_blocks)-1))]
        # output.append(pattern.format(pos=i_pos, morphemes=f"[{','.join(morphemes)}]"))

        morphemesn = [f"#Morpheme & {{stem: morphemes[{i}].realisation}}" for i in range((len(i_blocks) - 1))]
        morphemes = []
        realisation = ""
        if morphemesn:
            morphemes += ["#Morpheme"] + morphemesn
            realisation = ",realisation: morphemes[len(morphemes)-1].realisation"
        output.append("#Forme{pos}: #Forme & {{morphemes: {morphemes}{realisation}}}".format(pos=i_pos, morphemes=f"[{','.join(morphemes)}]", realisation=realisation))

    return output


def read_stems(stems: type_stems) -> list[str]:
    assert stems

    output: list[str] = []

    reg = re.compile(r"(?<==)(\w+)(?=,|$)")

    for category, attvals_stem in stems.items():
        for key, value in attvals_stem.items():
            match value:
                case str():
                    # TODO: value ici sera la traduction
                    output.append(f"#{key}{category}: #Lexeme{category} & {{stems: \"{key}\"}}")
                case dict() as stem_trad:
                    _sigma = key.replace("=", ": \"").replace(",", "\",") + "\""
                    values = "".join(map(str.capitalize, reg.findall(key)))
                    sigma = f"sigma: {{{_sigma}}}"
                    for stem, traduction in stem_trad.items():
                        # TODO: traduction à gérer
                        output.append(
                            f"#{stem}{category}{values}: #Lexeme{category} & {{sigma: {{{_sigma}}}, stems: \"{stem}\"}}")
                case _:
                    raise TypeError()

    return output
