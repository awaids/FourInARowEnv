from .PlayerBase import NNPlayerBase
from .PlayerBase import get_available_cols
from .PlayerBase import ObsType, ActType

class HumanPlayer(NNPlayerBase):
    def __init__(self) -> None:
        super().__init__('HP')

    def get_action(self, state: ObsType) -> ActType:
        while True:
            action = int(input('Enter Cols:'))
            if action in get_available_cols(state):
                return action
            print('Invalid Col selected')
