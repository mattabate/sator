# Worked examples

Every grid below came out of `sator` itself, on the default word list.
The command above each block reproduces it.

## Seeded with ABATE

The one Matt asked for. ABATE goes in the top row; everything else is the search's doing. Every other word here is one he approved by hand.

```console
$ sator ABATE -c 3
7,372 words of length 5 (4,165 hand-approved, tried first), seeded with ABATE in row 1

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

Found in 0.10s.

## The seed does not have to be on top

`-r 3` puts ABATE in the third row.

```console
$ sator ABATE -c 2 -r 3
7,372 words of length 5 (4,165 hand-approved, tried first), seeded with ABATE in row 3

I C A N T
T U T O R
A B A T E
G A L E N
O N L S D

I C A N T
T U M O R
A B A T E
L A S T A
O N S E T
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
4,165 hand-approved words of length 5, seeded with ABATE in row 1

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
10,614 words of length 5 (4,165 hand-approved, tried first), seeded with ABATE in row 1

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
