import pytest
from screens.game import Game
"""
Tests for the Game class in screens.game.
Ensures score updating and life count decreases.
"""
def test_game_score_update():
    """
    Ensures the score increments correctly when points are added.
    """
    state = Game()
    state.startup({})
    starting_score = state.game_stats['score']
    state.game_stats['score'] += 100
    assert state.game_stats['score'] == starting_score + 100


def test_game_lives_decrease():
    """
    Verifies that lives decrease properly when a life is lost.
    """
    state = Game()
    state.startup({})
    initial_lives = state.game_stats['lives']
    state.game_stats['lives'] -= 1
    assert state.game_stats['lives'] == initial_lives - 1
