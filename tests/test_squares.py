"""Tests that need no word list and no network.

Runs under pytest, or on its own: ``python tests/test_squares.py``.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sator import (  # noqa: E402
    APPROVED_BONUS,
    APPROVED_MIN_SCORE,
    Square,
    WordIndex,
    default_words,
    load,
    search,
)

# A four-word list that admits exactly one double word square.
TINY = ["CAT", "OAR", "TEN", "COT", "AAE", "TRN"]


def test_index_matches():
    index = WordIndex(["CAT", "COT", "CUT", "BAT"])
    assert index.matches("C?T") == ("CAT", "COT", "CUT")
    assert index.matches("???") == ("BAT", "CAT", "COT", "CUT")
    assert index.matches("Z??") == ()
    assert "CAT" in index and "DOG" not in index


def test_scores_order_the_candidates():
    # Same four words, opposite orders: the score decides what is tried first.
    plain = WordIndex(["CAT", "COT", "CUT", "BAT"])
    scored = WordIndex(plain.words, {"CUT": 50, "COT": 40, "CAT": 30})
    assert plain.matches("C?T") == ("CAT", "COT", "CUT")
    assert scored.matches("C?T") == ("CUT", "COT", "CAT")
    # An unscored word sorts last, not first.
    assert scored.matches("???")[-1] == "BAT"


def test_search_takes_scored_pairs():
    scored = [(w, 1 if w == "CAT" else 0) for w in TINY]
    found = list(search(scored, order=3, limit=10))
    assert [s.rows for s in found] == [s.rows for s in search(TINY, order=3, limit=10)]


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


def _fake_wordlist():
    """A throwaway list + approved file, wired up through the env overrides."""
    tmp = Path(tempfile.mkdtemp())
    (tmp / "words.txt").write_text("CAT;50\nDOG;10\nEEL;50\nDOG;10\n")
    (tmp / "approved.json").write_text(json.dumps(["dog"]))
    os.environ["SATOR_WORDLIST"] = str(tmp / "words.txt")
    os.environ["SATOR_APPROVED"] = str(tmp / "approved.json")
    return tmp


def test_load_with_scores():
    tmp = _fake_wordlist()
    assert load(tmp / "words.txt") == ["CAT", "DOG", "EEL"]
    # Pairs come back best-first, and a repeated word appears once.
    assert load(tmp / "words.txt", with_scores=True) == [
        ("CAT", 50),
        ("EEL", 50),
        ("DOG", 10),
    ]
    assert load(tmp / "words.txt", min_score=50) == ["CAT", "EEL"]


def test_approval_beats_score():
    _fake_wordlist()
    # DOG is hand-approved and scores 10; CAT and EEL are unchecked, scoring 50.
    # The default keeps all three: nothing rejected, approvals in regardless,
    # unchecked words over the cut.
    assert default_words() == [("DOG", 10 + APPROVED_BONUS), ("CAT", 50), ("EEL", 50)]
    # The cut bites unchecked words only. DOG scores 10 and survives all of it.
    assert default_words(min_score=51) == [("DOG", 10 + APPROVED_BONUS)]
    assert default_words(min_score=0)[0][0] == "DOG", "approved words sort first"
    assert default_words(approved_only=True) == [("DOG", 10 + APPROVED_BONUS)]


def test_default_cut_comes_from_the_generator():
    # 25 is approvd_min_score in mattabate/wordlist's generate_scored_wordlist.py:
    # the bottom of the band it gives approved words.
    assert APPROVED_MIN_SCORE == 25
    _fake_wordlist()
    (Path(os.environ["SATOR_WORDLIST"])).write_text("CAT;24\nEEL;25\nDOG;10\n")
    assert [w for w, _ in default_words()] == ["DOG", "EEL"]


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
