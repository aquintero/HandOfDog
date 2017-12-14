import numpy as np
from .go_board import GoBoard, Color, Direction


class GoGame:
    def __init__(self, board_size=19, komi=6.5):
        self.board_size = board_size
        self.board = GoBoard(board_size=board_size)
        self.colors = (Color.black, Color.white)
        self.komi = komi
        self.board_history = [self.board.board]
        self.move_history = []

    def reset(self):
        self.board.reset()
        self.board_history = [self.board.board]
        self.move_history = []

    def play_game(self, player_black, player_white):
        players = [player_black, player_white]
        n_moves = self.board_size * self.board_size * 2
        n_pass = 0
        for t in range(n_moves):
            if n_pass == 2:
                break
            player = players[t % 2]
            color = self.colors[t % 2]
            mask = self.legal_moves(color)
            move = player.play(color, self.board_history, mask)
            if move > self.board_size * self.board_size or move < 0:
                raise Exception(f"move #{move} invalid for board_size {self.board_size}x{self.board_size}.")
            if move == self.board_size * self.board_size:
                self.move_history.append(move)
                n_pass += 1
                continue
            n_pass = 0
            i = move % self.board_size
            j = move // self.board_size
            if not mask[i, j]:
                raise Exception(f"move {i} {j} is not a legal move.")
            self.board.play(color, i, j)
            for direction in Direction:
                ni = i + direction[0]
                nj = j + direction[1]
                if not self.board.is_in_bounds(ni, nj):
                    continue
                if self.board.is_color(-color, ni, nj):
                    self.board.clear(ni, nj)
            self.board_history.append(np.array(self.board.board))
            self.move_history.append(move)
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
                    for board in self.board_history:
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

    def to_sgf(self, file_path):
        sgf = []
        color, b, w = self.score()
        winner = 'B' if color == Color.black else 'W'
        difference = abs(b - w)
        sgf.append(f'(;GM[1]FF[4]CA[UTF-8]SZ[{self.board_size}]KM[{self.komi}]PB[Black]PW[White]RE[{winner}+{difference}]')
        for t, move in enumerate(self.move_history):
            player = 'W' if t % 2 else 'B'
            if move == self.board_size * self.board_size:
                sgf.append(f'{player}[]')
                continue
            i = chr(ord('a') + (move % self.board_size))
            j = chr(ord('a') + (move // self.board_size))
            player = 'W' if t % 2 else 'B'
            sgf.append(f';{player}[{j}{i}]')
        sgf.append(')')
        with open(file_path, 'w')as f:
            f.write(''.join(sgf))
