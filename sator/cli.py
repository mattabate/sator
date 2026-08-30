"""``sator`` on the command line."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from .squares import search
from .wordlists import (
    APPROVED_BONUS,
    APPROVED_MIN_SCORE,
    default_words,
    download,
    load,
)

__all__ = ["main"]


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sator",
        description="Find double word squares -- grids where every row and "
        "every column is a word.",
    )
    p.add_argument(
        "seed",
        nargs="?",
        help="a word to build around, e.g. ABATE. Omit to search freely, "
        "in which case --order is required.",
    )
    p.add_argument("-n", "--order", type=int, help="size of the square")
    p.add_argument(
        "-r", "--row", type=int, default=1, help="row for the seed, 1 = top"
    )
    p.add_argument(
        "-c", "--count", type=int, default=5, help="how many squares to find"
    )
    p.add_argument(
        "-w",
        "--words",
        type=Path,
        help="word list: a .txt, a .json, or a directory of .txt files. "
        "Defaults to Matt's list, downloaded on first use.",
    )
    p.add_argument(
        "-s",
        "--min-score",
        type=int,
        default=APPROVED_MIN_SCORE,
        help=f"score an unchecked word needs to get in, 0-50 (default "
        f"{APPROVED_MIN_SCORE}). Hand-approved words ignore it entirely -- they "
        f"are in whatever the model scored them.",
    )
    p.add_argument(
        "--approved-only",
        action="store_true",
        help="narrow to the hand-approved words and nothing else, dropping "
        "every unchecked word however well it scored.",
    )
    p.add_argument(
        "--repeats", action="store_true", help="allow a word to appear twice"
    )
    p.add_argument(
        "--symmetric",
        action="store_true",
        help="only SATOR-shaped squares, which read the same down as across",
    )
    p.add_argument("--json", action="store_true", help="print JSON, not grids")
    p.add_argument(
        "--download", action="store_true", help="refresh the cached word list and exit"
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.download:
        print(download())
        return 0

    if args.seed is None and args.order is None:
        print("sator: give a seed word or --order", file=sys.stderr)
        return 2

    order = args.order or len(args.seed)
    if args.words:
        words = load(
            args.words, length=order, min_score=args.min_score, with_scores=True
        )
        approved = 0
    else:
        words = default_words(
            min_score=args.min_score,
            length=order,
            approved_only=args.approved_only,
        )
        approved = sum(1 for _, s in words if s >= APPROVED_BONUS)

    if not words:
        print(f"sator: no {order}-letter words in that list", file=sys.stderr)
        return 1

    if args.approved_only:
        pool_note = f"{len(words):,} hand-approved words of length {order}"
    else:
        pool_note = f"{len(words):,} words of length {order}" + (
            f" ({approved:,} hand-approved, tried first)" if approved else ""
        )
    print(
        pool_note
        + (f", seeded with {args.seed.upper()} in row {args.row}" if args.seed else "")
    )

    started = time.time()
    found = []
    for square in search(
        words,
        order=order,
        seed=args.seed,
        row=args.row,
        distinct=not args.repeats,
        symmetric=args.symmetric,
        limit=args.count,
    ):
        found.append(square)
        if not args.json:
            print()
            print(square.render())

    if args.json:
        print(json.dumps([list(s.rows) for s in found], indent=2))

    print(f"\n{len(found)} square(s) in {time.time() - started:.1f}s", file=sys.stderr)
    if not found and not args.words and args.min_score > 0:
        print(
            f"sator: nothing at --min-score {args.min_score} -- lowering it "
            f"lets in more unchecked words",
            file=sys.stderr,
        )
    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())
