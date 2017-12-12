import numpy as np
from enum import Enum


class Color(Enum):
    black = -1
    empty = 0
    white = 1


class Direction(Enum):
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)


class GoGame:
    def __init__(self, player_black, player_white, board_size=19, komi=6.5):
        self.board_size = board_size
        self.board = GoBoard(board_size)
        self.players = (player_black, player_white)
        self.colors = (Color.black, Color.white)
        self.komi = komi
        self.history = [self.board]

    def reset(self):
        self.board = GoBoard(self.board_size)
        self.history = [self.board]

    def play_game(self):
        n_moves = self.board.size * self.board.size * 2
        for t in range(n_moves):
            player = self.players[t % 2]
            color = self.colors[t % 2]
            mask = self.legal_moves(color)
            move = player.play(self.history, mask, color)

    def legal_moves(self, color):
        board_size = self.board_size
        mask = np.full((board_size, board_size), False, dtype=bool)
        temp_board = GoBoard(go_board=self.board)
        for i in range(board_size):
            for j in range(board_size):
                if not self.board.is_empty(i, j):
                    continue
                temp_board.play(color, i, j)
                for direction in Direction:
                    ni = i + direction[0]
                    nj = j + direction[1]
                    if not temp_board.is_in_bounds(ni, nj):
                        continue
                    if temp_board.is_color(-color, ni, nj):
                        temp_board.clear(ni, nj)
                if temp_board.reach_empty(i, j):
                    mask[i, j] = True
                    for board in self.history:
                        if temp_board == board:
                            mask[i, j] = False
                            break
        return mask


class GoBoard:
    def __init__(self, go_board=None, board_size=19):
        board = None
        if go_board is None:
            board = np.full((board_size, board_size), Color.empty, dtype=int)
        else:
            board_size = board.board_size
            board = np.array(board.board)
        self.board_size = board_size
        self.board = board

    def reset(self):
        self.board = np.full((self.board_size, self.board_size), Color.empty, dtype=int)

    def reach_empty(self, i, j, visited=None):
        self.assert_in_bounds(i, j)
        color = self.board[i, j]
        if visited is None:
            visited = np.full((self.board_size, self.board_size), False, dtype=bool)
        visited[i, j] = True
        for direction in Direction:
            ni = i + direction[0]
            nj = j + direction[1]
            if not self.is_in_bounds(ni, nj) or visited[ni, nj]:
                continue
            if self.board[ni, nj] == Color.empty:
                return True
            if self.board[ni, nj] == color:
                if self.reach_empty(ni, nj, visited):
                    return True
            return False

    def clear(self, i, j):
        self.assert_in_bounds(i, j)
        color = self.board[i, j]
        if color == Color.empty or self.reach_empty(i, j):
            return False
        self._clear_recursive(i, j)

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
        return np.equals(self.board, other.board)

    def __ne__(self, other):
        return not  np.equals(self.board, other.board)

    def play(self, color, i, j):
        self.assert_in_bounds(i, j)
        self.assert_empty(i, j)
        self.board[i, j] = color

    def remove(self, i, j):
        self.assert_in_bounds(i, j)
        self.assert_not_empty(i, j)
        self.board[i, j] = Color.empty

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
