import unittest
from ai.go.go_board import GoBoard
from ai.go.go_types import Color


class GoBoardTests(unittest.TestCase):
    def setUp(self):
        self.go_board = GoBoard(board_size=19)

    def play_black_stone_test(self):
        self.go_board.play(Color.black, 5, 5)
        self.assertEqual(self.go_board.board[5, 5], Color.black)

    def play_white_stone_test(self):
        self.go_board.play(Color.white, 5, 5)
        self.assertEqual(self.go_board.board[5, 5], Color.white)

    def play_overlapping_stones_test(self):
        self.go_board.play(Color.white, 5, 5)
        with self.assertRaises(Exception):
            self.go_board.play(Color.white, 5, 5)
