"""Builders for :class:`FormeEntry` at the lexique.forme public boundary."""

from frozendict import frozendict

from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.utils.stem_space import StemSpace


def make_forme_entry(
    pos: str,
    stems: tuple[str, ...],
    sigma: dict[str, str],
) -> FormeEntry:
    """Build a :class:`FormeEntry` whose surface form is the first stem.

    Args:
        pos: Part of speech tag.
        stems: Stem variants; the first is the lemma / surface default.
        sigma: Feature bundle for the form.

    Returns:
        FormeEntry: Entry with a radical-only morpheme structure.

    """
    return FormeEntry(
        pos=pos,
        morphemes=Morphemes(
            radical=Radical(
                stems=StemSpace(stems=stems),
                sigma=frozendict(sigma),
            ),
            others=[],
        ),
        sigma=frozendict(sigma),
    )
