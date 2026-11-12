
import pytest

from biomechanics.smoothing import AngleSmoother


def test_first_value_is_returned_directly():
    smoother = AngleSmoother(alpha=0.3)

    result = smoother.update({
        "left_elbow": 170.0
    })

    assert result["left_elbow"] == pytest.approx(170.0)


def test_ema_smoothing():
    smoother = AngleSmoother(alpha=0.3)

    smoother.update({
        "left_elbow": 170.0
    })

    result = smoother.update({
        "left_elbow": 180.0
    })

    # 0.3 * 180 + 0.7 * 170 = 173
    assert result["left_elbow"] == pytest.approx(173.0)


def test_multiple_angles_are_smoothed_independently():
    smoother = AngleSmoother(alpha=0.5)

    smoother.update({
        "left_elbow": 160.0,
        "right_elbow": 170.0
    })

    result = smoother.update({
        "left_elbow": 180.0,
        "right_elbow": 160.0
    })

    assert result["left_elbow"] == pytest.approx(170.0)
    assert result["right_elbow"] == pytest.approx(165.0)


def test_none_value_does_not_update_previous_value():
    smoother = AngleSmoother(alpha=0.5)

    smoother.update({
        "left_elbow": 160.0
    })

    result = smoother.update({
        "left_elbow": None
    })

    assert result["left_elbow"] is None

    next_result = smoother.update({
        "left_elbow": 180.0
    })

    # Previous valid value is still 160
    assert next_result["left_elbow"] == pytest.approx(170.0)


def test_reset_one_angle():
    smoother = AngleSmoother(alpha=0.5)

    smoother.update({
        "left_elbow": 160.0,
        "right_elbow": 170.0
    })

    smoother.reset("left_elbow")

    result = smoother.update({
        "left_elbow": 180.0,
        "right_elbow": 160.0
    })

    # Left elbow starts fresh
    assert result["left_elbow"] == pytest.approx(180.0)

    # Right elbow continues smoothing
    assert result["right_elbow"] == pytest.approx(165.0)


def test_reset_all_angles():
    smoother = AngleSmoother(alpha=0.5)

    smoother.update({
        "left_elbow": 160.0,
        "right_elbow": 170.0
    })

    smoother.reset()

    result = smoother.update({
        "left_elbow": 180.0,
        "right_elbow": 180.0
    })

    assert result["left_elbow"] == pytest.approx(180.0)
    assert result["right_elbow"] == pytest.approx(180.0)


def test_invalid_alpha():
    with pytest.raises(ValueError):
        AngleSmoother(alpha=0)

    with pytest.raises(ValueError):
        AngleSmoother(alpha=1.5)
