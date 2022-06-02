from frozendict import frozendict

from lexique.structures import Phonology


def is_123(t: str) -> bool: ...


def is_456(t: str) -> bool: ...


def is_789(t: str) -> bool: ...


def is_a(t: str) -> bool: ...


def is_u(t: str) -> bool: ...


def is_v(t: str) -> bool: ...


def verify(t: str, stem: frozendict, phonology: Phonology) -> str: ...


def apply(rule: str, stem: frozendict, phonology: Phonology) -> str: ...


def format_stem(stem: str, phonology: Phonology) -> frozendict: ...
