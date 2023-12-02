import threading
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import random
import string

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


# This function generates words by changing one letter of the input word
def generate_similar_words(word: str) -> List[str]:
    similar_words = []
    for i in range(len(word)):
        for char in string.ascii_lowercase:
            if char != word[i]:
                new_word = word[:i] + char + word[i + 1 :]
                similar_words.append(new_word)
    random.shuffle(similar_words)
    return similar_words


@app.websocket("/ws/words")
async def websocket_endpoint(websocket: WebSocket):
    print("Connected")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if len(data) == 5 and data.isalpha():
            similar_words = generate_similar_words(data.lower())
            for word in similar_words:
                await websocket.send_text(word)
        else:
            await websocket.send_text("Invalid input")
