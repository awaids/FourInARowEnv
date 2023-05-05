import numpy as np
from pathlib import Path
from ..BoardDefines import RED, BLACK, compare_images
from ..Board import Board

class Test_board:
    def test_available_cols(self):
        board = Board(rows=3, cols=4, win_at=2)
        board.b_array = np.array([
            [ 0,  0,  0,  0,],
            [ 0,  0,  0,  0,],
            [ 0,  0,  0,  0,],
        ], dtype=np.int8)
        assert(board.available_cols == [0, 1, 2, 3]), "Unexpected free cols"

        board.b_array = np.array([
            [ 0,  0,  0, -1,],
            [ 1,  0,  0, -1,],
            [ 1,  0,  0, -1,],
        ], dtype=np.int8)
        assert(board.available_cols == [0, 1, 2,]), "Unexpected free cols"

        board.b_array = np.array([
            [ 1,  1, -1, -1,],
            [ 1,  1, -1, -1,],
            [ 1,  1, -1, -1,],
        ], dtype=np.int8)
        assert(board.available_cols == []), "Unexpected free cols"

    def test_rows_cols(self):
        board = Board(rows=3, cols=4, win_at=2)
        assert(board.rows == 3)
        assert(board.cols == 4)
        
    def test_add_piece(self):
        board = Board(rows=3, cols=4, win_at=2)
        
        # CHeck subsequent addtions
        assert(board.add_piece(col=0, piece=-1) == True), "Addition is poosible here"
        ref_b_array =  np.array([
            [ 0,  0,  0,  0,],
            [ 0,  0,  0,  0,],
            [ -1,  0,  0,  0,],
        ], dtype=np.int8)
        assert(np.array_equal(ref_b_array, board.b_array)), "Arrays not the same"

        assert(board.add_piece(col=0, piece=1) == True), "Addition is still poosible here"
        ref_b_array =  np.array([
            [ 0,  0,  0,  0,],
            [ 1,  0,  0,  0,],
            [-1,  0,  0,  0,],
        ], dtype=np.int8)
        assert(np.array_equal(ref_b_array, board.b_array)), "Arrays not the same"

        assert(board.add_piece(col=0, piece=1) == True), "Addition is still poosible here"
        ref_b_array =  np.array([
            [ 1,  0,  0,  0,],
            [ 1,  0,  0,  0,],
            [-1,  0,  0,  0,],
        ], dtype=np.int8)
        assert(np.array_equal(ref_b_array, board.b_array)), "Arrays not the same"

        # Addtion to a filled col
        assert(board.add_piece(col=0, piece=1) == False), "Addition now not possible"

    def test_board_filled(self):
        board = Board(rows=2, cols=2, win_at=3)
        assert(board.drawn == False), "Empty board"

        board.b_array = np.array([
            [ 1,  0,],
            [ 1, -1,],
        ], dtype=np.int8)
        assert(board.drawn == False), "Board still not empty"

        board.b_array = np.array([
            [ 1,  1,],
            [ 1, -1,],
        ], dtype=np.int8)
        assert(board.drawn == True)
        assert(board.won == False)

    def test_won(self):
        board = Board(rows=3, cols=3, win_at=2)
        board.b_array = np.array([
            [ 0,  0,  0],
            [ 0,  0,  0],
            [ 0,  0,  0],
        ], dtype=np.int8)
        assert(board.won == False)

        board.b_array = np.array([
            [ 0,  0,  0],
            [-1,  0,  0],
            [ 1,  1,  0],
        ], dtype=np.int8)
        assert(board.won == True)

        board.b_array = np.array([
            [ 0,  0,  0],
            [-1,  0,  0],
            [ 1,  0,  1],
        ], dtype=np.int8)
        assert(board.won == False)

        board.b_array = np.array([
            [-1,  0,  0],
            [-1,  0,  0],
            [ 1, -1,  1],
        ], dtype=np.int8)
        assert(board.won == True)

        board.b_array = np.array([
            [ 0,  0,  0],
            [-1,  0,  1],
            [ 1, -1,  1],
        ], dtype=np.int8)
        assert(board.won == True)

    def test_get_diagnol_arr(self):
        board = Board(rows=2, cols=3, win_at=2)
        board.b_array = np.array([
            [ 0,  0,  1],
            [-1,  1, -1],
        ], dtype=np.int8)
        assert(board.won == True)

        board.b_array = np.array([
            [ 0, -1,  0],
            [-1,  1, -1],
        ], dtype=np.int8)
        assert(board.won == True)

        board.b_array = np.array([
            [ 0,  0,  0],
            [-1,  1, -1],
        ], dtype=np.int8)
        assert(board.won == False)

        board = Board(rows=3, cols=3, win_at=3)
        board.b_array = np.array([
            [ 1,  0,  0],
            [-1,  1,  0],
            [-1, -1,  1],
        ], dtype=np.int8)
        assert(board.won == True)

        board.b_array = np.array([
            [ 1,  0, -1],
            [-1, -1,  1],
            [-1, -1,  1],
        ], dtype=np.int8)
        assert(board.won == True)

        board.b_array = np.array([
            [ 1,  0,  0],
            [-1, -1,  1],
            [-1, -1,  1],
        ], dtype=np.int8)
        assert(board.won == False)

    def test_regressions(self):
        board = Board(rows=2, cols=2, win_at=2)
        board.b_array = np.array([
            [ 1, 1,-1, 1,-1, 1, 1],
            [-1,-1, 1,-1, 1,-1,-1],
            [ 1, 1,-1, 1,-1, 1,-1],
            [-1, 1, 1, 1, 1, 1,-1],
            [ 1,-1,-1, 1, 1,-1, 1],
            [-1, 1,-1,-1, 1,-1,-1]], dtype=np.int8)
        assert(board.won == True)
        assert(board.drawn == False)

        board.b_array = np.array([
            [ 1,-1, 1, 1,-1, 1, 1],
            [-1, 1,-1,-1,-1, 1, 1],
            [ 1,-1, 1, 1,-1,-1,-1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1, 1,-1,-1, 1,-1, 1],
            [ 1,-1,-1,-1, 1,-1, 1]],dtype=np.int8)
        assert(board.won == True)
        assert(board.drawn == False)

        board.b_array = board.b_array * -1
        assert(board.won == True)
        assert(board.drawn == False)

        board.b_array = np.array([
            [-1,-1, 1,-1, 1, 1, 1],
            [ 1,-1, 1, 1,-1, 1, 1],
            [-1, 1, 1,-1, 1, 1, 1],
            [ 1, 1,-1,-1, 1,-1,-1],
            [-1,-1, 1,-1,-1, 1,-1],
            [ 1,-1,-1, 1,-1, 1,-1]],dtype=np.int8)
        assert(board.won == True)
        assert(board.drawn == False)

    def test_broken_check_win(self):
        board = Board()
        board.b_array = np.array([
            [-1,-1, 1,-1, 0,-1, 1],
            [ 1, 1,-1, 1, 0, 1,-1],
            [ 1,-1, 1, 1, 0,-1,-1],
            [ 1, 1, 1,-1, 1, 1,-1],
            [-1,-1,-1, 1,-1, 1, 1],
            [-1,-1, 1,-1,-1, 1,-1]],dtype=np.int8)
        assert(board.won == False)
        assert(board.drawn == False)

        board.b_array = np.array([
            [-1,-1, 1,-1, 0,-1, 1],
            [ 1, 1,-1, 1, 0, 1,-1],
            [ 1,-1, 1, 1,-1,-1,-1],
            [ 1, 1, 1,-1, 1, 1,-1],
            [-1,-1,-1, 1,-1, 1, 1],
            [-1,-1, 1,-1,-1, 1,-1]],dtype=np.int8)
        assert(board.won == True)
        assert(board.drawn == False)

        board.b_array = np.array([
            [-1,-1, 1,-1, 0,-1, 1],
            [ 1, 1,-1, 1, 0, 1,-1],
            [ 1,-1, 1, 1, 1,-1,-1],
            [ 1, 1, 1,-1, 1, 1,-1],
            [-1,-1,-1, 1,-1, 1, 1],
            [-1,-1, 1,-1,-1, 1,-1]],dtype=np.int8)
        assert(board.won == True)
        assert(board.drawn == False)

