import json


all_wins = []

with open("4_letter_words.json", "r") as f:
    wordle_words = json.load(f)
# with open("4_letter_words.json", "w") as f:
#     wordle_words = list(set(wordle_words))
#     json.dump(wordle_words, f, indent=4)


def possibilities(template):
    """return all words that fit "?q??t"""
    possibilities = wordle_words
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


def get_new_templates(template, valid_words):
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


def process_template(template, valid_words):
    """return all words that fit "?q??t"""

    new_tamplates = get_new_templates(template, valid_words)

    for template in new_tamplates:
        for s in template:
            print(" ".join(s))
        print("")
    for template in new_tamplates:
        gw = get_words_in_template(template)
        if not all([s in wordle_words for s in gw]):
            return False

        if len((set([s for s in get_words_in_template(template)]))) != len(
            get_words_in_template(template)
        ):
            return False

        if all(["?" not in t for t in template]):
            all_wins.append([" ".join(t) for t in template])
            with open("wins.json", "w") as f:
                json.dump(all_wins, f, indent=4)

        process_template(template, valid_words)

    return True


if __name__ == "__main__":
    WORD = "matt"
    # row template
    templates = []
    for i in range(4):
        template = [
            "????",
            "????",
            "????",
            "????",
        ]
        template[i] = WORD
        templates.append(template)

    # diagnol template
    template = []
    for i in range(4):
        row = ""
        for j in range(4):
            if j == i:
                row += WORD[j]
            else:
                row += "?"

        template.append(row)
    templates.append(template)

    # diagnol template
    template = []
    for i in range(4):
        row = ""
        for j in range(4):
            if j == 3 - i:
                row += WORD[j]
            else:
                row += "?"

        template.append(row)
    templates.append(template)

    for template in [templates[1], templates[4], templates[5]]:
        for s in get_words_in_template(template):
            wordle_words.append(s)

        process_template(template, wordle_words)

# if __name__ == "__main__":

#     template =[
#         "j????",
#         "?o???",
#         "??y??",
#         "???c?",
#         "????e"
#     ] # enter the template here as a list of strings

#     for s in get_words_in_template(template):
#         wordle_words.append(s)

#     process_template(template, wordle_words)
