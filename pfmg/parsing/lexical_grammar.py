"""Export realized lexicon forms as NLTK lexical productions."""

from collections.abc import Iterable

from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.parsing.lexicon_lookup import RealizedLexicon


def quote(value: str) -> str:
    """Return *value* as a string literal the NLTK grammar reader accepts.

    The reader has no escape sequence, so a form containing one kind of quote
    is written with the other one, and a form containing both cannot be
    expressed at all.

    Args:
        value: A surface form or a feature value.

    Returns:
        str: The quoted literal.

    Raises:
        ValueError: If *value* holds both a single and a double quote.

    """
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    message = (
        f"La forme {value!r} contient les deux types de guillemets : "
        f"le lecteur de grammaire NLTK n'a pas d'échappement."
    )
    raise ValueError(message)


class LexicalGrammarExporter:
    """Build NLTK lexical rule strings from realized forms.

    The terminal of a production is the surface form itself, so a spelling
    shared by several paradigm cells yields several productions and the chart
    parser resolves the ambiguity on its own.
    """

    def export_lexicon(self, lexicon: RealizedLexicon, how: str) -> str:
        """Export every realized form for *how* (translation or validation)."""
        match how:
            case "translation":
                return self.export_translation(lexicon)
            case "validation":
                return self.export_validation(lexicon)
            case _:
                message = f"'{how}' is neither 'translation' nor 'validation'."
                raise ValueError(message)

    def export_translation(self, formes: Iterable[Forme]) -> str:
        """Return newline-joined translation lexical productions, deduplicated."""
        return self.__join(self.export_forme_translation(forme) for forme in formes)

    def export_validation(self, formes: Iterable[Forme]) -> str:
        """Return newline-joined validation lexical productions, deduplicated.

        Several source cells often realize the same destination form with the
        same features; once the terminal is that form, they are the very same
        production.
        """
        return self.__join(self.export_forme_validation(forme) for forme in formes)

    @staticmethod
    def __join(productions: Iterable[str]) -> str:
        """Join productions, keeping the first occurrence of each."""
        return "\n".join(dict.fromkeys(productions))

    def export_forme_translation(self, forme: Forme) -> str:
        """Return one translation production for *forme*."""
        infos = {f"D{k}": v for k, v in forme.destination.get_sigma().items()}
        infos["translation"] = forme.destination.to_string()
        return self.export_entry_with_infos(forme.source, infos)

    def export_forme_validation(self, forme: Forme) -> str:
        """Return one validation production for *forme*."""
        return self.export_entry(forme.destination)

    def export_entry(self, entry: FormeEntry) -> str:
        """Return a validation-style NLTK lexical production for *entry*."""
        sigma = {
            key: value for key, value in entry.get_sigma().items() if key.istitle()
        }
        return self.__production(entry, sigma)

    def export_entry_with_infos(self, entry: FormeEntry, infos: dict) -> str:
        """Return a translation-style NLTK lexical production for *entry*."""
        sigma = {
            f"S{key}": value
            for key, value in entry.get_sigma().items()
            if key.istitle()
        }
        sigma.update(infos)
        return self.__production(entry, sigma)

    @staticmethod
    def __production(entry: FormeEntry, sigma: dict) -> str:
        """Return ``POS[features] -> 'surface form'`` for *entry*."""
        features = ",".join(f"{key}={quote(value)}" for key, value in sigma.items())
        return f"{entry.pos}[{features}] -> {quote(entry.to_string())}"
