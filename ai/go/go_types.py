from enum import IntEnum, Enum


class Color(IntEnum):
    black = -1
    empty = 0
    white = 1


class Direction(tuple, Enum):
    left = (0, -1)
    right = (0, 1)
    up = (-1, 0)
    down = (1, 0)
