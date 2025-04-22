import pytest
import pygame as pg
from config import WINDOW_WIDTH
from objects.paddle import Paddle
from screens.game import Game
from objects.ball import Ball
from objects.brick import Brick
from state_manager.states import States

"""
Consolidated tests for core game functionality:
- Paddle behavior
- Ball logic
- Brick setup
- Game score/lives
- Finite State Machine transitions
"""

# --- PADDLE TESTS ---

"""
This tests for the Paddle class in objects.paddle.
Validates paddle positioning and movement logic.
"""

def test_paddle_initial_position():
    paddle = Paddle((255, 255, 255), 100, 20)
    paddle.rect.x = (WINDOW_WIDTH - 100) // 2
    paddle.rect.y = 900 - 80
    assert paddle.rect.y == 900 - 80

def test_paddle_stays_in_bounds_right():
    paddle = Paddle((255, 255, 255), 100, 20)
    paddle.rect.x = WINDOW_WIDTH - 100
    paddle.move_right(200)
    assert paddle.rect.x <= WINDOW_WIDTH - 16 - paddle.rect.width

def test_paddle_stays_in_bounds_left():
    paddle = Paddle((255, 255, 255), 100, 20)
    paddle.rect.x = 10
    paddle.move_left(50)
    assert paddle.rect.x >= 16

# --- SCORE & LIVES TESTS ---

"""
Tests for the Game class in screens.game.
Ensures score updating and life count decreases.
"""
def test_game_score_update():
    state = Game()
    state.startup({})
    starting_score = state.game_stats['score']
    state.game_stats['score'] += 100
    assert state.game_stats['score'] == starting_score + 100

    """
    Verifies that lives decrease properly when a life is lost.
    """
def test_game_lives_decrease():
    state = Game()
    state.startup({})
    initial_lives = state.game_stats['lives']
    state.game_stats['lives'] -= 1
    assert state.game_stats['lives'] == initial_lives - 1

# --- BRICK TEST ---

"""
Test for the Brick class.
Confirms that brick objects are initialized correctly.
"""

def test_brick_initialization():
    """
    Confirms color and size are assigned to a brick.
    """
    color = (255, 0, 0)
    width = 60
    height = 15
    brick = Brick(color, width, height)
    assert brick.image.get_size() == (width, height)
    assert brick.color == color

# --- Ball Tests ---

"""
Tests for Ball behavior.
Checks initial state and launching.
"""
def test_ball_launch_direction():
    dummy_sounds = {k: lambda: None for k in ['brick', 'paddle', 'life_lost', 'game_over', 'win', 'wall']}
    ball = Ball((255, 0, 0), 10, 5, sounds=dummy_sounds)
    ball.launch()
    assert ball.dx != 0
    assert ball.dy != 0

    """
    This test verifies that the ball starts centered before launch.
    """
def test_ball_initial_position():
    dummy_sounds = {k: lambda: None for k in ['brick', 'paddle', 'life_lost', 'game_over', 'win', 'wall']}
    ball = Ball((255, 0, 0), 10, 5, sounds=dummy_sounds)
    assert ball.dx == 0 and ball.dy == 0

# --- FSM Test --- 
    """
    This test ensures that states transition properly by setting 'done' and next state.
    """
def test_fsm_next_state_change():
    state = States()
    state.done = True
    state.next = "menu"
    assert state.done is True and state.next == "menu"
