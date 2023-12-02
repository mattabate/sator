# Worked examples

Every grid below came out of `sater` itself, on the default word list.
The command above each block reproduces it.

## Seeded with ABATE

The one Matt asked for. ABATE goes in the top row; everything else is the search's doing.

```console
$ sater ABATE -c 3
3,258 words of length 5, seeded with ABATE in row 1

A B A T E
C A M E L
T R E A D
S E N S E
O R D E R

A B A T E
C A M E L
T R E N D
S E N S E
O R D E R

A B A T E
R I S E N
I S B A D
S O A M I
E N D O N
```

- across: ABATE, CAMEL, TREAD, SENSE, ORDER — down: ACTSO, BARER, AMEND, TEASE, ELDER
- across: ABATE, CAMEL, TREND, SENSE, ORDER — down: ACTSO, BARER, AMEND, TENSE, ELDER
- across: ABATE, RISEN, ISBAD, SOAMI, ENDON — down: ARISE, BISON, ASBAD, TEAMO, ENDIN

Found in 0.95s.

## The seed does not have to be on top

`-r 3` puts ABATE in the third row.

```console
$ sater ABATE -c 2 -r 3
3,258 words of length 5, seeded with ABATE in row 3

S C A N S
N O W O N
A B A T E
P R I M E
E A T E R

A C T I I
B U R N T
A B A T E
F I D E L
T C E L L
```

- across: SCANS, NOWON, ABATE, PRIME, EATER — down: SNAPE, COBRA, AWAIT, NOTME, SNEER
- across: ACTII, BURNT, ABATE, FIDEL, TCELL — down: ABAFT, CUBIC, TRADE, INTEL, ITELL

Found in 0.32s.

## Seeded with a name

A seed does not have to be a word -- if it is not in the list, it is added for the duration of the search.

```console
$ sater MATT -c 3
1,731 words of length 4, seeded with MATT in row 1

M A T T
I C E R
M I L E
I D L E

M A T T
I C E R
N I L E
I D L E

M A T T
A F A R
Y A L E
O N L Y
```

- across: MATT, ICER, MILE, IDLE — down: MIMI, ACID, TELL, TREE
- across: MATT, ICER, NILE, IDLE — down: MINI, ACID, TELL, TREE
- across: MATT, AFAR, YALE, ONLY — down: MAYO, AFAN, TALL, TREY

Found in 0.02s.

## SATOR-shaped squares

`--symmetric` keeps only the grids that read the same down as across, so each of the four words appears twice.

```console
$ sater --symmetric -n 4 -c 3
1,731 words of length 4

A B C S
B A C K
C C N Y
S K Y S

A B C S
B A I L
C I A O
S L O G

A B C S
B A I L
C I A O
S L O T
```

- across: ABCS, BACK, CCNY, SKYS — down: ABCS, BACK, CCNY, SKYS
- across: ABCS, BAIL, CIAO, SLOG — down: ABCS, BAIL, CIAO, SLOG
- across: ABCS, BAIL, CIAO, SLOT — down: ABCS, BAIL, CIAO, SLOT

Found in 0.00s.

## Turning the quality dial down

`-s 0` accepts every entry in the list, including crossword fill like `ASADA` and `BIGIF`. More squares, worse words.

```console
$ sater ABATE -c 2 -s 0
11,083 words of length 5, seeded with ABATE in row 1

A B A T E
S A M O A
A C I N G
D O D G E
A N E A R

A B A T E
R A B I A
A C I N G
G O R G E
E N D E R
```

- across: ABATE, SAMOA, ACING, DODGE, ANEAR — down: ASADA, BACON, AMIDE, TONGA, EAGER
- across: ABATE, RABIA, ACING, GORGE, ENDER — down: ARAGE, BACON, ABIRD, TINGE, EAGER

Found in 0.03s.
