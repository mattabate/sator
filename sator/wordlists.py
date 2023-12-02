"""Getting words in.

The default list is Matt's scored crossword word list, ~417,000 entries in
"crossword constructor" format (``WORD;score``, score 0-50), published at
https://github.com/mattabate/wordlist. It is downloaded once and cached, so
``sator ABATE`` works on a fresh checkout with nothing else installed.

Every word in it has one of three states, and the search treats each
differently:

* **rejected** -- 16,284 words thrown out by hand. They are not in the file at
  all: it is generated with ``WHERE status != 'rejected'``. Nothing you do to
  ``min_score`` can put one in a square.
* **approved** -- 31,343 words kept by hand. Always allowed, whatever they
  scored. A person already answered the question; a model's number does not
  get to overrule it.
* **unchecked** -- the other 386,327. Nobody has ruled on these, so the score
  decides, at :data:`APPROVED_MIN_SCORE` or above.

That is the whole rule: *not rejected, and either approved or good enough*.
It matters because the score is a machine's guess and the bands overlap --
the generator maps approvals to 25-50 and unchecked words to 0-50, so a score
cut alone is not a filter for quality. Approvals are handled separately, by
:data:`APPROVED_BONUS`: they sort ahead of every unchecked word regardless of
score, so the search tries them first and reaches for unchecked fill only
where nothing approved fits.

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

_RAW = "https://raw.githubusercontent.com/mattabate/wordlist/refs/heads/main/"
WORDLIST_URL = _RAW + "quickstart/matts_wordlist.txt"
APPROVED_URL = _RAW + "quickstart/sorted_words/approved.json"

#: Added to a hand-approved word's score. Larger than the 0-50 score range, so
#: every approved word outranks every unchecked one and gets tried first.
APPROVED_BONUS = 100

#: Default floor for unchecked words. This is ``approvd_min_score`` from
#: mattabate/wordlist's own ``scripts/generate_scored_wordlist.py`` -- the
#: bottom of the band it gives hand-approved words. So an unchecked word has to
#: score at least as high as the *lowest* an approved word can score to get in.
APPROVED_MIN_SCORE = 25

__all__ = [
    "APPROVED_BONUS",
    "APPROVED_MIN_SCORE",
    "APPROVED_URL",
    "WORDLIST_URL",
    "approved_words",
    "cache_path",
    "default_words",
    "download",
    "load",
]


def cache_path() -> Path:
    """Where the downloaded list lives. Override with ``SATOR_WORDLIST``."""
    override = os.environ.get("SATOR_WORDLIST")
    if override:
        return Path(override).expanduser()
    root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return root / "sator" / "matts_wordlist.txt"


def approved_path() -> Path:
    """Where the approved-word list lives. Override with ``SATOR_APPROVED``."""
    override = os.environ.get("SATOR_APPROVED")
    if override:
        return Path(override).expanduser()
    return cache_path().parent / "approved.json"


def download(dest: Path | None = None, url: str = WORDLIST_URL) -> Path:
    """Fetch a word list to ``dest`` (default: the cache path)."""
    dest = Path(dest) if dest else cache_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as response:
        payload = response.read()
    dest.write_bytes(payload)
    return dest


def _fetched(path: Path, url: str) -> Path:
    if not path.exists():
        print(f"sator: fetching {url}\n       -> {path}")
        download(path, url)
    return path


def approved_words() -> set[str]:
    """The hand-approved words, downloading them on first use."""
    path = _fetched(approved_path(), APPROVED_URL)
    raw = json.loads(path.read_text())
    return {str(w).replace(" ", "").upper() for w in raw}


def default_words(
    min_score: int = APPROVED_MIN_SCORE,
    length: int | None = None,
    approved_only: bool = False,
) -> list[tuple[str, int]]:
    """The default list as ``(word, score)`` pairs, downloading on first use.

    Nothing rejected (it is not in the file), every approved word, and the
    unchecked ones scoring ``min_score`` or better.

    ``min_score`` applies to unchecked words **only**. The score is a model's
    guess and approval is a person's answer, so no cut can throw away a word
    that was approved by hand. Approved words carry :data:`APPROVED_BONUS`, so
    handing the result straight to :func:`sator.search` tries them first.

    ``approved_only=True`` narrows to the hand-kept words and nothing else.
    """
    scored = load(
        _fetched(cache_path(), WORDLIST_URL),
        length=length,
        with_scores=True,
    )
    approved = approved_words()
    kept = [(w, s + APPROVED_BONUS) for w, s in scored if w in approved]
    if not approved_only:
        kept += [(w, s) for w, s in scored if w not in approved and s >= min_score]
    return sorted(kept, key=lambda kv: (-kv[1], kv[0]))


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
    with_scores: bool = False,
):
    """Read a word list.

    :param source: a ``.txt`` file, a ``.json`` file, or a directory of ``.txt``.
    :param length: keep only words of this length. ``None`` keeps everything.
    :param min_score: for scored lists, drop anything below this. Unscored
        words count as 50. On Matt's list this is a confidence filter, not a
        quality one -- see the module docstring before reaching for it.
    :param with_scores: return ``(word, score)`` pairs instead of words, so the
        search can try the better words first.
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

    best: dict[str, int] = {}
    for word, score in scored:
        if score < min_score or (length is not None and len(word) != length):
            continue
        best[word] = max(score, best.get(word, score))

    if with_scores:
        return sorted(best.items(), key=lambda kv: (-kv[1], kv[0]))
    return sorted(best)
