import pytest
import pygame as pg
from screens.game import Game
from objects.paddle import Paddle
from objects.ball import Ball
from objects.brick import Brick
from objects.power_item import PowerItem
from unittest.mock import MagicMock, patch

"""
These tests make sure the power-ups in the game do what they are meant to do.
The tests check that things like paddle resizing, ball speed changes, sticky effects, and extra lives all trigger and reset correctly.
"""
pg.init()

@pytest.fixture
def paddle():
    return Paddle(color=(0, 255, 255), width=100, height=20)

@pytest.fixture
def ball():
    dummy_sounds = {
        'brick': MagicMock(),
        'paddle': MagicMock(),
        'life_lost': MagicMock(),
        'game_over': MagicMock(),
        'win': MagicMock(),
        'wall': MagicMock(),
    }
    return Ball(color=(255, 0, 0), radius=10, speed=5, sounds=dummy_sounds)

@pytest.fixture
def dummy_game():
    class DummyGame:
        def __init__(self):
            self.game_stats = {'lives': 2}
            self.laser_mode = False
    return DummyGame()
    
#--- Power Effects ---
"""This test ensures that the power effect item falls when the respected bricks are broken."""
def test_power_item_falls():
    start_y = 100
    item = PowerItem(50, start_y, 'sticky', speed=5)

    # Call update a few times
    for _ in range(3):
        item.update()

    # After 3 updates, y should have increased by 3 * speed
    expected_y = start_y + (3 * item.speed)
    assert item.rect.centery == expected_y

"""This test ensures a power-up item spawns when a brick is hit and the random condition is met."""
def test_powerup_spawns_on_brick_hit():
    game = Game()
    game.startup({})

    # Set up a brick and make sure it's positioned to collide with the ball
    brick = Brick((255, 0, 0), 60, 15)
    brick.rect.center = (100, 100)
    game.brick_wall.add(brick)
    game.all_sprites.add(brick)

    game.ball.rect.center = brick.rect.center  # Force collision

    # Force a power-up to spawn and make sure it's the 'sticky' one
    with patch('random.random', return_value=0.1):  # Ensure power-up spawns
        with patch('random.choice', return_value='sticky'):
            game._handle_collisions()

    # Assert that at least one power-up is in the group
    assert any(isinstance(sprite, PowerItem) for sprite in game.power_items)
    
# --- Paddle Size Power-Ups ---
"""This test ensures that the paddle's width increases after the 'expand' power-up is applied."""
def test_expand_paddle(paddle, ball):
    power = PowerItem(100, 100, 'expand')
    effect = power.apply_effect(paddle=paddle, ball=ball)
    assert paddle.rect.width > paddle.original_width
    assert effect == 'expand'

"""This test ensures that the paddle's width decreases after the 'shrink' power-up is applied."""
def test_shrink_paddle(paddle, ball):
    power = PowerItem(100, 100, 'shrink')
    effect = power.apply_effect(paddle=paddle, ball=ball)
    assert paddle.rect.width < paddle.original_width
    assert effect == 'shrink'

"""This test ensures the paddle size goes back to its original size after calling reset_size()."""
def test_reset_paddle_size(paddle, ball):
    power = PowerItem(100, 100, 'expand')
    power.apply_effect(paddle=paddle, ball=ball)
    paddle.reset_size()
    assert paddle.rect.width == paddle.original_width

# --- Ball Power-Ups ---
"""This test ensures the ball's speed increases after the 'fast_ball' power-up is applied."""
def test_fast_ball(paddle, ball):
    ball.launch()  # Set initial dx/dy so we can measure speed
    original_speed = abs(ball.dx)
    power = PowerItem(100, 100, 'fast_ball')
    effect = power.apply_effect(paddle=paddle, ball=ball)
    assert abs(ball.dx) > original_speed or abs(ball.dy) > original_speed
    assert effect == 'fast_ball'

"""This test ensures the ball returns to its original speed after calling reset_speed()."""
def test_reset_ball_speed(paddle, ball):
    power = PowerItem(100, 100, 'fast_ball')
    power.apply_effect(paddle=paddle, ball=ball)
    ball.reset_speed()
    assert abs(ball.dx) == ball.original_speed
    assert abs(ball.dy) == ball.original_speed

"""This test ensures the 'sticky' attribute is set to True on the ball after the sticky power-up is applied."""
def test_sticky_ball(paddle, ball):
    power = PowerItem(100, 100, 'sticky')
    effect = power.apply_effect(paddle=paddle, ball=ball)
    assert hasattr(ball, 'sticky') and ball.sticky is True
    assert effect == 'sticky'

# --- Extra Lives and Laser Power Up ---
"""This test ensures an extra life is added to the game stats when the 'extra_life' power-up is applied."""
def test_extra_life(paddle, ball, dummy_game):
    power = PowerItem(100, 100, 'extra_life')
    effect = power.apply_effect(paddle=paddle, ball=ball, game=dummy_game)
    assert dummy_game.game_stats['lives'] == 3
    assert effect == 'extra_life'

"""This test ensures the 'laser' power-up sets laser_mode to True in the game."""
def test_laser_powerup(paddle, ball, dummy_game):
    power = PowerItem(100, 100, 'laser')
    effect = power.apply_effect(paddle=paddle, ball=ball, game=dummy_game)
    assert dummy_game.laser_mode is True
    assert effect == 'laser'
