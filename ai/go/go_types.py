from enum import IntEnum, Enum
from ai.go.core import go_core as core


class Color(IntEnum):
    black = core.BLACK
    empty = core.EMPTY
    white = core.WHITE

class Direction(tuple, Enum):
    left = (0, -1)
    right = (0, 1)
    up = (-1, 0)
    down = (1, 0)
