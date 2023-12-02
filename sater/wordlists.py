"""Getting words in.

The default list is Matt's scored crossword word list, ~413,000 entries in
"crossword constructor" format (``WORD;score``, score 0-50), published at
https://github.com/mattabate/wordlist. It is downloaded once and cached, so
``sater ABATE`` works on a fresh checkout with nothing else installed.

Any other list works too: pass a ``.txt`` (one word per line, with or without
``;score``), a ``.json`` (a list of words, or a list of ``[word, score]``
pairs), or a directory of ``.txt`` files -- which is the shape the English Open
Word List ships in.
"""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Iterable

WORDLIST_URL = (
    "https://raw.githubusercontent.com/mattabate/wordlist/"
    "refs/heads/main/quickstart/matts_wordlist.txt"
)

__all__ = ["WORDLIST_URL", "cache_path", "download", "default_words", "load"]


def cache_path() -> Path:
    """Where the downloaded list lives. Override with ``SATER_WORDLIST``."""
    override = os.environ.get("SATER_WORDLIST")
    if override:
        return Path(override).expanduser()
    root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return root / "sater" / "matts_wordlist.txt"


def download(dest: Path | None = None, url: str = WORDLIST_URL) -> Path:
    """Fetch the word list to ``dest`` (default: the cache path)."""
    dest = Path(dest) if dest else cache_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as response:
        payload = response.read()
    dest.write_bytes(payload)
    return dest


def default_words(min_score: int = 50) -> list[str]:
    """The default list, downloading it on first use."""
    path = cache_path()
    if not path.exists():
        print(f"sater: fetching {WORDLIST_URL}\n       -> {path}")
        download(path)
    return load(path, min_score=min_score)


def _parse_line(line: str) -> tuple[str, int] | None:
    line = line.strip()
    if not line:
        return None
    word, _, score = line.partition(";")
    word = word.replace(" ", "").upper()
    if not word.isalpha():
        return None
    try:
        return word, int(score)
    except ValueError:
        return word, 50


def load(
    source: str | Path,
    length: int | None = None,
    min_score: int = 0,
) -> list[str]:
    """Read a word list.

    :param source: a ``.txt`` file, a ``.json`` file, or a directory of ``.txt``.
    :param length: keep only words of this length. ``None`` keeps everything.
    :param min_score: for scored lists, drop anything below this. Unscored
        words count as 50. Matt's list tops out at 50, which is roughly "a
        word I would actually put in a puzzle".
    """
    path = Path(source).expanduser()
    scored: list[tuple[str, int]] = []

    if path.is_dir():
        files: Iterable[Path] = sorted(path.rglob("*.txt"))
    else:
        files = [path]

    for f in files:
        if f.suffix == ".json":
            raw = json.loads(f.read_text())
            for item in raw:
                if isinstance(item, (list, tuple)):
                    word, score = item[0], int(item[1])
                else:
                    word, score = str(item), 50
                word = word.replace(" ", "").upper()
                if word.isalpha():
                    scored.append((word, score))
        else:
            for line in f.read_text(errors="ignore").splitlines():
                parsed = _parse_line(line)
                if parsed:
                    scored.append(parsed)

    words = {
        word
        for word, score in scored
        if score >= min_score and (length is None or len(word) == length)
    }
    return sorted(words)
