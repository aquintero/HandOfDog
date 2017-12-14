import numpy as np
from .go_board import GoBoard, Color, Direction


class GoGame:
    def __init__(self, player_black, player_white, board_size=19, komi=6.5):
        self.board_size = board_size
        self.board = GoBoard(board_size=board_size)
        self.players = (player_black, player_white)
        self.colors = (Color.black, Color.white)
        self.komi = komi
        self.history = [self.board.board]

    def reset(self):
        self.board.reset()
        self.history = [self.board.board]

    def play_game(self):
        n_moves = self.board_size * self.board_size * 2
        n_pass = 0
        for t in range(n_moves):
            if n_pass == 2:
                break
            player = self.players[t % 2]
            color = self.colors[t % 2]
            mask = self.legal_moves(color)
            move = player.play(color, self.history, mask)
            if move > self.board_size * self.board_size or move < 0:
                raise Exception(f"move #{move} invalid for board_size {self.board_size}x{self.board_size}.")
            if move == self.board_size * self.board_size:
                n_pass += 1
                continue
            n_pass = 0
            i = move % self.board_size
            j = move // self.board_size
            if not mask[i, j]:
                raise Exception(f"move {i} {j} is not a legal move.")
            self.history.append(np.array(self.board.board))
            self.board.play(color, i, j)
            for direction in Direction:
                ni = i + direction[0]
                nj = j + direction[1]
                if not self.board.is_in_bounds(ni, nj):
                    continue
                if self.board.is_color(-color, ni, nj):
                    self.board.clear(ni, nj)
        score = self.score()
        return score

    def legal_moves(self, color):
        board_size = self.board_size
        mask = np.full((board_size, board_size), False, dtype=bool)
        for i in range(board_size):
            for j in range(board_size):
                if not self.board.is_empty(i, j):
                    continue
                temp_board = GoBoard(go_board=self.board)
                temp_board.play(color, i, j)
                for direction in Direction:
                    ni = i + direction[0]
                    nj = j + direction[1]
                    if not temp_board.is_in_bounds(ni, nj):
                        continue
                    if temp_board.is_color(-color, ni, nj):
                        temp_board.clear(ni, nj)
                if temp_board.reach_color(Color.empty, i, j):
                    mask[i, j] = True
                    for board in self.history:
                        if np.equal(temp_board.board, board).all():
                            mask[i, j] = False
                            break
        return mask

    def score(self):
        b, w = self.board.score()
        w += self.komi
        if b > w:
            return Color.black, b, w
        else:
            return Color.white, b, w