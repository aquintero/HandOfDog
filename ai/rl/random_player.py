import numpy as np
from ai.go.go_player import GoPlayer


class RandomPlayer(GoPlayer):
    def __init__(self):
        pass

    def play(self, color, history, mask):
        size = history[0].shape[0]
        policy = np.random.uniform(size=(size, size))
        policy = np.minimum(policy, mask)
        point = np.unravel_index(policy.argmax(), policy.shape)
        if policy[point] == 0:
            return size * size
        return point[0] + point[1] * size
