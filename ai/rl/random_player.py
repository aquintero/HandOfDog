import numpy as np
from ai.go.go_player import GoPlayer


class RandomPlayer(GoPlayer):
    def play(self, color, history, move_history, current_move, mask):
        size = history[0].shape[0]
        policy = np.random.uniform(size=(size, size))
        policy = np.minimum(policy, mask)
        point = np.unravel_index(policy.argmax(), policy.shape)
        if policy[point] == 0:
            return size * size
        return point[0] + point[1] * size
