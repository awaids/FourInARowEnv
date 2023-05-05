import numpy as np
from .BoardGUI import BoardGUI
from .BoardDefines import *
from typing import List, Literal, Dict
sliding_window_view = np.lib.stride_tricks.sliding_window_view


class Board:
    """ Class that maintains the board and all its specs """
    def __init__(self, rows: int = 6, cols: int = 7, win_at:int = 4) -> None:
        self.win_at = win_at
        self.shape = (rows, cols)
        self.gui = BoardGUI(rows=rows, cols=cols)
        self.reset()

    def reset(self) -> None:
        self.b_array = np.zeros(shape=self.shape, dtype=np.int8)
        self.nmove = 1  # This has to be set to 1 as this has implication in main

    @property
    def available_cols(self) -> List[int]:
        """ Returns list of columns that are not completely filled """
        return [idx for idx, col in enumerate(self.b_array.T) if np.count_nonzero(col) < len(col)]

    @property
    def rows(self) -> int:
        return self.shape[0]

    @property
    def cols(self) -> int:
        return self.shape[1]

    @property
    def b_array_invert(self) -> np.ndarray:
        """ Useful to get actual board as we invert after each turn to aid learning """
        return self.b_array * -1
    
    @property
    def won(self) -> bool:
        return self._check_win()

    @property
    def drawn(self) -> bool:
        return self._board_filled() and not self.won
    
    def _board_filled(self) -> bool:
        """ Returns True if board is completely filled """
        return np.count_nonzero(self.b_array) >= self.b_array.size

    def _check_win(self) -> bool:
        """ Updates the internal values of won and drawn """
        def found_pattern(b_array:np.ndarray) -> bool:
            """ Returns True if the required pattern found in 2D array """
            assert(b_array.ndim > 1), "2D array expected here"
            for rows in sliding_window_view(b_array, (1, self.win_at)):
                for window in rows:
                    # print(f'window: {window} sum: {abs(np.sum(window))}')
                    if abs(np.sum(window)) == self.win_at:
                        return True
            return False

        def check_diagonal_arr(arr:np.ndarray) -> bool:
            """ Returns True if the diagonals contains a win condition. """
            for i in range(-arr.shape[0] + 1, arr.shape[1]):
                print(f'diag: {np.diag(arr, k=i)} sum: {abs(np.sum(np.diag(arr, k=i))) }')
                if abs(np.sum(np.diag(arr, k=i))) >= self.win_at:
                    return True
            return False
        return found_pattern(self.b_array) | found_pattern(self.b_array.T) | check_diagonal_arr(self.b_array) | check_diagonal_arr(np.fliplr(self.b_array))

    
    def _check_win(self) -> bool:
        """ Returns True if win condition found """
        def found_pattern1(arr:np.ndarray) -> bool:
            """ Returns True if the required pattern found in 1D array """
            assert(arr.ndim == 1), "1D array expected here"
            if arr.shape[0] < self.win_at:
                # If the given array is smaller than the window size
                return False

            # Check all windows for win condition
            for window in sliding_window_view(arr, window_shape=(self.win_at)):
                if abs(np.sum(window)) == self.win_at:
                    return True
            return False

        def get_diagnols(arr:np.ndarray) -> List[np.ndarray]:
            """ Returns 1D arrays of diagonals """
            assert(arr.ndim == 2), "2D array expected here"
            nrows, ncols = arr.shape
            return [np.diag(arr, k=i) for i in range(-nrows + 1, ncols)]

        # check horizontally, vertically, diagonals and flipped diagnols
        for rows in [self.b_array, self.b_array.T, get_diagnols(self.b_array), get_diagnols(np.fliplr(self.b_array))]:
            for row in rows:
                if found_pattern1(row):
                    return True
        return False
    
    def add_piece(self, col:int, piece:PieceType = 1) -> bool:
        """ Adds piece to given col, return False if addition not poosible, updates the board """
        if col not in self.available_cols:
            return False
        # Determine addition index
        at = max(np.where(self.b_array.T[col] == 0)[0])
        self.b_array.T[col, at] = piece
        self.nmove += 1
        return True
    
    def render(self, labelkey:dict, info:dict=None, stats:Dict[str, str]=None) -> None:
        """ Visualizes the complete board, the labelkey must be {'1': str, '-1': str}. This
            way we can differenitatie players. info will be centered on the board"""
        assert(set(labelkey.keys()) == {'1', '-1'}), "label keys missing!"
        self.gui.reset()
        for val, color, label in zip([1, -1], [PURPLE, GREEN], [labelkey['1'], labelkey['-1']]):
            idxs = np.where(self.b_array == val)
            for r_id, c_id in zip(idxs[0], idxs[1]):
                self.gui.draw_piece(row=r_id, col=c_id, color=color, plabel=label)

        if info:
            assert('text' in info.keys()), "info dict missing key(text)"
            assert('color' in info.keys()), "info dict missing key(color)"
            self.gui.add_info(info=info.get('text'), color=info.get('color'))
        
        if stats:
            self.gui.add_stats(stats)
        self.gui.show()