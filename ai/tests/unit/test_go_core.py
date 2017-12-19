import unittest
import numpy as np
import ai.go.core.go_core as core

class TestGoBoard(unittest.TestCase):

    def test_is_in_bounds(self):
        self.assertEqual(True, core.is_in_bounds(5, 0, 0))
        self.assertEqual(True, core.is_in_bounds(5, 0, 4))
        self.assertEqual(False, core.is_in_bounds(5, 0, 5))
        self.assertEqual(True, core.is_in_bounds(5, 4, 0))
        self.assertEqual(False, core.is_in_bounds(5, -1, 0))
        self.assertEqual(False, core.is_in_bounds(5, 5, 0))

    def test_reach_color(self):
        board = np.array([[1, 1, -1, 0, 0],
                         [-1, -1, 0, 0, 1],
                         [0, 0, 1, 1, -1],
                         [1, 1, -1, 1, 1],
                         [-1, 1, 1, 0, 0]])
        self.assertEqual(False, core.reach_color(board, core.EMPTY, 0, 0))
        self.assertEqual(True, core.reach_color(board, core.EMPTY, 4, 1))
        self.assertEqual(False, core.reach_color(board, core.EMPTY, 3, 2))
        self.assertEqual(False, core.reach_color(board, core.EMPTY, 4, 0))
        self.assertEqual(False, core.reach_color(board, core.EMPTY, 2, 4))

    def test_clear(self):
        board = np.array([[core.WHITE, core.WHITE, core.BLACK, core.EMPTY, core.EMPTY],
                          [core.BLACK, core.BLACK, core.EMPTY, core.EMPTY, core.WHITE],
                          [core.EMPTY, core.EMPTY, core.WHITE, core.WHITE, core.BLACK],
                          [core.WHITE, core.WHITE,  core.BLACK, core.WHITE, core.WHITE],
                          [core.BLACK, core.WHITE, core.WHITE, core.EMPTY, core.EMPTY]])
        self.assertEqual(False, core.clear(board, 0, 2))
        self.assertEqual(False, core.clear(board, 4, 1))
        self.assertEqual(True, core.clear(board, 0, 0))
        self.assertEqual(True, core.clear(board, 4, 0))
        self.assertEqual(True, core.clear(board, 3, 2))
        self.assertEqual(True, core.clear(board, 2, 4))

    def test_score(self):
        board = np.array([[core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY],
                          [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.WHITE, core.EMPTY, core.EMPTY, core.WHITE, core.EMPTY],
                          [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY],
                          [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.WHITE, core.EMPTY, core.EMPTY, core.WHITE, core.EMPTY],
                          [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY],
                          [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.WHITE, core.EMPTY, core.EMPTY, core.WHITE, core.EMPTY],
                          [core.EMPTY, core.EMPTY, core.BLACK, core.BLACK, core.BLACK, core.WHITE, core.WHITE, core.WHITE, core.EMPTY],
                          [core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.BLACK, core.BLACK, core.BLACK, core.WHITE, core.WHITE],
                          [core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.BLACK, core.BLACK, core.WHITE]])

        score = core.score(board)
        self.assertEqual(38, score[0])
        self.assertEqual(43, score[1])

    def test_play_stone(self):
        moves = [[(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (5, 5),
                  (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (0, 6), (1, 5), (3, 5), (2, 4), (4, 4),
                  (0, 4), (2, 4), (7, 5), (7, 6), (8, 7), (8, 6), (7, 4), (0, 9)],
                 [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (5, 4), (6, 5), (6, 6), (6, 7),
                  (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7), (1, 4), (3, 4), (0, 5), (2, 5),
                  (4, 5), (0, 5), (2, 5), (7, 7), (7, 8), (8, 8), (0, 9)]]

        board = np.full((9, 9), core.EMPTY)
        result = [[core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.WHITE, core.EMPTY, core.EMPTY, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.WHITE, core.EMPTY, core.EMPTY, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.WHITE, core.EMPTY, core.EMPTY, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.BLACK, core.BLACK, core.WHITE, core.WHITE, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.BLACK, core.BLACK, core.BLACK, core.WHITE, core.WHITE],
                  [core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.BLACK, core.BLACK, core.WHITE]]

        play_game(board, moves)
        self.assertEqual(True, np.equal(board, result).all())

    def test_legal_moves(self):
        moves = [[(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (5, 5),
                  (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (0, 6), (1, 5), (3, 5), (1, 1), (1, 0),
                  (2, 4), (4, 4), (0, 4), (2, 4)],
                 [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (5, 4), (6, 5), (6, 6), (6, 7),
                  (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7), (1, 4), (3, 4), (0, 1), (8, 8),
                  (0, 5), (2, 5), (4, 5), (0, 5)]]

        board = np.full((9, 9), core.EMPTY)
        result = [[core.EMPTY, core.WHITE, core.BLACK, core.WHITE, core.EMPTY, core.WHITE, core.BLACK, core.WHITE, core.EMPTY],
                  [core.BLACK, core.BLACK, core.BLACK, core.WHITE, core.WHITE, core.BLACK, core.BLACK, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.BLACK, core.EMPTY, core.BLACK, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.WHITE, core.BLACK, core.BLACK, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.EMPTY, core.WHITE, core.BLACK, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.WHITE, core.WHITE, core.BLACK, core.BLACK, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.BLACK, core.BLACK, core.BLACK, core.WHITE, core.WHITE, core.WHITE, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY],
                  [core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.EMPTY, core.WHITE]]

        black_legal_moves = [[1, 0, 0, 0, 0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 0]]
        white_legal_moves = [[0, 0, 0, 0, 1, 0, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 0, 0, 0, 1, 0, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 0, 0, 1, 0, 0, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 0]]

        history = play_game(board, moves)
        self.assertEqual(True, np.equal(board, result).all())

        legal_moves = np.ones((9, 9), dtype=int)
        core.legal_moves(board, history, core.BLACK, legal_moves)
        self.assertEqual(True, np.equal(legal_moves, black_legal_moves).all())

        legal_moves = np.zeros((9, 9), dtype=int)
        core.legal_moves(board, history, core.WHITE, legal_moves)
        self.assertEqual(True, np.equal(legal_moves, white_legal_moves).all())

        legal_moves = np.zeros((9, 9), dtype=int)
        core.legal_moves(np.full((9, 9), core.EMPTY), np.full((6, 9, 9), core.EMPTY), core.BLACK, legal_moves)
        self.assertEqual(True, np.equal(legal_moves, np.ones((9, 9), dtype=int)).all())


def play_game(board, moves):
    t = 0
    history = [np.array(board)]
    while True:
        if t >= len(moves[0]):
            break
        core.play_stone(board, core.BLACK, moves[0][t][0], moves[0][t][1])
        history.append(np.array(board))
        if t >= len(moves[1]):
            break
        core.play_stone(board, core.WHITE, moves[1][t][0], moves[1][t][1])
        history.append(np.array(board))
        t += 1
    return np.array(history)
