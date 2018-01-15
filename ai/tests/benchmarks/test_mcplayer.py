import unittest
from ai.go.go_game import GoGame
from ai.go.go_engine import GoEngine, GoState, GoColor
from ai.rl.mcts import MCPlayer, MCSearch
from ai.rl.models import CNNModel
import numpy as np
import tensorflow as tf


class TestGoBoard(unittest.TestCase):
    def setUp(self):
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True

        board_size = 19
        komi = 7.5
        self.go_game = GoGame(board_size=board_size)
        model = CNNModel(board_size=board_size)
        history = np.zeros((2, board_size, board_size), dtype=int)
        root_state = GoState(komi, GoColor.black, history[-1], history)
        values, win_rate = model.predict([root_state])
        search = MCSearch(GoEngine(), model, root_state, values, win_rate)
        self.white_player = MCPlayer(search)
        self.black_player = MCPlayer(search)

    def test_play_black_stone(self):
        score = self.go_game.play_game(self.black_player, self.white_player)
        print(score)
        print(self.go_game.history[len(self.go_game.moves)])
        self.go_game.to_sgf('test.sgf')
