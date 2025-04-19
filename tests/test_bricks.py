import pytest
from gameScreen import create_bricks


def test_brick_wall_creation():
    bricks = create_bricks(5, 9)
    assert len(bricks) == 45  # 5 rows x 9 columns
