import json
import random

def random_quote():
    try:
        with open("data/quotes.json", "r") as file:
            quotes = json.load(file)
            selected_quote = random.choice(quotes)
        return f"-{selected_quote}-"
    except FileNotFoundError as e:
        print(e)
        return "- Never give in and never give up -"
