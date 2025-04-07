import pytest
from gameScreen import Ball
from constants import WINDOW_WIDTH

def test_ball_launch_direction():
    ball = Ball((255, 0, 0), 10, 5)
    ball.launch()
    assert ball.dy == -5
    assert -5 <= ball.dx <= 5

def test_ball_initial_position():
    ball = Ball((255, 0, 0), 10, 5)
    assert ball.rect.centerx == WINDOW_WIDTH // 2
