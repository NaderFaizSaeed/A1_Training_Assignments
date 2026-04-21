from fastapi import FastAPI
import json
import random


app = FastAPI()


def load_data():
    with open("processed_data/quotes.json", "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/quotes")
def get_quotes():
    return load_data()


@app.get("/quotes/random")
def get_random_quote():
    data = load_data()
    return random.choice(data)