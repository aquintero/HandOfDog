import numpy as np
from ai.go.go_types import Color, Direction


class GoBoard:
    def __init__(self, go_board=None, board_size=19):
        board = None
        if go_board is None:
            board = np.full((board_size, board_size), Color.empty, dtype=int)
        else:
            board_size = go_board.board_size
            board = np.array(go_board.board)
        self.board_size = board_size
        self.board = board

    def reset(self):
        self.board = np.full((self.board_size, self.board_size), Color.empty, dtype=int)

    def reach_color(self, color, i, j, visited=None):
        self.assert_in_bounds(i, j)
        start_color = self.board[i, j]
        if visited is None:
            visited = np.full((self.board_size, self.board_size), False, dtype=bool)
        visited[i, j] = True
        for direction in Direction:
            ni = i + direction[0]
            nj = j + direction[1]
            if not self.is_in_bounds(ni, nj) or visited[ni, nj]:
                continue
            if self.board[ni, nj] == color:
                return True
            if self.board[ni, nj] == start_color and self.reach_color(color, ni, nj, visited):
                return True
        return False

    def clear(self, i, j):
        self.assert_in_bounds(i, j)
        color = self.board[i, j]
        if color == Color.empty or self.reach_color(Color.empty, i, j):
            return False
        self._clear_recursive(i, j)
        return True

    def score(self):
        w = 0
        b = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                color = self.board[i, j]
                if color == Color.white:
                    w += 1
                elif color == Color.black:
                    b += 1
                else:
                    reach_black = self.reach_color(Color.black, i, j)
                    reach_white = self.reach_color(Color.white, i, j)
                    if reach_black and not reach_white:
                        b += 1
                    elif reach_white and not reach_black:
                        w += 1
        return b, w

    def _clear_recursive(self, i, j):
        self.assert_in_bounds(i, j)
        color = self.board[i, j]
        if color == Color.empty:
            return
        self.board[i, j] = Color.empty
        for direction in Direction:
            ni = i + direction[0]
            nj = j + direction[1]
            if not self.is_in_bounds(ni, nj) or color != self.board[ni, nj]:
                continue
            self._clear_recursive(ni, nj)

    def __eq__(self, other):
        return np.equal(self.board, other.board)

    def __ne__(self, other):
        return not np.equal(self.board, other.board)

    def play(self, color, i, j):
        self.assert_in_bounds(i, j)
        self.assert_empty(i, j)
        self.board[i, j] = color

    def remove(self, i, j):
        self.assert_in_bounds(i, j)
        self.assert_not_empty(i, j)
        self.board[i, j] = Color.empty

    def get(self, i, j):
        self.assert_in_bounds(i, j)
        return self.board[i, j]

    def assert_in_bounds(self, i, j):
        if not self.is_in_bounds(i, j):
            raise Exception(
                f'position {i} {j} is not a valid point on a board of size {self.board_size}x{self.board_size}')

    def assert_empty(self, i, j):
        if not self.is_empty(i, j):
            raise Exception(f'position {i} {j} cannot be played because it is not empty')

    def assert_not_empty(self, i, j):
        if self.is_empty(i, j):
            raise Exception(f'position {i} {j} cannot be removed because it is empty')

    def is_empty(self, i, j):
        self.assert_in_bounds(i, j)
        return self.board[i, j] == Color.empty

    def is_color(self, color, i, j):
        self.assert_in_bounds(i, j)
        return self.board[i, j] == color

    def is_in_bounds(self, i, j):
        return 0 <= i < self.board_size and 0 <= j < self.board_size
