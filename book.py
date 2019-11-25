import chess.pgn
from io import StringIO
import json

class Book(object):
    def __init__(self, color):
        self.color = color
        self.nodes = dict()

    def load(self, name):
        with open(name) as book_file:
            lines = json.load(book_file)
        for line in lines:
            g = chess.pgn.read_game(StringIO(line['pgn']))
            self.add_line(g, line['id'])

    def add_line(self, cgame, id):
        mainline = iter(cgame.mainline())
        first_move = next(mainline)
        if first_move.san() not in self.nodes:
            self.nodes[first_move.san()] = BookNode(self.color != 'white', 0, first_move.san())
        self.nodes[first_move.san()].add_line(mainline, cgame, id)

    def check_game(self, cgame):
        mainline = iter(cgame.mainline())
        first_move = next(mainline)
        if first_move.san() not in self.nodes:
            return (first_move.san(), None)
        node = self.nodes[first_move.san()]
        for move in mainline:
            if move.san() in node.moves:
                node = node.moves[move.san()]
            else:
                return (move.san(), node)
        return (move.san(), node)

class BookNode(object):
    parent = None
    move = None

    def __init__(self, player_move, depth, move):
        self.player_move = player_move
        self.depth = depth
        self.move = move
        self.moves = {}
        self.lines = []

    def add_line(self, remaining_moves, line, id):
        self.lines.append(id)
        try:
            next_move = next(remaining_moves)
            if next_move.san() not in self.moves:
                self.moves[next_move.san()] = BookNode(not self.player_move, self.depth + 1, next_move.san())
            self.moves[next_move.san()].add_line(remaining_moves, line, id)
        except StopIteration:
            pass

    def __repr__(self):
        valid = ",".join(self.moves.keys()).rjust(4)
        if self.player_move:
            move = '++ ' + valid
        else:
            move = 'x      '
        return f"{str(self.depth).rjust(2)} - {move}"
