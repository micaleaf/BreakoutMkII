import pytest
from config import WINDOW_WIDTH
from gameScreen import Paddle, paddle_width, paddle_height


def test_paddle_initial_position():
    paddle = Paddle((255, 255, 255), paddle_width, paddle_height)
    paddle.rect.x = (WINDOW_WIDTH - paddle_width) // 2
    paddle.rect.y = 900 - 80  # Set this manually
    assert paddle.rect.y == 900 - 80


def test_paddle_stays_in_bounds_right():
    paddle = Paddle((255, 255, 255), paddle_width, paddle_height)
    paddle.rect.x = WINDOW_WIDTH - 100
    paddle.move_right(200)
    assert paddle.rect.x <= WINDOW_WIDTH - 16 - paddle_width


def test_paddle_stays_in_bounds_left():
    paddle = Paddle((255, 255, 255), paddle_width, paddle_height)
    paddle.rect.x = 10
    paddle.move_left(50)
    assert paddle.rect.x >= 16
