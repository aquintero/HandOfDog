import unittest
from ai.go.go_game import GoGame
from ai.rl.random_player import RandomPlayer


class TestGoBoard(unittest.TestCase):
    def setUp(self):
        self.go_game = GoGame(board_size=19)
        self.white_player = RandomPlayer()
        self.black_player = RandomPlayer()

    def test_play_black_stone(self):
        score = self.go_game.play_game(self.black_player, self.white_player)
        print(score)
        self.go_game.to_sgf('test.sgf')
