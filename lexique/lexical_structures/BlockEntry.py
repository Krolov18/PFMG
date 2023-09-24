from ast import literal_eval
from dataclasses import dataclass
from typing import Iterator

from frozendict import frozendict

from lexique.lexical_structures.Factory import create_morpheme
from lexique.lexical_structures.interfaces.Display import Display
from lexique.lexical_structures.interfaces.Selector import Selector
from lexique.lexical_structures.Phonology import Phonology


@dataclass
class BlockEntry(Selector):
    data: dict[str, list[list[Display]]]

    def __post_init__(self):
        assert self.data
        assert all(self.data.values())
        assert all(all(x) for x in self.data.values())

    def __call__(
        self,
        pos: str,
        sigma: frozendict
    ) -> list[Display]:
        """
        :param pos:
        :param sigma:
        :return:
        """
        if pos not in self.data:
            raise KeyError(
                (f"'{pos}' n'est pas dans les catégories disponibles"
                 f" {list(self.data.keys())}.")
            )

        output: list[Display] = []

        for bloc in self.data[pos]:
            morpheme = BlockEntry.__select_morpheme(sigma, bloc)
            if morpheme is not None:
                output.append(morpheme)
        return output

    @classmethod
    def from_dict(
        cls,
        data: dict[str, list[dict[str, str]]],
        phonology: Phonology
    ) -> 'BlockEntry':
        return cls(
            data={category: list(
                cls.__rulify(block=rules, phonology=phonology)
            ) for category, rules in data.items()}
        )

    @staticmethod
    def __rulify(
        block: dict[str, str] | list[dict[str, str]],
        phonology: Phonology
    ) -> Iterator[list[Display]]:
        """
        :param block: Bloc ou liste de blocs de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        method_name = (f"_{BlockEntry.__name__}__rulify_"
                       f"{block.__class__.__name__.lower()}")
        return getattr(
            BlockEntry,
            method_name
        )(
            block=block,
            phonology=phonology
        )

    @staticmethod
    def __rulify_dict(
        block: dict[str, str],
        phonology: Phonology
    ) -> Iterator[list[Display]]:
        """
        :param block: Bloc de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        if not block:
            raise ValueError()

        output: list[Display] = []

        for key, value in block.items():
            _sigma = BlockEntry.__dictify_str(key)
            output.append(
                create_morpheme(
                    rule=value,
                    sigma=_sigma,
                    phonology=phonology
                )
            )

        yield output

    @staticmethod
    def __rulify_list(
        block: list[dict[str, str]],
        phonology: Phonology
    ) -> Iterator[list[Display]]:
        """
        :param block: Liste de blocs de règles
        :return: liste de blocs au format frozendict/Morpheme
        """
        if not block:
            raise ValueError()

        for i_block in block:
            yield from BlockEntry.__rulify_dict(
                block=i_block,
                phonology=phonology
            )

    @staticmethod
    def __dictify_str(chars: str) -> frozendict:
        """
        :param chars: Une chaine de caractère prête 
                      à être parsée et convertie en frozendict.
        :return: Transforme une chaine de caractère en un frozendict python.
        """
        return frozendict(
            ({}
             if chars == ""
             else literal_eval(
                ("{\""
                 + chars.replace("=", "\":\"").replace(",", "\",\"")
                 + "\"}")
            ))
        )

    @staticmethod
    def __select_morpheme(
        sigma: frozendict,
        morphemes: list[Display]
    ) -> Display | None:
        """
        :param sigma:
        :param morphemes:
        :return:
        """
        winner: Display | None = None
        for morpheme in morphemes:
            if morpheme.get_sigma().items() <= sigma.items():
                winner = morpheme
        return winner
