import pytest
from config import WINDOW_WIDTH
from objects.ball import Ball
"""
This tests for the Ball class in objects.ball.
Covers launch behavior and initial position of the ball.
"""
def test_ball_launch_direction():
    ball = Ball((255, 0, 0), 10, 5)
    ball.launch()
    assert ball.dy == -5
    assert -5 <= ball.dx <= 5 # Tests that the ball launches upward and dx is within range.

def test_ball_initial_position():
    ball = Ball((255, 0, 0), 10, 5)
    assert ball.rect.centerx == WINDOW_WIDTH // 2 # Verifies the ball starts at the horizontal center of the screen.
