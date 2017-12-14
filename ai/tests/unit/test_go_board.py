import unittest
import numpy as np
from ai.go.go_board import GoBoard
from ai.go.go_types import Color


class TestGoBoard(unittest.TestCase):
    def setUp(self):
        self.go_board = GoBoard(board_size=5)

    def test_play_black_stone(self):
        self.go_board.play(Color.black, 2, 2)
        self.assertEqual(Color.black, self.go_board.board[2, 2])

    def test_play_white_stone(self):
        self.go_board.play(Color.white, 2, 2)
        self.assertEqual(Color.white, self.go_board.board[2, 2])

    def test_play_overlapping_stones(self):
        self.go_board.play(Color.white, 2, 2)
        with self.assertRaisesRegex(Exception, 'it is not empty'):
            self.go_board.play(Color.white, 2, 2)

    def test_is_in_bounds(self):
        self.assertEqual(True, self.go_board.is_in_bounds(0, 0))
        self.assertEqual(False, self.go_board.is_in_bounds(-1, 0))
        self.assertEqual(False, self.go_board.is_in_bounds(0, 5))

    def test_reach_empty(self):
        self.go_board.play(Color.white, 0, 1)
        self.go_board.play(Color.white, 1, 1)
        self.go_board.play(Color.black, 0, 0)
        self.assertEqual(True, self.go_board.reach_color(Color.empty, 0, 0))
        self.go_board.play(Color.black, 1, 0)
        self.go_board.play(Color.white, 2, 1)
        self.assertEqual(True, self.go_board.reach_color(Color.empty, 0, 0))
        self.go_board.play(Color.white, 2, 0)
        self.assertEqual(False, self.go_board.reach_color(Color.empty, 0, 0))

    def test_full_game(self):
        self.go_board.play(Color.black, 2, 2)
        self.go_board.play(Color.white, 2, 1)
        self.go_board.play(Color.black, 1, 2)
        self.go_board.play(Color.white, 3, 2)
        self.go_board.play(Color.black, 3, 3)
        self.go_board.play(Color.white, 4, 1)
        self.go_board.play(Color.black, 1, 1)
        self.go_board.play(Color.white, 4, 3)
        self.go_board.play(Color.black, 3, 4)
        self.go_board.play(Color.white, 3, 0)
        self.go_board.play(Color.black, 1, 0)
        self.go_board.play(Color.white, 2, 0)
        b, w = self.go_board.score()
        self.assertEqual(15, b)
        self.assertEqual(9, w)

    def test_clear(self):
        b0 = np.array([[1, -1,  0, 0, 0],
                      [-1, -1, 0, 0, 0],
                      [0, 0, 1, 1, 1],
                      [0, 1,  1, -1, -1],
                      [0, 1, -1, -1, -1]])
        self.go_board.play(Color.black, 0, 1)
        self.go_board.play(Color.black, 1, 1)
        self.go_board.play(Color.black, 1, 0)
        self.go_board.play(Color.black, 4, 4)
        self.go_board.play(Color.black, 4, 3)
        self.go_board.play(Color.black, 3, 4)
        self.go_board.play(Color.black, 3, 3)
        self.go_board.play(Color.black, 4, 2)
        self.go_board.play(Color.white, 0, 0)
        self.go_board.play(Color.white, 4, 1)
        self.go_board.play(Color.white, 3, 1)
        self.go_board.play(Color.white, 3, 2)
        self.go_board.play(Color.white, 2, 2)
        self.go_board.play(Color.white, 2, 3)
        self.go_board.play(Color.white, 2, 4)
        self.assertEqual(False, self.go_board.clear(1, 1))
        self.assertEqual(True, np.equal(b0, self.go_board.board).all())

        b1 = np.array([[0, -1, 0, 0, 0],
                       [-1, -1, 0, 0, 0],
                       [0, 0, 1, 1, 1],
                       [0, 1, 1, -1, -1],
                       [0, 1, -1, -1, -1]])
        self.assertEqual(True, self.go_board.clear(0, 0))
        self.assertEqual(True, np.equal(b1, self.go_board.board).all())

        self.assertEqual(False, self.go_board.clear(2, 2))
        self.assertEqual(True, np.equal(b1, self.go_board.board).all())

        b2 = np.array([[0, -1, 0, 0, 0],
                       [-1, -1, 0, 0, 0],
                       [0, 0, 1, 1, 1],
                       [0, 1, 1, 0, 0],
                       [0, 1, 0, 0, 0]])
        self.assertEqual(True, self.go_board.clear(4, 4))
        self.assertEqual(True, np.equal(b2, self.go_board.board).all())
