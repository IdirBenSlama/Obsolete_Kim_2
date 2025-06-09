"""Simple in-memory embedding cache."""

from typing import Any, Dict


class _EmbedCache:
    """Basic cache keyed by language then text."""

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, lang: str, text: str):
        """Retrieve cached vector for language/text pair, if present."""
        return self._store.get(lang, {}).get(text)

    def set(self, lang: str, text: str, vec: Any) -> None:
        """Store vector for language/text pair."""
        self._store.setdefault(lang, {})[text] = vec


embed_cache = _EmbedCache()
