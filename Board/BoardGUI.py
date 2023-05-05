import pygame
import numpy as np
from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple, Dict
from .BoardDefines import *

@dataclass
class BoardInfo:
    """ Class to maintaint the info/stats to show """
    ptxt:str = ''
    info: dict = field(default_factory=dict) 
    stats: dict = field(default_factory=dict) 

class BoardGUI:
    def __init__(self, rows:int, cols:int) -> None:
        self.rows, self.cols = rows, cols
        self.pradius = BLOCK_SIZE/2 - (BLOCK_SIZE * 0.05)
        self.x = self.cols * BLOCK_SIZE + LINE_WIDTH
        self.y = self.rows * BLOCK_SIZE + LINE_WIDTH

    def __del__(self):
        if pygame.get_init():
            pygame.display.quit()
            pygame.quit() 

    def init(self) -> None:
        pygame.init()
        pygame.font.init()
        self._piece_font = pygame.font.SysFont("arial", int(BLOCK_SIZE / 2))
        self._font = pygame.font.SysFont("arial", int(self.y / 2))
        self._stat_font = pygame.font.SysFont("freesansbold", int(BLOCK_SIZE / 2.5))
        self._surface = pygame.display.set_mode((self.x, self.y))
        self.reset()

    @property
    def surface(self) -> pygame.Surface:
        """ This way we dont initialize pygame until required """
        if not pygame.get_init():
            self.init()
        return self._surface

    @property
    def font(self) -> pygame.font:
        if not pygame.get_init():
            self.init()
        return self._font
    
    @property
    def stat_font(self) -> pygame.font:
        if not pygame.get_init():
            self.init()
        return self._stat_font
    
    @property
    def piece_font(self) -> pygame.font:
        if not pygame.get_init():
            self.init()
        return self._piece_font

    def reset(self) -> None:
        """ Resets the surface """
        self._fill_background()
        self._add_border_lines()
        self._add_white_pieces()
    
    def _fill_background(self) -> None:
        """ Fills the backgound of the surface wit BLUE color """
        self.surface.fill(BLUE)

    def _add_border_lines(self) -> None:
        """ Adds Yellow lines as boarders """
        for r_id in range(self.rows+2):
            r_pos = r_id * BLOCK_SIZE
            pygame.draw.line(self.surface, YELLOW, (r_pos, 0), (r_pos, self.y), LINE_WIDTH)
        for c_id in range(self.cols+2):
            c_pos = c_id * BLOCK_SIZE
            pygame.draw.line(self.surface, YELLOW, (0, c_pos), (self.x, c_pos), LINE_WIDTH)
    
    def _add_white_pieces(self) -> None:
        """ Resets the surface by adding white peieces """
        for c_id in range(self.cols):
            for r_id in range(self.rows):
                self.draw_piece(r_id, c_id, WHITE)

    def show(self):
        pygame.display.flip()
        pygame.event.pump()
    
    def draw_piece(self, row:int, col:int, color:tuple, plabel:str=None) -> None:
        """ Adds a single piece """
        assert(row >=0 and row < self.rows), "Incorrect row recieved"
        assert(col >=0 and col < self.cols), "Incorrect col recieved"
        x = col * BLOCK_SIZE + BLOCK_SIZE / 2
        y = row * BLOCK_SIZE + BLOCK_SIZE / 2
        pygame.draw.circle(self.surface, color, (x, y), self.pradius)

        # Add label to the piece
        if plabel:
            text_render = self.piece_font.render(plabel, True, WHITE)
            self.surface.blit(text_render, text_render.get_rect(center = (x, y)))
        pygame.event.pump()

    def draw_board(self, b_array:np.array, labelkey:dict) -> None:
        """ Visualizes the complete board """
        assert(set(labelkey.keys()) == {'1', '-1'}), "label keys missing!"
        for val, color, label in zip([1, -1], [PURPLE, GREEN], [labelkey['1'], labelkey['-1']]):
            idxs = np.where(b_array == val)
            for r_id, c_id in zip(idxs[0], idxs[1]):
                self.draw_piece(row=r_id, col=c_id, color=color, plabel=label)
        pygame.event.pump()

    def add_info(self, info:str, color:tuple) -> None:
        """ Add the given text to surface """
        text = self.font.render(info, True, color)
        text_rect = text.get_rect(center=(self.x/2, self.y/2))
        self.surface.blit(text, text_rect)
        pygame.event.pump()

    def add_stats(self, stats:Dict[str,str]) -> None:
        """ Add stats to the top left corner """
        x, y = 0, 0
        for k, v in stats.items():
            text = self.stat_font.render(f'{k}: {v}', True, BRIGHT_RED)
            self.surface.blit(text, (x, y))
            y += self.stat_font.get_height() 

    def save(self, path:Path) -> None:
        """ Saves current surface as jpg """
        assert(path.suffix == '.jpg'), "Extension must be .jpg"
        pygame.image.save(self.surface, path)