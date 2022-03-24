import chess.pgn
from colorama import init, Fore, Back, Style

import itertools
import json
import requests
import sys
from datetime import date
from io import StringIO
from book import Book

today = date.today()
month = str(today.month).zfill(2)
init()

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
    book.load("books/e4nystyle.json")
else:
    print("building black")
    book = Book('black')
    book.load("books/e6b6.json")

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
        deviations = book.check_game(g)
        training = ""
        print(str(i).rjust(2) + " " + game["url"] + " - " + game[analyze]['result'])
        print("        " +  g.headers['ECOUrl'].split('/')[-1].replace('-', ' '))
        for (move, node) in deviations:
            move_num = int((node.depth + 1) / 2) + 1  # someday I hope to understand why +3
            if node.depth % 2 == 1:
                color = 'w'
            else:
                color = 'b'
            if node and node.lines:
                training = f"https://www.chessable.com/variation/{min(node.lines)}/#/{move_num}/{color}"
            if node:
                valid = ",".join(node.moves.keys()).rjust(4)
                if node.player_move:
                    print(Fore.RED + f"    You deviated from book on move {move_num} by playing " + Fore.WHITE + move.rjust(4) + Fore.RED + " instead of " + Fore.WHITE + valid + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + f"    On move {move_num} they played {move.rjust(4)} which isn't in the book {valid}" + Style.RESET_ALL)
                print("      " + training)
        if not deviations:
            print(f"     No book moves found: {g[0].san()}")
        print("")

if analyze == 'white':
    analyze_games(book, white_games)
else:
    analyze_games(book, black_games)
