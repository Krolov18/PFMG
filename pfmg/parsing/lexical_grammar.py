"""Export realized lexicon forms as NLTK lexical productions."""

from collections.abc import Iterable

from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.parsing.lexicon_index import RealizedLexicon


class LexicalGrammarExporter:
    """Build NLTK lexical rule strings from realized forms."""

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
        """Return newline-joined translation lexical productions."""
        return "\n".join(self.export_forme_translation(forme) for forme in formes)

    def export_validation(self, formes: Iterable[Forme]) -> str:
        """Return newline-joined validation lexical productions."""
        return "\n".join(self.export_forme_validation(forme) for forme in formes)

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
        features = ",".join(f"{key}='{value}'" for key, value in sigma.items())
        return f"{entry.pos}[{features}] -> '{entry.index}'"

    def export_entry_with_infos(self, entry: FormeEntry, infos: dict) -> str:
        """Return a translation-style NLTK lexical production for *entry*."""
        sigma = {
            f"S{key}": value
            for key, value in entry.get_sigma().items()
            if key.istitle()
        }
        sigma.update(infos)
        features = ",".join(f"{key}='{value}'" for key, value in sigma.items())
        return f"{entry.pos}[{features}] -> '{entry.index}'"
