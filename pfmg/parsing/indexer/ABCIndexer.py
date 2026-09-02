"""Abstract base for indexers that map token lists to index lists."""

from abc import ABC, abstractmethod

from pfmg.utils.abstract_factory import factory_method


class ABCindexer(ABC):
    """Abstract base for indexers: map tokens to list of index lists."""

    @abstractmethod
    def __call__(self, tokens: list[str]) -> list[list[str]]:
        """Map each token to a list of indices.

        Args:
            tokens: List of token strings.

        Returns:
            list[list[str]]: For each token, list of possible indices.

        """


def new_indexer(id_indexer: str, **kwargs) -> ABCindexer:
    """Factory to build an indexer by id (e.g. Desamb -> DesambIndexer).

    Args:
        id_indexer: Unique identifier of the indexer implementation.
        **kwargs: Arguments of the concrete indexer (e.g. ``lexicon`` and
            ``how`` for ``Desamb``, none for ``Identity``).

    Returns:
        ABCindexer: An indexer instance.

    Examples:
        >>> from pfmg.lexique.lexicon import Lexicon
        >>> from pfmg.utils.paths import get_project_path
        >>>
        >>> config_path = get_project_path() / "examples" / "data"
        >>> lexicon = Lexicon.from_yaml(config_path)
        >>> indexer = new_indexer("Desamb", lexicon=lexicon)
        >>> indexer(["le", "bruit"])
        [['36', '38', '40'], ['138']]
        >>> new_indexer("Identity")(["le", "bruit"])
        [['le'], ['bruit']]

    """
    assert __package__ is not None
    return factory_method(
        concrete_product=f"{id_indexer}Indexer",
        package=__package__,
        **kwargs,
    )
