# sator

Find **double word squares** — grids where every row *and* every column is a word.

```console
$ sator --symmetric -n 4 -c 2
4,266 words of length 4 (3,037 hand-approved, tried first)

A C T S
C A L L
T L D R
S L R S

A C T S
C I A O
T A G S
S O S A
```

Each of those reads the same down as across — the shape of the Roman [SATOR
square](https://en.wikipedia.org/wiki/Sator_Square) this project is named for:

```
S A T O R
A R E P O
T E N E T
O P E R A
R O T A S
```

By default `sator` looks for the harder kind — squares whose 2N words are all
different from each other. `--symmetric` asks for the SATOR shape instead.

## Install

```bash
git clone https://github.com/mattabate/sator.git
cd sator
pip install -e .
```

Python 3.10 or newer. **No dependencies** — the whole thing is standard library.

## Use it

```console
$ sator ABATE -c 1 --approved-only
sator: fetching https://raw.githubusercontent.com/mattabate/wordlist/refs/heads/main/quickstart/matts_wordlist.txt
       -> ~/.cache/sator/matts_wordlist.txt
3,875 hand-approved words of length 5, seeded with ABATE in row 1

A B A T E
L I T U P
I N A N E
A G R E E
R O I D S
```

Down: `ALIAR`, `BINGO`, `ATARI`, `TUNED`, `EPEES`. The first run downloads a
word list (see below) and caches it. After that it is instant: that square came
out of 3,875 candidate words in **0.03 seconds**.

More examples, all reproducible, are in [`examples/`](examples/README.md).

### Options

| Flag | What it does |
| --- | --- |
| `sator ABATE` | seed a square with a word |
| `-n, --order 5` | size of the square. Required if you give no seed |
| `-r, --row 3` | put the seed in row 3 instead of the top row |
| `-c, --count 10` | how many squares to find before stopping (default 5) |
| `-w, --words FILE` | use your own list — a `.txt`, a `.json`, or a directory of `.txt` |
| `-s, --min-score 40` | score an unchecked word needs to get in (0–50, default 25) |
| `--approved-only` | hand-approved words and nothing else |
| `--symmetric` | only SATOR-shaped squares, which read the same down as across |
| `--repeats` | allow a word to appear twice |
| `--json` | print JSON instead of grids |
| `--download` | refresh the cached word list and exit |

## The words are the whole game

A double word square is only as good as its word list, and any big list is
mostly words you would never put in a puzzle. The default list carries a human
answer to that. Every entry has one of three states:

| | words | what `sator` does with it |
| --- | --- | --- |
| **rejected** | 16,284 | never used — they are not even in the published file |
| **approved** | 31,343 | always used, whatever they scored |
| **unchecked** | 386,327 | used if they score `--min-score` or better |

That is the whole rule: **not rejected, and either approved or good enough.**
A person already answered the question for the first two; the model's number
only decides the third.

The default cut is **25**, which is not a taste of mine — it is
`approvd_min_score` from the word list's own
[`generate_scored_wordlist.py`](https://github.com/mattabate/wordlist), the
bottom of the band it gives hand-approved words. So an unchecked word has to
score at least as high as the *lowest* an approved word can score:

| `--min-score` | 3-letter | 4-letter | 5-letter | 6-letter |
| --- | --- | --- | --- | --- |
| 0 (everything) | 2,121 | 5,465 | 11,083 | 18,744 |
| **25 (default)** | **1,829** | **4,266** | **7,418** | **11,677** |
| 40 | 1,748 | 3,651 | 5,606 | 7,488 |
| `--approved-only` | 1,679 | 3,037 | 3,875 | 3,055 |

Two things follow that are easy to get wrong. **`--min-score` never touches an
approved word** — the score is a model's guess and approval is a person's
answer, so no cut can throw one away. And **`--min-score` is not a quality
dial**: the bands overlap almost completely, so an unchecked word can score 50,
and a cut of 40 on the raw list still leaves a pool that is only 46% approved.
If you want quality, use `--approved-only`; raising the score just makes the
search rarer, not better.

Approved words are always tried first, so the difference shows up in the
corners the approved list cannot reach.

## Use it as a library

```python
from sator import search, default_words

for square in search(default_words(length=5), seed="ABATE", limit=3):
    print(square.render(), "\n")
    print(square.rows, square.cols, square.symmetric)
```

`default_words()` returns `(word, score)` pairs, and `search()` takes either
those or plain words. With scores it tries the best words first, so the squares
that come out first are built from the words you like most — which is what
makes `-c 1` worth running.

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

Candidates are tried best-scored-first, so the answer you see first is the one
built from the best words rather than the one that happens to start with A.

Lookups go through `WordIndex`, which buckets the list by `(position, letter)`
and intersects the smallest buckets first. Every pattern it answers is
memoised, which is what makes order 5 finish in milliseconds rather than
minutes.

## Word lists

The default is [**mattabate/wordlist**](https://github.com/mattabate/wordlist) —
417,670 entries scored 0–50 by a model trained on the words I said yes and no
to, plus the approved/rejected lists themselves. `sator` downloads
`matts_wordlist.txt` and `approved.json` on first use to `~/.cache/sator/`, or
wherever you point `$SATOR_WORDLIST` and `$SATOR_APPROVED`. That repo is
published under CC BY-NC-SA 4.0.

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

Sixteen tests, no network and no word list required.

## Where this came from

This is an old project, cleaned up and published. It started on **2 December
2023** as a FastAPI backend with a Next.js front end — a website for drawing
word squares — and the search itself was rewritten through 2025 inside
[mattabate/wordplay](https://github.com/mattabate/wordplay), where it lived as a
single `main.py`.

In August 2026 the two copies were consolidated into this one, the web app was
dropped, and the history was flattened to a single root commit. That commit
keeps the original 2 December 2023 author date, so the repo still says when the
project is from. What is left is the part that was ever worth keeping: a
terminal program that reads a word list and builds squares out of it.

Earlier versions leaned on [Chris Jones's crossword word
list](https://github.com/christophsjones/crossword-wordlist) and the English
Open Word List; this one reads whatever you give it and ships no word data of
its own.

## License

MIT licensed — see [LICENSE](LICENSE). The word lists are not mine to relicense
and carry their own terms.
