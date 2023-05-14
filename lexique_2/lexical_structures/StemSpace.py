from dataclasses import dataclass


@dataclass
class StemSpace:
    stems: tuple[str, ...]
