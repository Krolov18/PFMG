"""Feature structures for grammar RHS (list of feature dicts per phrase)."""

from dataclasses import dataclass

from pfmg.parsing.features.FeatureMixin import FeatureMixin
from pfmg.parsing.features.utils import FeatureReader


@dataclass
class Features(FeatureMixin):
    """List of feature dicts, one per RHS phrase (agreement features).

    Attributes:
        data: List of feature dicts (one per RHS phrase).

    """

    data: list[dict]

    def __setitem__(self, key: int, value: dict) -> None:
        """Set the feature dict at index key.

        Args:
            key: Index in the feature list.
            value: Feature dict to store.

        """
        self.data[key] = value

    def __getitem__(self, item: int) -> dict:
        """Get the feature dict at index item.

        Args:
            item: Index in the feature list.

        Returns:
            dict: Feature dict at that index.

        """
        return self.data[item]

    @classmethod
    def from_string(cls, data: str, target: str, phrase_len: int) -> Features:
        """Build Features from a string (broadcast and parse).

        Args:
            data: Feature specification string.
            target: Prefix for feature names (e.g. "S" or "D").
            phrase_len: Number of phrases (for broadcast).

        Returns:
            Features: New Features instance.

        """
        data = Features.broadcast(data, phrase_len)
        return cls(data=FeatureReader().parse(data=data, target=target))

    def to_nltk(self) -> list[str]:
        """Return NLTK-style feature strings (key=value, comma-separated) for each phrase.

        Returns:
            list[str]: One string per phrase.

        """
        result: list[str] = []

        for i_x in self.data:
            result.append(",".join([f"{key}={value}" for key, value in i_x.items()]))

        return result

    def add_translation(self, translations: list[str]) -> None:
        """Add 'translation' fields to each RHS part.

        Args:
            translations: Translation indices per phrase (same length as data).

        """
        assert len(translations) == len(self.data)
        for i in range(len(translations)):
            self.data[i]["translation"] = f"?{translations[i]}{i}"

    def get_translations(self) -> tuple[str, ...]:
        """Return the translation field from each feature dict.

        Returns:
            tuple[str, ...]: Translation value per phrase.

        """
        return tuple(x["translation"] for x in self.data)