def test_BoardGUI_render():
    test_path = Path(__file__).parent / 'test_BoardGUI_render.jpg'
    ref_path = Path(__file__).parent / 'ref_test_BoardGUI_render.jpg'
    board = Board()
    board.b_array = np.array([
            [-1,-1, 1,-1, 0,-1, 1],
            [ 1, 1,-1, 1, 0, 1,-1],
            [ 1,-1, 1, 1, 1,-1,-1],
            [ 1, 1, 1,-1, 1, 1,-1],
            [-1,-1,-1, 1,-1, 1, 1],
            [-1,-1, 1,-1,-1, 1,-1]],dtype=np.int8)
    labelskey = {'1': 'P1', '-1': 'P2'}
    info = {'text': '!test!', 'color': RED}
    board.render(labelskey, info)
    board.gui.save(test_path)
    assert(compare_images(test_path, ref_path)), "Images not equal"
    test_path.unlink()

    # Test if render does not contains the last info
    test_path2 = Path(__file__).parent / 'test_BoardGUI_render2.jpg'
    ref_path2 = Path(__file__).parent / 'ref_test_BoardGUI_render2.jpg'
    info = {'text': '!hello!', 'color': BLACK}
    board.render(labelskey, info)
    board.gui.save(test_path2)
    assert(compare_images(ref_path2, test_path2)), "Images not equal"
    test_path2.unlink()
    

