"""sator -- search for double word squares.

    >>> from sator import search, default_words
    >>> next(search(default_words(), seed="ABATE")).render()

See :mod:`sator.squares` for the search and :mod:`sator.wordlists` for
getting words in.
"""

from .squares import BLANK, Square, WordIndex, search
from .wordlists import (
    APPROVED_BONUS,
    APPROVED_MIN_SCORE,
    APPROVED_URL,
    WORDLIST_URL,
    approved_words,
    default_words,
    download,
    load,
)

__version__ = "0.2.0"

__all__ = [
    "BLANK",
    "Square",
    "WordIndex",
    "search",
    "APPROVED_BONUS",
    "APPROVED_MIN_SCORE",
    "APPROVED_URL",
    "WORDLIST_URL",
    "approved_words",
    "default_words",
    "download",
    "load",
    "__version__",
]
