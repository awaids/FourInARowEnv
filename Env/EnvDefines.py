from typing import TypeVar, Literal
from random import getrandbits

# Data types
ObsType = TypeVar("ObsType")
ActType = TypeVar("ActType")

PlayerType = Literal[1, 2]
FOUR = 4


# Rewards -> This affects training
LostValue = -1
WonValue = 1
DrawnValue = 0.8
WrongValue = -5

# Helper functions
def shuffle_player1() -> bool:
    # Randomly decide who takes first turn
    return bool(getrandbits(1))

