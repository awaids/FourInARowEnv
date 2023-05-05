import random
from .PlayerBase import NNPlayerBase
from .PlayerBase import get_available_cols
from .PlayerBase import ObsType, ActType
from typing import Optional, List


def get_rand_action(actions:List[ActType]) -> ActType:
    """ Returns a random action from the given list of actions"""
    return actions[random.randrange(len(actions))]

class RandomPlayer(NNPlayerBase):
    def __init__(self, pid:str, seed:Optional[int] = None) -> None:
        super().__init__(pid)
        if seed:
            random.seed(seed)

    def get_action(self, state: ObsType) -> ActType:
        return get_rand_action(get_available_cols(state))