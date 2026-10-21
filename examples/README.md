# Worked examples

Every grid below came out of `sator` itself, on the default word list.
The command above each block reproduces it.

## Plain English only

Matt, on a square of approved words: 'the words in this one are fine, like acceptable, but together they are bad'. Approval is a crossword judgment and admits names, phrases and crosswordese; `--also-in` keeps only the words a dictionary lists as plain lowercase headwords, so every one of these ten is a word you would say.

```console
$ sator SCARE -c 1 --approved-only --also-in /usr/share/dict/words
1,573 hand-approved words of length 5 also in /usr/share/dict/words, seeded with SCARE in row 1

S C A R E
T A L O N
A B O U T
G A U G E
E L D E R
```

Found in 0.15s.

## Plain English, no seed

The same pool, 1,573 words, searched freely.

```console
$ sator -n 5 -c 3 --approved-only --also-in /usr/share/dict/words
1,573 hand-approved words of length 5 also in /usr/share/dict/words

S T A G E
T A L O N
A B B O T
L O U S E
L O S E R

S T A G E
C A B A L
A L O U D
R O U G E
E N T E R

C A T C H
A N I L E
U N B I D
S U I N G
E L A T E
```

Found in 1.33s.

## Seeded with ABATE

The one Matt asked for. ABATE goes in the top row; everything else is the search's doing. Every other word here is one he approved by hand.

```console
$ sator ABATE -c 3
7,367 words of length 5 (4,160 hand-approved, tried first), seeded with ABATE in row 1

A B A T E
S Y R I A
A T I L T
N E E D A
A S S E T

A B A T E
K E S H A
I S Y E T
T O N G A
A S C O T

A B A T E
L U C I A
O C T E T
A K I T A
D O N O T
```

Found in 0.11s.

## The seed does not have to be on top

`-r 3` puts ABATE in the third row.

```console
$ sator ABATE -c 2 -r 3
7,367 words of length 5 (4,160 hand-approved, tried first), seeded with ABATE in row 3

S C O U T
H U M P H
A B A T E
N A N O S
K N I N E

S C O U T
H U M P H
A B A T E
M A N O R
S N I P E
```

Found in 0.09s.

## Seeded with a name

A seed does not have to be a word -- if it is not in the list, it is added for the duration of the search.

```console
$ sator MATT -c 3
4,188 words of length 4 (3,707 hand-approved, tried first), seeded with MATT in row 1

M A T T
A P R A
K E E P
E X E S

M A T T
A R I A
K E E P
E A R S

M A T T
A S I A
K E E P
E A R S
```

Found in 0.08s.

## SATOR-shaped squares

`--symmetric` keeps only the grids that read the same down as across, so each of the four words appears twice.

```console
$ sator --symmetric -n 4 -c 3
4,188 words of length 4 (3,707 hand-approved, tried first)

A C T S
C A L L
T L D R
S L R S

A C T S
C E L L
T L D R
S L R S

A C T S
C I A O
T A G S
S O S A
```

Found in 0.08s.

## Hand-approved words and nothing else

`--approved-only` drops every unchecked word however well it scored, so all ten entries are ones Matt kept by hand.

```console
$ sator ABATE -c 2 --approved-only
4,160 hand-approved words of length 5, seeded with ABATE in row 1

A B A T E
P I T A S
G N A R S
A G R E E
R O I D S

A B A T E
V I S I T
I N F E R
A G A T E
S O R O S
```

Found in 0.10s.

## Letting every unchecked word in

`-s 0` drops the score floor, so the search can reach the 375,398 entries nobody has ruled on. Approved words are still tried first, but the corners they cannot fill are where `INONA` gets in.

```console
$ sator ABATE -c 2 -s 0
10,609 words of length 5 (4,160 hand-approved, tried first), seeded with ABATE in row 1

A B A T E
S Y R I A
A T I L T
N E E D A
A S S E T

A B A T E
S Y R I A
F R E E T
I N O N A
T E N E T
```

Found in 0.09s.
