import pytest
from game import Game

def test_game_score_update():
    state = Game()
    state.startup({})
    starting_score = state.game_stats['score']
    state.game_stats['score'] += 100
    assert state.game_stats['score'] == starting_score + 100

def test_game_lives_decrease():
    state = Game()
    state.startup({})
    initial_lives = state.game_stats['lives']
    state.game_stats['lives'] -= 1
    assert state.game_stats['lives'] == initial_lives - 1
