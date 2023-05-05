import pytest
import numpy as np
from pathlib import Path
from Board import BoardGUI
from ..BoardDefines import *
from TestHelpers import compare_images

class Test_BoardGUI:
    def test_simple_render(self):
        board = BoardGUI(rows=2, cols=1)
        # Need to init here to make sure that screen has been created
        test_path = Path(__file__).parent / 'test_simple_render.jpg'
        ref_path = Path(__file__).parent / 'ref_test_simple_render.jpg'
        board.init()
        board.save(test_path)
        assert(compare_images(ref_path, test_path)), "Images not same"
        test_path.unlink()

    def test_draw_piece_asserts(self):
        """ Checks the asserts of the add piece """
        board = BoardGUI(rows=1, cols=1)
        with pytest.raises(AssertionError):
            board.draw_piece(row=0, col=1, color=PURPLE)
        
        with pytest.raises(AssertionError):
            board.draw_piece(row=1, col=0, color=PURPLE)
        
        with pytest.raises(AssertionError):
            board.draw_piece(row=0, col=-1, color=PURPLE)
        
        with pytest.raises(AssertionError):
            board.draw_piece(row=-1, col=0, color=PURPLE)

    def test_draw_piece(self):
        test_path = Path(__file__).parent / 'test_draw_piece.jpg'
        ref_path = Path(__file__).parent / 'ref_test_draw_piece.jpg'
        board = BoardGUI(rows=2, cols=2)
        board.draw_piece(row=1, col=0, color=PURPLE)
        board.draw_piece(row=1, col=1, color=GREEN)
        board.save(test_path)
        assert(compare_images(test_path, ref_path)), "Images not equal"
        test_path.unlink()

    def test_draw_board(self):
        test_path = Path(__file__).parent / 'test_draw_board.jpg'
        ref_path = Path(__file__).parent / 'ref_test_draw_board.jpg'
        board = BoardGUI(2,2)
        b_array = np.array([
            [ 0, -1], 
            [ 1,  0],
        ], dtype=np.int8)
        board.draw_board(b_array, labelkey={'1': 'p1', '-1': 'p2'})
        board.save(test_path)
        assert(compare_images(test_path, ref_path)), "Images not equal"
        test_path.unlink()

    def test_add_info(self):
        test_path = Path(__file__).parent / 'test_add_info.jpg'
        ref_path = Path(__file__).parent / 'ref_test_add_info.jpg'
        board = BoardGUI(2,2)
        board.add_info(info="Hello", color=BLACK)
        board.save(test_path)
        assert(compare_images(test_path, ref_path)), "Images not equal"
        test_path.unlink()

    def test_add_stats(self):
        test_path = Path(__file__).parent / 'test_add_stats.jpg'
        ref_path = Path(__file__).parent / 'ref_test_add_stats.jpg'
        board = BoardGUI(2,2)
        stats = {'Hello': '25', 'Stats': '00'}
        board.add_stats(stats)
        board.save(test_path)
        assert(compare_images(test_path, ref_path)), "Images not equal"
        test_path.unlink()