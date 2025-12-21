from enum import Enum

BOARD_WIDTH = 13
BOARD_HEIGHT = 19

class Phase(Enum):
    ROLL = "Roll Phase"
    MAIN = "Main Phase"
    ATTACK = "Attack Phase"
    ADJUST = "Adjust Phase"
    END = "End Turn"
