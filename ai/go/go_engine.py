import ai.go.core.go_core as core
import numpy as np


class GoColor:
    white = core.WHITE
    black = core.BLACK


class GoState:
    def __init__(self, komi, color, board, history):
        self.komi = komi
        self.color = color
        self.board = board
        self.board_size = board.shape[0]
        self.history = history


class GoEngine:
    def next_state(self, state, action):
        board = np.array(state.board, dtype=int)
        core.play_stone(board, state.color, int(action % state.board_size), int(action // state.board_size))
        history = np.zeros(state.history.shape, dtype=int)
        history[:-1] = state.history[1:]
        history[-1] = board
        color = GoColor.white if state.color == GoColor.black else GoColor.black
        return GoState(state.komi, color, board, history)

    def legal_mask(self, state):
        board_size = state.board.shape[0]
        legal_moves = np.zeros((board_size, board_size), dtype=int)
        core.legal_moves(state.board, state.history, state.color, legal_moves)
        return legal_moves
