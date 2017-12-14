import unittest
from ai.go.go_game import GoGame
from ai.go.go_player import GoPlayer


class TestGoBoard(unittest.TestCase):
    def setUp(self):
        self.valid_black_moves = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (5, 5), (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (0, 6), (1, 5), (3, 5), (2, 4), (4, 4), (0, 4), (2, 4), (7, 5), (7, 6), (8, 7), (8, 6), (7, 4), (0, 9)]
        self.valid_white_moves = [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (5, 4), (6, 5), (6, 6), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7), (1, 4), (3, 4), (0, 5), (2, 5), (4, 5), (0, 5), (2, 5), (7, 7), (7, 8), (8, 8), (0, 9)]

        self.invalid_black_moves = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (5, 5), (5, 6),
                                    (4, 6), (3, 6), (2, 6), (1, 6), (0, 6), (1, 5), (3, 5), (2, 4), (4, 4), (0, 4), (2, 4), (4, 4)]
        self.invalid_white_moves = [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (5, 4), (6, 5), (6, 6), (6, 7), (5, 7),
                                    (4, 7), (3, 7), (2, 7), (1, 7), (0, 7), (1, 4), (3, 4), (0, 5), (2, 5), (4, 5), (0, 5)]

    def test_valid_game(self):
        black_player = GoPlayer()
        white_player = GoPlayer()

        def black_play(color, history, mask):
            i = len(history) // 2
            move = self.valid_black_moves[i]
            return move[0] + move[1] * len(history[0])

        black_player.play = black_play

        def white_play(color, history, mask):
            i = len(history) // 2 - 1
            move = self.valid_white_moves[i]
            return move[0] + move[1] * len(history[0])

        white_player.play = white_play

        go_game = GoGame(board_size=9, komi=4.5)
        color, b, w = go_game.play_game(black_player, white_player)
        self.assertEqual(38, b)
        self.assertEqual(47.5, w)

    def test_invalid_game(self):
        black_player = GoPlayer()
        white_player = GoPlayer()

        def black_play(color, history, mask):
            i = len(history) // 2
            move = self.invalid_black_moves[i]
            return move[0] + move[1] * len(history[0])

        black_player.play = black_play

        def white_play(color, history, mask):
            i = len(history) // 2 - 1
            move = self.invalid_white_moves[i]
            return move[0] + move[1] * len(history[0])

        white_player.play = white_play
        go_game = GoGame(board_size=9, komi=4.5)
        with self.assertRaisesRegex(Exception, 'not a legal move'):
            go_game.play_game(black_player, white_player)
