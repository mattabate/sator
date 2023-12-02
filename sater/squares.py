"""Search for double word squares.

A *double word square* of order N is an N x N grid where all N rows and all N
columns read as words. The famous SATOR square is order 5::

    S A T O R
    A R E P O
    T E N E T
    O P E R A
    R O T A S

Rows and columns spell the same five words there, which makes it a *symmetric*
square. This module looks for the harder kind by default: squares whose 2N
words are all different from one another (``distinct=True``).

The search is a depth-first fill with a most-constrained-first heuristic. At
every step it looks at each unfinished row and column, counts how many words
still fit, and commits to the line with the fewest options -- so a hopeless
branch dies at the top of the tree instead of at the bottom. Candidate lookups
go through :class:`WordIndex`, which pre-buckets the word list by (position,
letter) and caches every pattern it has already answered.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence

BLANK = "?"

__all__ = ["BLANK", "Square", "WordIndex", "search"]


@dataclass(frozen=True)
class Square:
    """A finished grid. ``rows`` are top to bottom, ``cols`` left to right."""

    rows: tuple[str, ...]

    @property
    def order(self) -> int:
        return len(self.rows)

    @property
    def cols(self) -> tuple[str, ...]:
        return tuple("".join(row[i] for row in self.rows) for i in range(self.order))

    @property
    def words(self) -> tuple[str, ...]:
        """All 2N words, rows first."""
        return self.rows + self.cols

    @property
    def symmetric(self) -> bool:
        """True when the square reads the same down as across, like SATOR."""
        return self.rows == self.cols

    def render(self, sep: str = " ") -> str:
        """The grid as text, one row per line."""
        return "\n".join(sep.join(row) for row in self.rows)

    def __str__(self) -> str:
        return self.render()


class WordIndex:
    """A word list of one fixed length, queryable by pattern.

    ``index.matches("?BAT?")`` returns every word with B, A, T in positions
    2-4. Patterns repeat constantly during a depth-first search, so results are
    memoised; on a 30,000 word list the cache is what makes order 5 tractable.
    """

    def __init__(self, words: Iterable[str]) -> None:
        self.words: tuple[str, ...] = tuple(sorted({w for w in words if w}))
        lengths = {len(w) for w in self.words}
        if len(lengths) > 1:
            raise ValueError(f"mixed word lengths: {sorted(lengths)}")
        self.length: int = lengths.pop() if lengths else 0

        buckets: list[defaultdict[str, set[str]]] = [
            defaultdict(set) for _ in range(self.length)
        ]
        for word in self.words:
            for i, letter in enumerate(word):
                buckets[i][letter].add(word)
        self._by_pos = [{k: frozenset(v) for k, v in b.items()} for b in buckets]
        self._lookup = frozenset(self.words)
        self._cache: dict[str, tuple[str, ...]] = {}

    def __len__(self) -> int:
        return len(self.words)

    def __contains__(self, word: object) -> bool:
        return word in self._lookup

    def matches(self, pattern: str) -> tuple[str, ...]:
        """Every word fitting ``pattern``, where ``?`` is an unknown letter."""
        hit = self._cache.get(pattern)
        if hit is not None:
            return hit

        fixed = [(i, c) for i, c in enumerate(pattern) if c != BLANK]
        if not fixed:
            result = self.words
        else:
            # Intersect the smallest buckets first so the set shrinks fast.
            sets = sorted(
                (self._by_pos[i].get(c, frozenset()) for i, c in fixed), key=len
            )
            acc = sets[0]
            for s in sets[1:]:
                if not acc:
                    break
                acc = acc & s
            result = tuple(sorted(acc))

        self._cache[pattern] = result
        return result


def _column(grid: Sequence[str], j: int) -> str:
    return "".join(row[j] for row in grid)


def _set_row(grid: Sequence[str], i: int, word: str) -> list[str]:
    out = list(grid)
    out[i] = word
    return out


def _set_col(grid: Sequence[str], j: int, word: str) -> list[str]:
    return [row[:j] + word[i] + row[j + 1 :] for i, row in enumerate(grid)]


def _finished_words(grid: Sequence[str]) -> list[str]:
    out = [row for row in grid if BLANK not in row]
    for j in range(len(grid)):
        col = _column(grid, j)
        if BLANK not in col:
            out.append(col)
    return out


def _mirror_ok(grid: Sequence[str]) -> bool:
    """For a symmetric search: no filled cell may disagree with its mirror."""
    n = len(grid)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = grid[i][j], grid[j][i]
            if a != BLANK and b != BLANK and a != b:
                return False
    return True


def _still_valid(
    grid: Sequence[str], index: WordIndex, distinct: bool, symmetric: bool
) -> bool:
    """Reject a grid whose finished lines are not usable words.

    Filling one line can finish a crossing line by accident, and that
    accidental line is not guaranteed to be a word -- so it gets checked here
    rather than at the end, which is the whole point of pruning.
    """
    if symmetric and not _mirror_ok(grid):
        return False
    done = _finished_words(grid)
    for word in done:
        if word not in index:
            return False
    if distinct and len(set(done)) != len(done):
        return False
    return True


def _extend(
    grid: list[str], index: WordIndex, distinct: bool, symmetric: bool
) -> Iterator[Square]:
    best_count = None
    best_fill = None  # (is_row, position, candidates)

    for i, row in enumerate(grid):
        if BLANK not in row:
            continue
        cands = index.matches(row)
        if best_count is None or len(cands) < best_count:
            best_count, best_fill = len(cands), (True, i, cands)

    for j in range(len(grid)):
        col = _column(grid, j)
        if BLANK not in col:
            continue
        cands = index.matches(col)
        if best_count is None or len(cands) < best_count:
            best_count, best_fill = len(cands), (False, j, cands)

    if best_fill is None:
        yield Square(tuple(grid))
        return
    if best_count == 0:
        return

    is_row, pos, candidates = best_fill
    for word in candidates:
        nxt = _set_row(grid, pos, word) if is_row else _set_col(grid, pos, word)
        if not _still_valid(nxt, index, distinct, symmetric):
            continue
        yield from _extend(nxt, index, distinct, symmetric)


def search(
    words: Iterable[str],
    order: int | None = None,
    seed: str | None = None,
    row: int = 1,
    distinct: bool = True,
    symmetric: bool = False,
    limit: int | None = None,
) -> Iterator[Square]:
    """Yield double word squares, best-constrained-line-first.

    :param words: the word list. Only words of the target length are used.
    :param order: the size of the square. Defaults to ``len(seed)``.
    :param seed: a word to plant before searching, e.g. ``"ABATE"``. It is
        added to the word list if missing, so a name still works as a seed.
    :param row: which row the seed goes in, 1 = top.
    :param distinct: require all 2N words to differ. Set False to also allow
        squares where a word appears twice.
    :param symmetric: only SATOR-shaped squares, which read the same down as
        across. Implies ``distinct=False``, since every word then appears
        twice by construction.
    :param limit: stop after this many squares. ``None`` means keep going.

    Results arrive lazily, so ``next(search(...))`` is a cheap way to get one.
    """
    if symmetric:
        distinct = False
    if order is None:
        if seed is None:
            raise ValueError("pass order= or seed=")
        order = len(seed)

    pool = {w.strip().upper() for w in words}
    pool = {w for w in pool if len(w) == order and w.isalpha()}
    if seed is not None:
        seed = seed.strip().upper()
        if len(seed) != order:
            raise ValueError(f"seed {seed!r} is not {order} letters")
        pool.add(seed)

    index = WordIndex(pool)

    if seed is None:
        grid = [BLANK * order for _ in range(order)]
    else:
        if not 1 <= row <= order:
            raise ValueError(f"row must be 1..{order}, got {row}")
        grid = _set_row([BLANK * order] * order, row - 1, seed)

    found = 0
    for square in _extend(grid, index, distinct, symmetric):
        yield square
        found += 1
        if limit is not None and found >= limit:
            return
