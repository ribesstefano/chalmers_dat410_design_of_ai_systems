from transform import Transform, Identity, Rotate90, Flip

import random
import numpy as np

X = 1
O = -1
EMPTY = 0

X_WINS = 1
O_WINS = -1
DRAW = 0
NOT_OVER = 2

class Board(object):
    """Class to implement the board of game tic-tac-toe"""
    def __init__(self, board=None, illegal_move=None, board_size=3):
        self.board_size = board_size
        self.board_dimensions = (board_size, board_size)
        if board is None:
            # if game started the board is initialized as empty board
            self.board = np.array([EMPTY] * board_size ** 2)
        else:
            self.board = board
        # for every board there are a set of illegal moves
        self.illegal_move = illegal_move
        # matrix version of board to simplify later controls
        self.board_2d = self.board.reshape(self.board_dimensions)

    def get_board_dimensions(self):
        return self.board_dimensions

    def get_result(self):
        """returns the result of the game:
        - (1) if X wins
        - (-1) if O wins
        - (0) if tie
        - (2) if game is not over"""
        if self.illegal_move is not None:
            return O_WINS if self.get_turn() == X else X_WINS

        rows_cols_and_diagonals = self._get_rows_cols_diagonals(self.board_2d)

        sums = list(map(sum, rows_cols_and_diagonals))
        max_value = max(sums)
        min_value = min(sums)

        if max_value == self.board_size:
            return X_WINS

        if min_value == -self.board_size:
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
            return Board(board_copy, move_index, board_size)
        board_copy[move_index] = self.get_turn()
        return Board(board_copy, board_size=self.board_size)

    def get_turn(self):
        """Returns whose turn it is"""
        non_zero = np.count_nonzero(self.board)
        return X if (non_zero % 2 == 0) else O

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
                move = self._get_symbol(self.board_2d[r, c])
                if c == 0:
                    board_as_string += f"|{move}|"
                elif c == 1:
                    board_as_string += f"{move}|"
                else:
                    board_as_string += f"{move}|\n"
        board_as_string += "-------\n"
        return board_as_string

    def _get_rows_cols_diagonals(self, board_2d):
        """returns every row, column and diagonal of the board"""
        rows_diagonal = self._get_rows_diagonal(board_2d)
        cols_antidiagonal = self._get_rows_diagonal(np.rot90(board_2d))
        return rows_diagonal + cols_antidiagonal


    def _get_rows_diagonal(self, board_2d):
        """returns rows and main diagonal of the board"""
        num_rows = board_2d.shape[0]
        return ([row for row in board_2d[range(num_rows), :]]
                + [board_2d.diagonal()])

    def _get_symbol(self, cell):
        """returns symbol in a cell"""
        if cell == X:
            return 'X'
        if cell == O:
            return 'O'
        return '-'

class BoardCache:
    """class to cache boards"""
    def __init__(self):
        self.cache = {}

    def set_for_position(self, board, o):
        self.cache[board.board_2d.tobytes()] = o

    def get_for_position(self, board):
        board_2d = board.board_2d
        orientations = self._get_symmetrical_board_orientations(board_2d)
        for b, t in orientations:
            result = self.cache.get(b.tobytes())
            if result is not None:
                return (result, t), True
        return None, False

    def reset(self):
        self.cache = {}

    def _get_symmetrical_board_orientations(self, board_2d):
        """returns orientations of a given board"""
        TRANSFORMATIONS = [
            Identity(), Rotate90(1), Rotate90(2), Rotate90(3), Flip(np.flipud),
            Flip(np.fliplr), Transform(Rotate90(1), Flip(np.flipud)),
            Transform(Rotate90(1), Flip(np.fliplr))
        ]
        return [(t.transform(board_2d), t) for t in TRANSFORMATIONS]