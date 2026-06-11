import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.elo import expected_score, update_rating, batch_update


def test_expected_score_equal_ratings():
    assert abs(expected_score(1500, 1500) - 0.5) < 1e-9


def test_expected_score_higher_rated_favored():
    score = expected_score(1600, 1500)
    assert score > 0.5


def test_update_rating_win():
    new_rating = update_rating(1500, 1500, result=1.0, k=32)
    assert new_rating == pytest.approx(1516.0, abs=0.1)


def test_update_rating_loss():
    new_rating = update_rating(1500, 1500, result=0.0, k=32)
    assert new_rating == pytest.approx(1484.0, abs=0.1)


def test_update_rating_tie():
    new_rating = update_rating(1500, 1500, result=0.5, k=32)
    assert new_rating == pytest.approx(1500.0, abs=0.1)


def test_batch_update_returns_both():
    winner_new, loser_new = batch_update(1500, 1500, k=32)
    assert winner_new > 1500
    assert loser_new < 1500
    assert abs((winner_new + loser_new) - 3000) < 0.1  # 零和
