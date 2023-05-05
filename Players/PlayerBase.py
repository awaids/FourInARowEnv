from __future__ import annotations
from pathlib import Path
from Env import ObsType, ActType
from abc import ABC, abstractmethod
from typing import List

import numpy as np
import pickle

class NNPlayerBase(ABC):
    def __init__(self, pid:str) -> None:
        super().__init__()
        self.id = pid

    @abstractmethod
    def get_action(self, state: ObsType) -> ActType:
        raise NotImplemented

    def update_internals(self, next_state:ObsType, state:ObsType, action:ActType, reward:int, done:bool) -> None:
        pass

    def dump(self, pkl_file:Path) -> None:
        """ Saves the current object. This is useful to restart training. """
        print(f'Dumping {self.__class__.__name__} object.')
        with open(pkl_file, 'wb') as fp:
            pickle.dump(self, fp)
    
    @classmethod
    def restore_player(cls, pkl_file:Path) -> NNPlayerBase:
        """ Restores the object from the pkl file """
        assert(pkl_file.exists()), "pkl file does not exists"
        with open(pkl_file, 'rb') as fp:
            return pickle.load(fp)


class SequentialPlayer(NNPlayerBase):
    """ TestPlayer to get action in sequence. Mainly used for testing purposes """
    count = 0
    def __init__(self, pid: str) -> None:
        super().__init__(pid)

    def get_action(self, state: ObsType) -> ActType:
        action = self.count % state.shape[1]
        self.count += 1
        return action

def get_available_cols(state: ObsType) -> List[int]:
    """ Helper function that returns all available moves """
    return [idx for idx, col in enumerate(state.T) if np.count_nonzero(col) < len(col)]


def restore_player(load_dir:Path) -> NNPlayerBase:
    """ TODO:TEST this function
        Restores the latest NNPlayer based on time """
    assert(load_dir), "load_dir is empty"
    pkl_file = sorted(list(load_dir.iterdir()))[-1]
    print(f'Restoring NNPlayer: {pkl_file}')
    return NNPlayerBase.restore_player(pkl_file=pkl_file)