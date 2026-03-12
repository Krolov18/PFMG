def _ensure_nltk_data() -> None:
    """Download required NLTK data if missing (e.g. wordnet for parsing)."""
    import nltk

    for resource in ("wordnet",):
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)


_ensure_nltk_data()
