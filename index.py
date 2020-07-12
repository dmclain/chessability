import chess.pgn
import itertools
import json
import requests
import sys
from datetime import date
from io import StringIO
from book import Book

today = date.today()
month = str(today.month).zfill(2)

try:
    if sys.argv[1].startswith('b'):
        analyze = 'black'
    else:
        analyze = 'white'
except IndexError:
    analyze = 'white'

if analyze == 'white':
    print("building white")
    book = Book('white')
    book.load("books/d4.json")
else:
    print("building black")
    book = Book('black')
    book.load("books/sicilian.json")

fname = f"games/{month}.json"
print(f"loading games from {fname}")
with open(fname) as games_file:
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

def analyze_games(book, games):
    for i, (game, g) in enumerate(games):
        move, node = book.check_game(g)
        training = ""
        print(str(i).rjust(2) + " " + game["url"] + " - " + game[analyze]['result'])
        if node and node.lines:
            training = "https://www.chessable.com/variation/" + min(node.lines) + "/"
        if node:
            valid = ",".join(node.moves.keys()).rjust(4)
            move_num = int((node.depth + 1) / 2) + 1  # someday I hope to understand why +3
            if node.player_move:
                print(f"    You deviated from book on move {move_num} by playing {move.rjust(4)} instead of {valid}")
            else:
                print(f"    On move {move_num} they played {move.rjust(4)} which isn't in the book {valid}")
            print("      " + training)
        else:
            print(f"     No book moves found: {g[0].san()}")
        print("")

if analyze == 'white':
    analyze_games(book, white_games)
else:
    analyze_games(book, black_games)
