# sater

Find **double word squares** — grids where every row *and* every column is a word.

```console
$ sater --symmetric -n 4
A B C S
B A I L
C I A O
S L O G
```

Across: `ABCS`, `BAIL`, `CIAO`, `SLOG`. Down: the same four. That one is
*symmetric*, like the Roman [SATOR
square](https://en.wikipedia.org/wiki/Sator_Square) this project is named for:

```
S A T O R
A R E P O
T E N E T
O P E R A
R O T A S
```

By default `sater` looks for the harder kind — squares whose 2N words are all
different from each other. `--symmetric` asks for the SATOR shape instead.

## Install

```bash
git clone https://github.com/mattabate/sater.git
cd sater
pip install -e .
```

Python 3.10 or newer. **No dependencies** — the whole thing is standard library.

## Use it

```console
$ sater ABATE -c 1
sater: fetching https://raw.githubusercontent.com/mattabate/wordlist/refs/heads/main/quickstart/matts_wordlist.txt
       -> ~/.cache/sater/matts_wordlist.txt
3,258 words of length 5, seeded with ABATE in row 1

A B A T E
C A M E L
T R E A D
S E N S E
O R D E R
```

The first run downloads a word list (see below) and caches it. After that it is
instant: that square came out of 3,258 candidate words in **0.04 seconds**.

More examples, all reproducible, are in [`examples/`](examples/README.md).

### Options

| Flag | What it does |
| --- | --- |
| `sater ABATE` | seed a square with a word |
| `-n, --order 5` | size of the square. Required if you give no seed |
| `-r, --row 3` | put the seed in row 3 instead of the top row |
| `-c, --count 10` | how many squares to find before stopping (default 5) |
| `-w, --words FILE` | use your own list — a `.txt`, a `.json`, or a directory of `.txt` |
| `-s, --min-score 40` | for scored lists, the lowest score to accept (0–50) |
| `--symmetric` | only SATOR-shaped squares, which read the same down as across |
| `--repeats` | allow a word to appear twice |
| `--json` | print JSON instead of grids |
| `--download` | refresh the cached word list and exit |

`--min-score` is the dial that matters. Crossword word lists contain entries
like `ACTSO` and `ANEGG` — legal fill, ugly squares. Raise the score and the
grids get cleaner and rarer:

| `--min-score` | 4-letter words | 5-letter words |
| --- | --- | --- |
| 0 | 5,465 | 11,083 |
| 30 | 3,565 | 6,049 |
| 40 | 1,731 | 3,258 |
| 50 | 136 | 284 |

## Use it as a library

```python
from sater import search, load

words = load("~/.cache/sater/matts_wordlist.txt", length=5, min_score=40)

for square in search(words, seed="ABATE", limit=3):
    print(square.render(), "\n")
    print(square.rows, square.cols, square.symmetric)
```

`search()` is a generator, so `next(search(words, seed="ABATE"))` stops as soon
as it has one. Nothing is written to disk and there are no module globals — you
can run several searches in the same process.

## How the search works

Depth-first fill with a most-constrained-line-first heuristic:

1. Look at every unfinished row and column and count how many words still fit.
2. Commit to the line with the **fewest** options. A hopeless branch therefore
   dies near the top of the tree instead of near the bottom.
3. Filling one line can accidentally finish a crossing line. Check those
   immediately: if the accident is not a word, or repeats a word already in the
   grid, drop the branch.
4. No blanks left? That is a square.

Candidate lookups go through `WordIndex`, which buckets the list by
`(position, letter)` and intersects the smallest buckets first. Every pattern
it answers is memoised, which is what makes order 5 finish in milliseconds
rather than minutes.

## Word lists

The default is [**mattabate/wordlist**](https://github.com/mattabate/wordlist) —
~413,000 entries scored 0–50 by a model trained on words I said yes and no to.
It is downloaded on first use to `~/.cache/sater/`, or wherever you point
`$SATER_WORDLIST`. It is published under CC BY-NC-SA 4.0.

Bring your own with `--words`:

- **`.txt`** — one word per line, either bare (`abate`) or scored (`ABATE;40`)
- **`.json`** — a list of words, or a list of `[word, score]` pairs
- **a directory** — every `.txt` under it, which is the shape the [English Open
  Word List](http://dreamsteep.com/projects/the-english-open-word-list.html)
  ships in

Words are upper-cased, spaces are stripped, anything non-alphabetic is dropped.

## Tests

```bash
python tests/test_squares.py     # or: pytest
```

Eleven tests, no network and no word list required.

## Credits

The search grew out of [mattabate/wordplay](https://github.com/mattabate/wordplay),
where it lived as a single `main.py`. Earlier versions leaned on [Chris Jones's
crossword word list](https://github.com/christophsjones/crossword-wordlist) and
the English Open Word List; this one reads whatever you give it and ships no
word data of its own.

MIT licensed — see [LICENSE](LICENSE). The word lists are not mine to relicense
and carry their own terms.
