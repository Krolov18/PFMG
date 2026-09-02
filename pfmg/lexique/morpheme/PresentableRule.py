"""Presentation boundary for morpheme rule classes."""

from pfmg.external.decoupeur.MixinDecoupeur import MixinDecoupeur
from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.equality.MixinEquality import MixinEquality
from pfmg.external.gloser.MixinGloser import MixinGloser
from pfmg.external.representor.MixinRepresentor import MixinRepresentor


class PresentableRule(
    MixinDisplay,
    MixinEquality,
    MixinRepresentor,
    MixinDecoupeur,
    MixinGloser,
):
    """Base for morpheme rules; presentation lives in external mixins."""
