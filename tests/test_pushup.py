"""Tests for push-up analysis and repetition counting."""

import pytest

from exercises.pushup.analyzer import PushUpMovementAnalyzer


def create_analyzer():
    return PushUpMovementAnalyzer(
        top_threshold=160.0,
        bottom_threshold=90.0,
        movement_threshold=2.0
    )


def test_initial_top_position():
    analyzer = create_analyzer()

    result = analyzer.update({
        "left_elbow": 175.0,
        "right_elbow": 173.0
    })

    assert result["phase"] == "TOP"
    assert result["elbow_angle"] == pytest.approx(174.0)


def test_initial_bottom_position():
    analyzer = create_analyzer()

    result = analyzer.update({
        "left_elbow": 80.0,
        "right_elbow": 84.0
    })

    assert result["phase"] == "BOTTOM"
    assert result["elbow_angle"] == pytest.approx(82.0)


def test_descending_movement():
    analyzer = create_analyzer()

    analyzer.update({"left_elbow": 175.0})

    result = analyzer.update({"left_elbow": 145.0})

    assert result["phase"] == "DESCENDING"


def test_bottom_position():
    analyzer = create_analyzer()

    analyzer.update({"left_elbow": 175.0})
    analyzer.update({"left_elbow": 145.0})

    result = analyzer.update({"left_elbow": 80.0})

    assert result["phase"] == "BOTTOM"


def test_ascending_movement():
    analyzer = create_analyzer()

    analyzer.update({"left_elbow": 80.0})

    result = analyzer.update({"left_elbow": 120.0})

    assert result["phase"] == "ASCENDING"


def test_top_position_after_ascending():
    analyzer = create_analyzer()

    analyzer.update({"left_elbow": 80.0})
    analyzer.update({"left_elbow": 120.0})

    result = analyzer.update({"left_elbow": 175.0})

    assert result["phase"] == "TOP"


def test_small_angle_fluctuation_does_not_change_phase():
    analyzer = create_analyzer()

    analyzer.update({"left_elbow": 140.0})

    result = analyzer.update({"left_elbow": 141.0})

    assert result["phase"] == "UNKNOWN"


def test_tracking_lost():
    analyzer = create_analyzer()

    analyzer.update({"left_elbow": 175.0})

    result = analyzer.update({
        "left_elbow": None,
        "right_elbow": None
    })

    assert result["phase"] == "TRACKING_LOST"
    assert result["elbow_angle"] is None


def test_tracking_recovers():
    analyzer = create_analyzer()

    analyzer.update({"left_elbow": 175.0})

    analyzer.update({
        "left_elbow": None,
        "right_elbow": None
    })

    result = analyzer.update({"left_elbow": 170.0})

    assert result["phase"] == "TOP"


def test_reset():
    analyzer = create_analyzer()

    analyzer.update({"left_elbow": 175.0})

    analyzer.reset()

    result = analyzer.update({"left_elbow": 120.0})

    assert result["phase"] == "UNKNOWN"


def test_invalid_angle_is_ignored():
    analyzer = create_analyzer()

    result = analyzer.update({
        "left_elbow": 250.0,
        "right_elbow": None
    })

    assert result["phase"] == "TRACKING_LOST"
    assert result["elbow_angle"] is None
