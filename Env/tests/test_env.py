import pytest
import numpy as np
from pathlib import Path
from ..EnvDefines import *
from .. import FourInRowEnv, WLDEnum
from Players import RandomPlayer, SequentialPlayer
from TestHelpers import compare_images


class Test_FourInRowEnv:
    def test_action_space(self):
        # Check if the action space is correct
        rows, cols = 6, 7
        env = FourInRowEnv(rows=rows, cols=cols, render=False)
        for i in range(cols):
            assert(env.action_space.contains(i))
        with pytest.raises(AssertionError):
            assert(env.action_space.contains(cols))

    def test_register_trainer(self):
        env = FourInRowEnv()
        with pytest.raises(AssertionError):
            _ = env.render_labelkey
        pid = 'TST'
        env.register_trainer(RandomPlayer(pid=pid))
        assert(env.render_labelkey['-1'] == pid), "The id of the trainer is incorrect"

    def test_reset(self):
        env = FourInRowEnv()
        env.reset()
        assert(env.ngame == 1)
        assert(env.nwrong_moves == 0)

    def test_trainer_step(self):
        env = FourInRowEnv()
        env.register_trainer(SequentialPlayer('TST'))
        env.trainer_step()

        # Check internal values
        ref_board = np.array([
            [ 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
        ], dtype=np.int8)
        assert(np.array_equal(ref_board, env.state)), "The trainer step did not update the board"
        assert(env.reward == 0), "Incorrect reward"
        assert(env.info == None), "Incorrect info"
        assert(env.done == False), "Incorrect done"

    def test_act_trainer_win(self):
        env = FourInRowEnv()
        env.register_trainer(RandomPlayer('TST'))
        env.board.b_array = np.array([
            [ 1, 1,-1,-1, 1, 1, 0],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1,-1, 1,-1],
            [-1,-1, 1,-1,-1,-1, 1],
            [ 1, 1, 1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
        ], dtype=np.int8)
        env.trainer_step()
        assert(env.info == WLDEnum.LOST), "Trainer won means that RL lost"
        assert(env.reward == LostValue), "Reward is not correct"
        assert(env.done == True), "Done must be True here"
    
    def test_act_trainer_drawn(self):
        env = FourInRowEnv()
        env.register_trainer(RandomPlayer('TST'))
        env.board.b_array = np.array([
            [ 1, 1,-1,-1, 1, 1, 0],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
        ], dtype=np.int8)
        env.trainer_step()
        assert(env.info == WLDEnum.DRAWN), "Draw was expected here!"
        assert(env.reward == DrawnValue), "Reward is not correct"
        assert(env.done == True), "Done must be True here"
        
    def test_step(self):
        env = FourInRowEnv()
        env.register_trainer(SequentialPlayer('TST'))
        state, reward, done, info = env.step(action=0)
        # Check internal values
        ref_board = np.array([
            [ 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [ 1, 0, 0, 0, 0, 0, 0],
        ], dtype=np.int8)
        wld, wrong_moves = info[0], info[1]
        assert(np.array_equal(ref_board, state)), "The step did not update the board"
        assert(reward == 0), "Incorrect reward"
        assert(wld == None), "Incorrect info"
        assert(wrong_moves == 0), "Incorrect wrong moves"
        assert(done == False), "Incorrect done"   

    def test_step_win(self):
        env = FourInRowEnv()
        env.board.b_array = np.array([
            [ 1, 1,-1,-1, 1, 1, 0],
            [-1,-1, 1, 1,-1, 1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1]
        ], dtype=np.int8)
        env.register_trainer(SequentialPlayer('TST'))
        state, reward, done, info = env.step(action=6)
        # Check internal values
        ref_board = np.array([
            [ 1, 1,-1,-1, 1, 1, 1],
            [-1,-1, 1, 1,-1, 1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1]
        ], dtype=np.int8)
        wld, wrong_moves = info[0], info[1]
        assert(np.array_equal(ref_board, state)), "The step did not update the board"
        assert(reward == WonValue), "Incorrect reward"
        assert(wld == WLDEnum.WON), "Incorrect info"
        assert(wrong_moves == 0), "Incorrect wrong moves"
        assert(done == True), "Incorrect done"   

    def test_step_draw(self):
        env = FourInRowEnv()
        env.board.b_array = np.array([
            [ 1, 1,-1,-1, 1, 1, 0],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1]
        ], dtype=np.int8)
        env.register_trainer(SequentialPlayer('TST'))
        state, reward, done, info = env.step(action=6)
        # Check internal values
        ref_board = np.array([
            [ 1, 1,-1,-1, 1, 1, 1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1]
        ], dtype=np.int8)
        wld, wrong_moves = info[0], info[1]
        assert(np.array_equal(ref_board, state)), "The step did not update the board"
        assert(reward == DrawnValue), "Incorrect reward"
        assert(wld == WLDEnum.DRAWN), "Incorrect info"
        assert(wrong_moves == 0), "Incorrect wrong moves"
        assert(done == True), "Incorrect done" 

    def test_step_wrong_move(self):
        env = FourInRowEnv()
        env.board.b_array = np.array([
            [ 1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [ 1, 0, 0, 0, 0, 0, 0],
            [ 1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [ 1, 0, 0, 0, 0, 0, 0],
        ], dtype=np.int8)
        ref_board = env.board.b_array
        env.register_trainer(SequentialPlayer('TST'))
        state, reward, done, info = env.step(action=0)
        # Check internal values
        wld, wrong_moves = info[0], info[1]
        assert(np.array_equal(ref_board, state)), "The step did not update the board"
        assert(reward == WrongValue), "Incorrect reward"
        assert(wld == WLDEnum.WRONG_MOVE), "Incorrect info"
        assert(wrong_moves == 1), "Incorrect wrong moves"
        assert(done == False), "Incorrect done" 
        
    def test_step_lost(self):
        env = FourInRowEnv()
        env.board.b_array = np.array([
            [ 0, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [ 1, 0, 0, 0, 0, 0, 0],
            [ 1, 0, 0, 0, 0, 0, 0],
        ], dtype=np.int8)
        env.register_trainer(SequentialPlayer('TST'))
        state, reward, done, info = env.step(action=1)
        # Check internal values
        ref_board = np.array([
            [-1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0],
            [ 1, 0, 0, 0, 0, 0, 0],
            [ 1, 1, 0, 0, 0, 0, 0],
        ], dtype=np.int8)
        wld, wrong_moves = info[0], info[1]
        assert(np.array_equal(ref_board, state)), "The step did not update the board"
        assert(reward == LostValue), "Incorrect reward"
        assert(wld == WLDEnum.LOST), "Incorrect info"
        assert(wrong_moves == 0), "Incorrect wrong moves"
        assert(done == True), "Incorrect done" 


class Test_FourInRowEnv_Render:
    def test_step_render_draw(self):
        test_path = Path(__file__).parent / 'test_step_render.jpg'
        ref_path = Path(__file__).parent / 'ref_test_step_render.jpg'
        env = FourInRowEnv(render=False)
        env.board.b_array = np.array([
            [ 1, 1,-1,-1, 1, 1, 0],
            [-1,-1, 1, 1,-1, 1, 0],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1]
        ], dtype=np.int8)
        env.register_trainer(RandomPlayer('TST'))
        env.step(action=6)
        env.render()
        env.board.gui.save(test_path)
        assert(compare_images(ref_path, test_path)), "Images not equal"
        test_path.unlink()
        
    def test_step_render_won(self):
        test_path = Path(__file__).parent / 'test_step_render_won.jpg'
        ref_path = Path(__file__).parent / 'ref_test_step_render_won.jpg'
        env = FourInRowEnv(render=False)
        env.board.b_array = np.array([
            [ 1, 1,-1,-1, 1, 1, 0],
            [-1,-1, 1, 1,-1, 1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1]
        ], dtype=np.int8)
        env.register_trainer(RandomPlayer('TST'))
        env.step(action=6)
        env.render()
        env.board.gui.save(test_path)
        assert(compare_images(ref_path, test_path)), "Images not equal"
        test_path.unlink()

    def test_step_render_lost(self):
        test_path = Path(__file__).parent / 'test_step_render_lost.jpg'
        ref_path = Path(__file__).parent / 'ref_test_step_render_lost.jpg'
        env = FourInRowEnv(render=False)
        env.board.b_array = np.array([
            [ 1, 1, 1,-1,-1,-1, 0],
            [-1,-1, 1, 1,-1, 1, 0],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1]
        ], dtype=np.int8)
        env.register_trainer(RandomPlayer('TST'))
        env.step(action=6)
        env.render()
        env.board.gui.save(test_path)
        assert(compare_images(ref_path, test_path)), "Images not equal"
        test_path.unlink()

    def test_step_render_wrong_move(self):
        test_path = Path(__file__).parent / 'test_step_render_wrong_move.jpg'
        ref_path = Path(__file__).parent / 'ref_test_step_render_wrong_move.jpg'
        env = FourInRowEnv(render=False)
        env.board.b_array = np.array([
            [ 1, 1, 1,-1,-1,-1, 0],
            [-1,-1, 1, 1,-1, 1, 0],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1],
            [ 1, 1,-1,-1, 1, 1,-1],
            [-1,-1, 1, 1,-1,-1, 1]
        ], dtype=np.int8)
        env.register_trainer(RandomPlayer('TST'))
        env.step(action=0)
        env.render()
        env.board.gui.save(test_path)
        assert(compare_images(ref_path, test_path)), "Images not equal"
        test_path.unlink()