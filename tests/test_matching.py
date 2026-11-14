import numpy as np
import pytest

from analog.matching import great_circle_km, select_separated, terrain_distance


def test_missing_features_cannot_win():
    d = terrain_distance([[np.nan, 1, 20], [1, 2, 30]], [1, 2, 30])
    assert np.isinf(d[0]) and d[1] == 0


def test_explicit_distance_is_hand_checkable():
    assert terrain_distance([2, 4, 1000], [1, 2, 500]) == pytest.approx(1.0)


def test_duplicate_and_nearby_centres_do_not_fill_shortlist():
    indices = select_separated(
        np.array([0, 0, 0, 10]), np.array([0, 0, 0.1, 0]), np.array([0, 0.1, 0.2, 0.3]), 2, 300
    )
    assert indices == [0, 3]


def test_dateline_distance_uses_short_route():
    assert great_circle_km(0, 179, 0, -179) == pytest.approx(222.39, abs=0.1)


@pytest.mark.parametrize("weights", [[0, 0, 0], [-1, 1, 1], [np.nan, 1, 1]])
def test_invalid_weights_fail(weights):
    with pytest.raises(ValueError):
        terrain_distance([0, 0, 0], [0, 0, 0], weights=weights)


def test_empty_valid_candidates_returns_empty():
    assert select_separated(np.array([0]), np.array([0]), np.array([np.inf])) == []
