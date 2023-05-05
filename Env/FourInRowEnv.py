import numpy as np
from .EnvDefines import *
from Board import Board
from Players import PlayerBase
from gym import Env, spaces
from typing import Tuple, Dict
from enum import Enum

class WLDEnum(Enum):
    WON = 1
    LOST = 2
    DRAWN = 3
    WRONG_MOVE = 4
    CONTINUE = 5

class FourInRowEnv(Env):

    def __init__(self, rows: int = 6, cols: int = 7, render = False) -> None:
        assert(rows > 4), "rows must > 4"
        assert(cols > 4), "cols must > 4"
        self.ngame = -1
        self.shape = (rows, cols)
        self.action_space = spaces.Discrete(cols)
        self.observation_space = spaces.Box(low=-1, high=1, shape=self.shape, dtype=np.int8)
        self.render_env = render
        self.board = Board(rows=self.rows, cols=self.cols, win_at=FOUR)
        self.reset()
        self.trainer:PlayerBase = None

    @property
    def cols(self) -> int:
        return self.shape[1]

    @property
    def rows(self) -> int:
        return self.shape[0]
    
    @property
    def state(self) -> np.ndarray:
        return self.board.b_array
    
    @property
    def state_trainer(self) -> np.ndarray:
        return self.board.b_array_invert
    
    @property
    def moves(self) -> int:
        return self.board.nmove
    
    @property
    def render_labelkey(self) -> dict:
        """ This is required by the BoardGUI for labelling pieces """
        assert(self.trainer is not None), "Trainer has not been set!"
        return  {'-1': self.trainer.id, '1': 'RL'}
    
    @property    
    def stats(self) -> Dict[str, str]:
        """ These are stats required by the GUI """
        return {
            "Game" : str(self.ngame),
            "X_Moves": str(self.nwrong_moves)
        }

    def render(self) -> None:
        def wldenum_descp(val:WLDEnum) -> Tuple[str, tuple]:
            """ Convert the WLDEnum to string info to be displayed """
            if val == WLDEnum.WON:
                return 'Won', (10, 88, 1)
            if val == WLDEnum.LOST:
                return 'Lost', (225, 51, 223)
            if val == WLDEnum.WRONG_MOVE:
                return 'X',  (236, 14, 14)
            if val == WLDEnum.DRAWN:
                return 'DRAW',  (236, 110, 14)
            return '', (0,0,0)
    
        info, color = wldenum_descp(self.info)
        info = {'text':info, 'color':color}
        self.board.render(self.render_labelkey, info, self.stats)
    
    def register_trainer(self, player:PlayerBase) -> None:
        self.trainer = player
        
    def reset(self) -> ObsType:
        self.ngame += 1
        self.nwrong_moves = 0
        self.reset_internals()
        self.board.reset()
        return self.state
    
    def reset_internals(self) -> None:
        self.info = None
        self.done = False
        self.reward = 0

    def learner_step(self, action: ActType) -> bool:
        """ Learner takes turn """
        if not self.done:
            # Reset internals before we proceed with learner step
            self.reset_internals()
            self._act(action=action, isTrainer=False)

    def trainer_step(self) -> None:
        """ Tainer takes the move """
        if not self.done:
            action = self.trainer.get_action(state=self.state_trainer)
            self._act(action=action, isTrainer=True)

    def step(self, action: ActType) -> Tuple[ObsType, int, bool, WLDEnum]:
        self.learner_step(action)
        if self.info != WLDEnum.WRONG_MOVE:
            # Skip the trainer step as wrong move was discovered
            self.trainer_step()
        return self.state, self.reward, self.done, (self.info, self.nwrong_moves)

    def _act(self, action: ActType, isTrainer:bool = False) -> None:
        """ Performs the provided action. Updates the internals for 
            the env once the action is performed. Returns false if wrong move is detected """
        assert self.action_space.contains(action), "Action not part of action_space"
        piece = -1 if isTrainer else 1
        if self.board.add_piece(col=action, piece=piece):
            if self.board.won:
                # Keep track of reward if Trainer won
                self.reward = LostValue if isTrainer else WonValue
                self.done = True
                self.info =  WLDEnum.LOST if isTrainer else WLDEnum.WON
            elif self.board.drawn:
                self.reward = DrawnValue 
                self.done = True
                self.info = WLDEnum.DRAWN
        else:
            if isTrainer:
                assert(False), "Wrong MOVE from trainer!!"
            # Addition of piece was a failure -> Wrong move!
            self.reward = WrongValue
            # self.done = True # TODO: this can kept unset to continue taining with penatly
            self.info = WLDEnum.WRONG_MOVE
            self.nwrong_moves += 1
        
        if self.render_env:
            self.render()
