# Worked examples

Every grid below came out of `sator` itself, on the default word list.
The command above each block reproduces it.

## Seeded with ABATE

The one Matt asked for. ABATE goes in the top row; everything else is the search's doing. Every other word here is one he approved by hand.

```console
$ sator ABATE -c 3
7,418 words of length 5 (3,875 hand-approved, tried first), seeded with ABATE in row 1

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

Found in 0.35s.

## The seed does not have to be on top

`-r 3` puts ABATE in the third row.

```console
$ sator ABATE -c 2 -r 3
7,418 words of length 5 (3,875 hand-approved, tried first), seeded with ABATE in row 3

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

Found in 0.28s.

## Seeded with a name

A seed does not have to be a word -- if it is not in the list, it is added for the duration of the search.

```console
$ sator MATT -c 3
4,266 words of length 4 (3,037 hand-approved, tried first), seeded with MATT in row 1

M A T T
A B A R
C A G E
S A S K

M A T T
A B A R
C A G E
S A S S

M A T T
I S A W
C A G E
A P S E
```

Found in 0.25s.

## SATOR-shaped squares

`--symmetric` keeps only the grids that read the same down as across, so each of the four words appears twice.

```console
$ sator --symmetric -n 4 -c 3
4,266 words of length 4 (3,037 hand-approved, tried first)

A C T S
C A L L
T L D R
S L R S

A C T S
C I A O
T A G S
S O S A

A C T S
C I A O
T A G S
S O S O
```

Found in 0.26s.

## Hand-approved words and nothing else

`--approved-only` drops every unchecked word however well it scored, so all ten entries are ones Matt kept by hand.

```console
$ sator ABATE -c 2 --approved-only
3,875 hand-approved words of length 5, seeded with ABATE in row 1

A B A T E
L I T U P
I N A N E
A G R E E
R O I D S

A B A T E
P I T A S
G N A R S
A G R E E
R O I D S
```

Found in 0.29s.

## Letting every unchecked word in

`-s 0` drops the score floor, so the search can reach the 386,327 entries nobody has ruled on. Approved words are still tried first, but the corners they cannot fill are where `NEEDA` and `INONA` get in.

```console
$ sator ABATE -c 2 -s 0
11,083 words of length 5 (3,875 hand-approved, tried first), seeded with ABATE in row 1

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

Found in 0.29s.
