"""Implementation of a Trie."""

from collections.abc import Callable

_special_chars_map = {i: "\\" + chr(i) for i in b"()[]{}?*+-|^$\\.&~#\t\n\r\v\f"}

# type_memory = dict[str, "type_memory | Literal[1] | str"]


def identity[T](param: T) -> T:
    """Identity function: returns its argument unchanged."""
    return param


def __escape(pattern: str) -> str:
    """Escape regex special characters (and a few others) in the pattern."""
    return pattern.translate(_special_chars_map)


def add_word(memory: dict, word: str) -> None:
    """Insert a word into the trie (in-place update of memory)."""
    ref = memory
    for char in word:
        ref = ref.setdefault(char, ref.get(char, {}))
    ref[""] = 1


def add_words(memory: dict, words: list[str]) -> None:
    """Insert a list of words into the trie."""
    for word in words:
        add_word(memory, word)


def __build_pattern(
    memory_data: dict,
    escape: Callable[[str], str] = identity,
) -> str | None:
    """Build a regular expression pattern from a dictionary.

    Args:
        memory_data: Mapping storing entries that have already been parsed (trie).
        escape: Function to escape characters; defaults to identity.

    Returns:
        str | None: Pattern string ready to compile, or None for empty single-node.

    """
    if not memory_data:
        return ""

    if "" in memory_data and len(memory_data) == 1:
        return None

    alternatives: list[str] = []
    characters: list[str] = []
    has_quantifier: bool = False

    for char, value in sorted(memory_data.items()):
        if isinstance(value, dict):
            dict_str = __build_pattern(value)
            match dict_str:
                case str():
                    alternatives.append(escape(char) + dict_str)
                case None:
                    characters.append(escape(char))
                case _:
                    raise ValueError
        else:
            has_quantifier = True

    is_characters_only = not alternatives

    if len(characters) > 0:
        alternatives.append(
            characters[0] if len(characters) == 1 else f"[{''.join(characters)}]",
        )

    result = (
        alternatives[0] if len(alternatives) == 1 else f"(?:{'|'.join(alternatives)})"
    )

    if has_quantifier:
        result = f"{result}?" if is_characters_only else f"(?:{result})?"

    return result


def dict2str(
    memory: dict,
    escape: Callable[[str], str] = identity,
) -> str | None:
    """Build a regex pattern from a prefix trie (escape applied to each character).

    Args:
        memory: Trie dict (from add_word/add_words).
        escape: Function to escape special chars; defaults to identity.

    Returns:
        str | None: Regex pattern string, or None for empty single-node trie.

    """
    return __build_pattern(memory, escape)


def to_pattern(words: list[str]) -> str:
    """Build a trie from a list of words and return a regex pattern that matches exactly those words.

    Args:
        words: List of words to convert into an optimized pattern.

    Returns:
        str: Regex pattern that matches exactly the words in the list (no more, no less).

    """
    memory = {}
    add_words(memory, words)
    dict_str = dict2str(memory)
    assert dict_str is not None
    return dict_str


__all__ = ["add_word", "add_words", "dict2str", "to_pattern"]
