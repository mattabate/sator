import json
import tqdm
import enum

DICTIONARY: list[str] = []
ALL_WINS = []


def possibilities(template):
    """return all words that fit "?q??t"""
    possibilities = DICTIONARY
    for i, letter in enumerate(template):
        valid_words = []
        if letter == "?":
            continue
        for word in possibilities:
            if word[i] != letter:
                continue
            valid_words.append(word)
        possibilities = valid_words

    return possibilities


def get_new_templates(template):
    # get all possible words in every direction
    # for every row, get all possible words
    min_len_row = 10000000
    best_row_set = []
    best_row_index = None
    for i, row in enumerate(template):
        if "?" not in row:
            continue

        p = possibilities(row)
        if len(p) < min_len_row:
            min_len_row = len(p)
            best_row_set = p
            best_row_index = i

    min_len_col = 10000000
    best_col_set = []
    best_col_index = None
    for i, _ in enumerate(template):
        col = ""
        for row in template:
            col += row[i]

        if "?" not in col:
            continue

        p = possibilities(col)
        if len(p) < min_len_col:
            min_len_col = len(p)
            best_col_set = p
            best_col_index = i

    templates = []
    if min_len_row <= min_len_col:
        # create list of new templates
        for word in best_row_set:
            new_template = template.copy()
            new_template[best_row_index] = word
            templates.append(new_template)

    else:
        # create list of new templates
        for word in best_col_set:
            new_template = template.copy()
            for i, _ in enumerate(template):
                new_template[i] = (
                    new_template[i][:best_col_index]
                    + word[i]
                    + new_template[i][best_col_index + 1 :]
                )
            templates.append(new_template)

    return templates


def get_words_in_template(template):
    out = []
    for row in template:
        if "?" not in row:
            out.append(row)

    for i, _ in enumerate(template):
        col = ""
        for row in template:
            col += row[i]

        if "?" not in col:
            out.append(col)
    return out


def get_inital_templates(word: str):
    "Given a word, return all possible templates for the word."
    templates = []

    l = len(word)
    init_template = ["?" * l for _ in range(l)]

    for i in range(l):
        template = init_template.copy()
        template[i] = word
        if template not in templates:
            templates.append(template)

    return templates


def new_get_inital_templates(place: int, words: list[str]):
    "Given a word, return all possible templates for the word."
    templates = []

    l = len(words[1])
    init_template = ["?" * l for _ in range(l)]

    for word in words:
        template = init_template.copy()
        template[place - 1] = word
        if template not in templates:
            templates.append(template)

    return templates


def process_template(template, level):
    """return all words that fit "?q??t"""

    new_tamplates = get_new_templates(template)

    if level in [1, 2]:

        for template in tqdm.tqdm(new_tamplates):
            if level == 1:
                print("\n\n")
                for s in template:
                    print(s)

            gw = get_words_in_template(template)
            if not all([s in DICTIONARY for s in gw]):
                return False

            if len((set([s for s in get_words_in_template(template)]))) != len(
                get_words_in_template(template)
            ):
                return False

            if all(["?" not in t for t in template]):
                ALL_WINS.append(template)
                with open("wins.json", "w") as f:
                    json.dump(ALL_WINS, f, indent=4)

            process_template(template, level=level + 1)
    else:
        for template in new_tamplates:
            gw = get_words_in_template(template)
            if not all([s in DICTIONARY for s in gw]):
                return False

            if len((set([s for s in get_words_in_template(template)]))) != len(
                get_words_in_template(template)
            ):
                return False

            if all(["?" not in t for t in template]):
                ALL_WINS.append(template)
                with open("wins.json", "w") as f:
                    json.dump(ALL_WINS, f, indent=4)

            process_template(template, level=level + 1)

    return True


class Wordlist(enum.Enum):
    EOWL = "eowl"
    CROSSWORDS = "crosswords"


if __name__ == "__main__":
    print("starting")
    print("\n\n")
    f_wordlist = Wordlist.CROSSWORDS
    WORD = "CARROT"
    WORD = "STARSANDSTRIPES"

    all_words = []
    match f_wordlist:
        case Wordlist.EOWL:
            with open("eowl/eowl_words.json", "r") as f:
                all_words_lower = json.load(f)
                all_words = [w.upper() for w in all_words_lower]
        case Wordlist.CROSSWORDS:
            with open("crosswords/crossword_words.json", "r") as f:
                all_words_json = json.load(f)
                all_words = [w[0] for w in all_words_json]

    print(f"word: {WORD}")
    print(f"number of words: {len(all_words)}")
    print(f"dataset: {f_wordlist}")
    if WORD not in all_words and "?" not in WORD:
        all_words.append(WORD)

    DICTIONARY = [w for w in all_words if len(w) == len(WORD)]
    DICTIONARY = list(set(DICTIONARY))

    print(f"number {len(WORD)}-letter words: {len(DICTIONARY)}")
    print()
    templates = get_inital_templates(WORD)
    templates = new_get_inital_templates(14, DICTIONARY)

    level = 0

    print("\033[32m")
    for template in tqdm.tqdm(templates):
        print("\033[33m")
        for s in get_words_in_template(template):
            DICTIONARY.append(s)

        process_template(template, level + 1)
        print("\033[32m")
