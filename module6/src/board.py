import random
import itertools
import re

import numpy as np

from transform import Transform, Identity, Rotate90, Flip

TRANSFORMATIONS = [Identity(), Rotate90(1), Rotate90(2), Rotate90(3),
                   Flip(np.flipud), Flip(np.fliplr),
                   Transform(Rotate90(1), Flip(np.flipud)),
                   Transform(Rotate90(1), Flip(np.fliplr))]

BOARD_SIZE = 3
BOARD_DIMENSIONS = (BOARD_SIZE, BOARD_SIZE)

X = 1
O = -1
EMPTY = 0

X_WINS = 1
O_WINS = -1
DRAW = 0
NOT_OVER = 2

new_board = np.array([EMPTY] * BOARD_SIZE ** 2)

result_dict = {X_WINS: 'X is the winner', O_WINS: 'O is the winner', DRAW: 'The game finished in a draw'}


def play_game(x_strategy, o_strategy):
    """given the two players strategies it plays a game of tic-tac-toe"""
    board = Board()
    player_strategies = itertools.cycle([x_strategy, o_strategy])

    while not board.is_gameover():
        play = next(player_strategies)
        board = play(board)
    #     board.print_board()
    #
    # board.print_board()
    # print(result_dict.get(board.get_result()))
    return board


def play_games(total_games, x_strategy, o_strategy, play_single_game=play_game):
    """Plays a given number of games"""
    results = {
        X_WINS: 0,
        O_WINS: 0,
        DRAW: 0
    }

    results_array = []

    for g in range(total_games):
        end_of_game = (play_single_game(x_strategy, o_strategy))
        result = end_of_game.get_result()
        results[result] += 1
        results_array.append(result)

    x_wins_percent = results[X_WINS] / total_games * 100
    o_wins_percent = results[O_WINS] / total_games * 100
    draw_percent = results[DRAW] / total_games * 100

    print(f"X wins: {x_wins_percent:.2f}%")
    print(f"O wins: {o_wins_percent:.2f}%")
    print(f"draw  : {draw_percent:.2f}%")

    return results_array


def play_random_move(board):
    """Strategy to play random moves"""
    move = board.get_random_legal_move_index()
    return board.move(move)


def play_human_move(board):
    """Strategy that requires human input"""
    print('Type move coordinates as (n,m): ')
    line = input()
    print(type(line))
    line = re.sub("[()]", "", line)
    bits = line.split(',')  # split
    bits = [int(bit) for bit in bits]
    move = np.ravel_multi_index(bits, BOARD_DIMENSIONS)
    return board.move(move)


def is_even(value):
    """checks if value is even, returns Bool"""
    return value % 2 == 0


def is_empty(values):
    """checks if value is empty, returns Bool"""
    return values is None or len(values) == 0


class Board:
    """Class to implement the board of game tic-tac-toe"""

    def __init__(self, board=None, illegal_move=None):
        if board is None:
            # if game started the board is initialized as empty board
            self.board = np.copy(new_board)
        else:
            self.board = board

        # for every board there are a set of illegal moves
        self.illegal_move = illegal_move

        # matrix version of board to simplify later controls
        self.board_2d = self.board.reshape(BOARD_DIMENSIONS)

    def get_result(self):
        """returns the result of the game:
        - (1) if X wins
        - (-1) if O wins
        - (0) if tie
        - (2) if game is not over"""
        if self.illegal_move is not None:
            return O_WINS if self.get_turn() == X else X_WINS

        rows_cols_and_diagonals = get_rows_cols_diagonals(self.board_2d)

        sums = list(map(sum, rows_cols_and_diagonals))
        max_value = max(sums)
        min_value = min(sums)

        if max_value == BOARD_SIZE:
            return X_WINS

        if min_value == -BOARD_SIZE:
            return O_WINS

        if EMPTY not in self.board_2d:
            return DRAW

        return NOT_OVER

    def is_gameover(self):
        """check if game is over, returns Bool"""
        return self.get_result() != NOT_OVER

    def is_in_illegal_state(self):
        """check if board is in illegal state, i.e. illegal move is made. Returns Bool"""
        return self.illegal_move is not None

    def move(self, move_index):
        """plays a new move, move_index is the index of flattened board. Returns new board with move made"""
        board_copy = np.copy(self.board)

        if move_index not in self.get_valid_moves_indexes():
            return Board(board_copy, illegal_move=move_index)

        board_copy[move_index] = self.get_turn()
        return Board(board_copy)

    def get_turn(self):
        """Returns whose turn it is"""
        non_zero = np.count_nonzero(self.board)
        return X if is_even(non_zero) else O

    def get_valid_moves_indexes(self):
        """returns array of valid moves"""
        return ([i for i in range(self.board.size)
                 if self.board[i] == EMPTY])

    def get_illegal_moves_indexes(self):
        """returns array of illegal moves"""
        return ([i for i in range(self.board.size)
                 if self.board[i] != EMPTY])

    def get_random_legal_move_index(self):
        """returns a random move from legal moves"""
        return random.choice(self.get_valid_moves_indexes())

    def print_board(self):
        """prints board"""
        print(self.board_to_string())

    def board_to_string(self):
        rows, cols = self.board_2d.shape
        board_as_string = "-------\n"
        for r in range(rows):
            for c in range(cols):
                move = get_symbol(self.board_2d[r, c])
                if c == 0:
                    board_as_string += f"|{move}|"
                elif c == 1:
                    board_as_string += f"{move}|"
                else:
                    board_as_string += f"{move}|\n"
        board_as_string += "-------\n"

        return board_as_string


class BoardCache:
    """class to cache boards"""

    def __init__(self):
        self.cache = {}

    def set_for_position(self, board, o):
        self.cache[board.board_2d.tobytes()] = o

    def get_for_position(self, board):
        board_2d = board.board_2d

        orientations = get_symmetrical_board_orientations(board_2d)

        for b, t in orientations:
            result = self.cache.get(b.tobytes())
            if result is not None:
                return (result, t), True

        return None, False

    def reset(self):
        self.cache = {}


def get_symmetrical_board_orientations(board_2d):
    """returns orientations of a given board"""
    return [(t.transform(board_2d), t) for t in TRANSFORMATIONS]


def get_rows_cols_diagonals(board_2d):
    """returns every row, column and diagonal of the board"""
    rows_diagonal = get_rows_diagonal(board_2d)
    cols_antidiagonal = get_rows_diagonal(np.rot90(board_2d))
    return rows_diagonal + cols_antidiagonal


def get_rows_diagonal(board_2d):
    """returns rows and main diagonal of the board"""
    num_rows = board_2d.shape[0]
    return ([row for row in board_2d[range(num_rows), :]]
            + [board_2d.diagonal()])


def get_symbol(cell):
    """returns symbol in a cell"""
    if cell == X:
        return 'X'
    if cell == O:
        return 'O'
    return '-'


def is_draw(board):
    """returns True if game result is a draw"""
    return board.get_result() == DRAW
