"""sater -- search for double word squares.

    >>> from sater import search, default_words
    >>> next(search(default_words(), seed="ABATE")).render()

See :mod:`sater.squares` for the search and :mod:`sater.wordlists` for
getting words in.
"""

from .squares import BLANK, Square, WordIndex, search
from .wordlists import WORDLIST_URL, default_words, download, load

__version__ = "0.1.0"

__all__ = [
    "BLANK",
    "Square",
    "WordIndex",
    "search",
    "WORDLIST_URL",
    "default_words",
    "download",
    "load",
    "__version__",
]
