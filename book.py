import chess.pgn
from collections import defaultdict
from io import StringIO
import json

class Book(object):
    def __init__(self, color):
        self.color = color
        self.nodes = dict()
        self.transpositions = defaultdict(list)

    def load(self, name):
        with open(name) as book_file:
            lines = json.load(book_file)
        for line in lines:
            g = chess.pgn.read_game(StringIO(line['pgn']))
            self.add_line(g, line['id'])

    def add_line(self, cgame, id):
        first_move = cgame.next()
        if first_move.san() not in self.nodes:
            self.nodes[first_move.san()] = BookNode(self.color != 'white', 0, first_move.san())
        self.nodes[first_move.san()].add_line(cgame.next(), id, self.transpositions)

    def check_game(self, cgame):
        nodes = self.transpositions[cgame.next().board().fen()]
        departures = []
        for move in cgame.mainline():
            for node in nodes:
                if move.san() not in node.moves:
                    departures.append((move.san(), node))
            nodes = self.transpositions[move.board().fen()]
            # print(f"{move.san()} - {nodes}")

        return departures

class BookNode(object):
    parent = None
    move = None

    def __init__(self, player_move, depth, move):
        self.player_move = player_move
        self.depth = depth
        self.move = move
        self.moves = {}
        self.lines = []

    def add_line(self, line, id, transpositions):
        self.lines.append(id)
        next_move = line.next()
        if next_move:
            if next_move.san() not in self.moves:
                new_node = BookNode(not self.player_move, self.depth + 1, next_move.san())
                self.moves[next_move.san()] = new_node
                transpositions[next_move.board().fen()].append(new_node)
            self.moves[next_move.san()].add_line(next_move, id, transpositions)

    def __repr__(self):
        valid = ",".join(self.moves.keys()).rjust(4)
        if self.player_move:
            move = '++ ' + valid
        else:
            move = 'x      '
        return f"{str(self.depth).rjust(2)} - {move}"
