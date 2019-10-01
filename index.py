import chess.pgn
import itertools
import json
import requests
from io import StringIO
from book import Book

# print("building black")
# black_book = Book('black')
# black_book.load("najdorf.json")

print("building white")
white_book = Book('white')
white_book.load("d4.json")

print("loading games")
if False:
    resp = requests.get(u"https://api.chess.com/pub/player/davemclain/games/2019/09")
    games = resp.json()[u"games"]
else:
    with open("09.json") as games_file:
        games = json.load(games_file)[u"games"]

white_games = []
black_games = []

print("comparing games to book")
for game in games:
    g = chess.pgn.read_game(StringIO(game[u"pgn"]))
    if game[u"white"][u"username"] == u"davemclain":
        white_games.append((game, g))
    else:
        black_games.append((game, g))
        # print(repr(black_book.check_game(g)) + "   - " + game["url"])

for i, (game, g) in enumerate(white_games):
    move, node = white_book.check_game(g)
    print(str(i).rjust(2) + " " + move.rjust(4) + " - " + repr(node) + " - " + game["url"])

    # if me == u"white":
    #     moves = list(itertools.islice(g.mainline(), 8))
    #     if True or moves[0].san() == 'e4':
    #         print(" ".join(m.san().rjust(5) for m in moves))
    #         print(game[me]["result"] + "  " + game["url"])
