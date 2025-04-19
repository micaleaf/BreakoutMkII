import pytest
from screens.game import create_bricks
"""
This tests for the create_bricks function in screens.game.
Validates that the correct number of bricks are generated.
"""
def test_brick_wall_creation():
    bricks = create_bricks(5, 9)
    assert len(bricks) == 45  # 5 rows x 9 columns
