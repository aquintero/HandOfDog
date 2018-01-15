import numpy as np
import ai.go.core.go_core as core


class GoGame:
    def __init__(self, board_size=19, komi=6.5):
        self.board_size = board_size
        self.max_moves = self.board_size * self.board_size * 2 + 6
        self.history = np.full((self.max_moves + 1, self.board_size, self.board_size), core.EMPTY)
        self.komi = komi
        self.colors = [core.BLACK, core.WHITE]
        self.moves = []

    def reset(self):
        self.history = np.full((self.max_moves + 1, self.board_size, self.board_size), core.EMPTY)
        self.moves = []

    def play_game(self, player_black, player_white):
        players = [player_black, player_white]
        n_pass = 0
        for t in range(self.max_moves):
            if n_pass == 2:
                break
            np.copyto(self.history[t + 1], self.history[t])
            player = players[t % 2]
            color = self.colors[t % 2]
            mask = np.ones((self.board_size, self.board_size), dtype=int)
            core.legal_moves(self.history[t], self.history[max(0, t - 1): t + 1], color, mask)
            move = player.play(color, self.history, t, mask)
            if move > self.board_size * self.board_size or move < 0:
                raise Exception(f"move #{move} invalid for board_size {self.board_size}x{self.board_size}.")
            self.moves.append(move)
            if move == self.board_size * self.board_size:
                n_pass += 1
                continue
            n_pass = 0
            i = int(move % self.board_size)
            j = int(move // self.board_size)
            if not mask[i, j]:
                self.to_sgf('test.sgf')
                print(i, j)
                print(self.history[t])
                print(self.history[t + 1])
                print(player.search.tree.root.state.board)
                raise Exception(f"move {i} {j} is not a legal move.")
            core.play_stone(self.history[t + 1], color, i, j)

            if not np.equal(self.history[t + 1], player.search.tree.root.state.board).all():
                print(i, j)
                print(self.history[t])
                print(self.history[t + 1])
                print(player.search.tree.root.state.board)
        self.to_sgf('test.sgf')
        return self.score(self.history[t])

    def score(self, board):
        score = core.score(board)
        b = score[0]
        w = score[1]
        w += self.komi
        if b > w:
            return core.BLACK, b, w
        else:
            return core.WHITE, b, w

    def to_sgf(self, file_path):
        sgf = []
        color, b, w = self.score(self.history[len(self.moves)])
        winner = 'B' if color == core.BLACK else 'W'
        difference = abs(b - w)
        sgf.append(f'(;GM[1]FF[4]CA[UTF-8]SZ[{self.board_size}]KM[{self.komi}]PB[Black]PW[White]RE[{winner}+{difference}]')
        for t, move in enumerate(self.moves):
            player = 'W' if t % 2 else 'B'
            if move == self.board_size * self.board_size:
                sgf.append(f';{player}[]')
                continue
            i = chr(ord('a') + (move % self.board_size))
            j = chr(ord('a') + (move // self.board_size))
            player = 'W' if t % 2 else 'B'
            sgf.append(f';{player}[{j}{i}]')
        sgf.append(')')
        with open(file_path, 'w')as f:
            f.write(''.join(sgf))
