import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lock = threading.Lock()
processing_active = True  # Global flag to control processing

all_wins = []

with open("words.json", "r") as f:
    wordle_words = json.load(f)

wordle_words = list(set(wordle_words))  # De-duplicate words
with open("words.json", "w") as f:
    json.dump(wordle_words, f, indent=4)


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


async def process_template(template, valid_words, websocket, processing_active):
    # Check if processing should continue
    if not processing_active:
        return False

    new_templates = get_new_templates(template)

    for template in new_templates:
        # Check again before processing the new template
        if not processing_active:
            return False

        gw = get_words_in_template(template)
        if not all([s in wordle_words for s in gw]):
            continue  # Skip to next template if current one doesn't meet criteria

        if len(set(gw)) != len(gw):
            continue  # Skip to next template if current one doesn't meet criteria

        if all(["?" not in t for t in template]):
            all_wins.append(template)
            await websocket.send_json({"win": template})
            with open("wins.json", "w") as f:
                json.dump(all_wins, f, indent=4)

        # Check before calling the recursive function
        if not processing_active:
            return False

        await process_template(template, valid_words, websocket, processing_active)

        # Check again after returning from recursive call
        if not processing_active:
            return False

    return True


async def my_func(WORD: str, websocket: WebSocket, processing_active):
    templates = [["?????" for _ in range(5)] for _ in range(7)]
    for i in range(5):
        templates[i][i] = WORD  # Set row template
        templates[5][i] = WORD[i] + "?" * i + "?" * (4 - i)  # Set diagonal template
        templates[6][i] = (
            "?" * (4 - i) + WORD[i] + "?" * i
        )  # Set reverse diagonal template

    for template in templates:
        for s in get_words_in_template(template):
            wordle_words.append(s)

        await process_template(template, wordle_words, websocket, processing_active)

    return all_wins


@app.websocket("/ws/words")
async def websocket_endpoint(websocket: WebSocket):
    global processing_active
    processing_active = True  # Reset flag to True at the start of the connection

    print("Connected")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "KILL":
                print("Kill command received, stopping...")
                processing_active = False  # Set flag to False to stop processing
                break
            elif len(data) == 5 and data.isalpha():
                await my_func(
                    WORD=data.lower(),
                    websocket=websocket,
                    processing_active=processing_active,
                )
            else:
                await websocket.send_text("Invalid input")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
