"""Tests that need no word list and no network.

Runs under pytest, or on its own: ``python tests/test_squares.py``.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sater import Square, WordIndex, search  # noqa: E402

# A four-word list that admits exactly one double word square.
TINY = ["CAT", "OAR", "TEN", "COT", "AAE", "TRN"]


def test_index_matches():
    index = WordIndex(["CAT", "COT", "CUT", "BAT"])
    assert index.matches("C?T") == ("CAT", "COT", "CUT")
    assert index.matches("???") == ("BAT", "CAT", "COT", "CUT")
    assert index.matches("Z??") == ()
    assert "CAT" in index and "DOG" not in index


def test_index_rejects_mixed_lengths():
    try:
        WordIndex(["CAT", "HORSE"])
    except ValueError:
        return
    raise AssertionError("expected ValueError on mixed lengths")


def test_square_properties():
    square = Square(("CAT", "OAR", "TEN"))
    assert square.order == 3
    assert square.cols == ("COT", "AAE", "TRN")
    assert len(square.words) == 6
    assert not square.symmetric
    assert square.render() == "C A T\nO A R\nT E N"
    assert Square(("AB", "BA")).symmetric


def test_finds_the_known_square():
    found = list(search(TINY, order=3, limit=10))
    assert found, "expected at least one square"
    assert ("CAT", "OAR", "TEN") in [s.rows for s in found]


def test_every_result_is_really_a_square():
    words = set(TINY)
    for square in search(TINY, order=3, limit=10):
        for word in square.words:
            assert word in words, f"{word} is not in the list"


def test_distinct_flag():
    # SATOR-like squares repeat words; distinct=True must exclude them.
    palindromic = ["AB", "BA"]
    assert list(search(palindromic, order=2, distinct=True)) == []
    assert list(search(palindromic, order=2, distinct=False))


def test_symmetric_only_yields_symmetric():
    words = ["ABCS", "BAIL", "CIAO", "SLOG", "ABCD"]
    found = list(search(words, order=4, symmetric=True, limit=5))
    assert found, "expected the ABCS/BAIL/CIAO/SLOG square"
    for square in found:
        assert square.symmetric
        assert square.rows == square.cols


def test_seed_is_placed_and_kept():
    for square in search(TINY, seed="OAR", row=2, limit=3):
        assert square.rows[1] == "OAR"


def test_seed_not_in_list_still_works():
    for square in search(TINY, seed="cat", row=1, limit=1):
        assert square.rows[0] == "CAT"
        break


def test_limit_is_respected():
    assert len(list(search(TINY, order=3, limit=1))) <= 1


def test_bad_seed_row():
    try:
        next(search(TINY, seed="CAT", row=9))
    except ValueError:
        return
    raise AssertionError("expected ValueError on an out-of-range row")


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok   {name}")
            except Exception as exc:  # noqa: BLE001
                failures += 1
                print(f"  FAIL {name}: {exc}")
    print(f"\n{failures} failure(s)")
    sys.exit(1 if failures else 0)
