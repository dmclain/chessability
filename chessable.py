import chess.pgn
import itertools
import json
import requests
from io import StringIO
from book import Book

with open("najdorf.json") as book_file:
    lines = json.load(book_file)

najdorf_book = Book(20, u"black")

for line in lines:
    g = chess.pgn.read_game(StringIO(line))
    najdorf_book.add_line(g)
