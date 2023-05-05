from typing import Literal
import pygame
import numpy as np
from PIL import Image
from pathlib import Path

PieceType = Literal[1, -1]


# GUI defines
# Chanege these to affect the size of of the board!
LINE_WIDTH  = 2
BLOCK_SIZE = 100
BLUE, YELLOW =  (0, 0, 255), (255, 195, 0)
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GOLD, RED = (255, 195, 0), (144, 12, 63)
BRIGHT_RED = (255, 0, 0)
PURPLE, GREEN = (178, 0, 245), (26, 245, 0)


def load_surface(path:Path) -> pygame.Surface:
    """ Helper function to load an image and return it as Surface """
    return pygame.image.load(path)

def compare_images(path1:Path, path2:Path) -> bool:
    """ Returns True is the two images are same """
    assert(path1.exists()), "img1 does not exists"
    assert(path2.exists()), "img2 does not exists"
    img1 = np.array(Image.open(path1), dtype=int)
    img2 = np.array(Image.open(path2), dtype=int)
    return np.allclose(img1, img2)
        