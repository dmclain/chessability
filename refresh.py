from datetime import date
import requests

today = date.today()

year = today.year
month = str(today.month).zfill(2)

resp = requests.get(f"https://api.chess.com/pub/player/davemclain/games/{year}/{month}")

with open(f"games/{month}.json", "w") as file:
    file.write(resp.text)
