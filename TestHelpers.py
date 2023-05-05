import pygame
import numpy as np
from PIL import Image
from pathlib import Path

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