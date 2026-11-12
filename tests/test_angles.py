
import pytest
from types import SimpleNamespace

from biomechanics.angles import (
    calculate_angle,
    get_landmark_point,
    get_pushup_angles
)


def create_landmarks():
    """
    Create 33 simulated MediaPipe landmarks.
    Each landmark has coordinates and confidence values.
    """

    landmarks = [
        SimpleNamespace(
            x=0.0,
            y=0.0,
            visibility=1.0,
            presence=1.0
        )
        for _ in range(33)
    ]

    # Left side
    landmarks[11] = SimpleNamespace(
        x=0.0, y=0.0, visibility=1.0, presence=1.0
    )
    landmarks[13] = SimpleNamespace(
        x=1.0, y=0.0, visibility=1.0, presence=1.0
    )
    landmarks[15] = SimpleNamespace(
        x=2.0, y=0.0, visibility=1.0, presence=1.0
    )

    landmarks[23] = SimpleNamespace(
        x=0.0, y=1.0, visibility=1.0, presence=1.0
    )
    landmarks[25] = SimpleNamespace(
        x=0.0, y=2.0, visibility=1.0, presence=1.0
    )
    landmarks[27] = SimpleNamespace(
        x=0.0, y=3.0, visibility=1.0, presence=1.0
    )

    # Right side
    landmarks[12] = SimpleNamespace(
        x=0.0, y=0.0, visibility=1.0, presence=1.0
    )
    landmarks[14] = SimpleNamespace(
        x=1.0, y=0.0, visibility=1.0, presence=1.0
    )
    landmarks[16] = SimpleNamespace(
        x=2.0, y=0.0, visibility=1.0, presence=1.0
    )

    landmarks[24] = SimpleNamespace(
        x=0.0, y=1.0, visibility=1.0, presence=1.0
    )
    landmarks[26] = SimpleNamespace(
        x=0.0, y=2.0, visibility=1.0, presence=1.0
    )
    landmarks[28] = SimpleNamespace(
        x=0.0, y=3.0, visibility=1.0, presence=1.0
    )

    return landmarks


# Test 1: Right angle
def test_right_angle():
    angle = calculate_angle((1, 0), (0, 0), (0, 1))
    assert angle == pytest.approx(90.0)


# Test 2: Straight angle
def test_straight_angle():
    angle = calculate_angle((0, 0), (1, 0), (2, 0))
    assert angle == pytest.approx(180.0)


# Test 3: Zero angle
def test_zero_angle():
    angle = calculate_angle((2, 0), (1, 0), (3, 0))
    assert angle == pytest.approx(0.0)


# Test 4: Degenerate angle
def test_degenerate_angle():
    angle = calculate_angle((1, 1), (1, 1), (2, 2))
    assert angle is None


# Test 5: Non-finite coordinates
def test_non_finite_coordinates():
    angle = calculate_angle(
        (float("nan"), 0),
        (0, 0),
        (1, 1)
    )
    assert angle is None


# Test 6: Landmark coordinate extraction
def test_get_landmark_point():
    landmarks = create_landmarks()

    point = get_landmark_point(landmarks, 11)

    assert point == (0.0, 0.0)


# Test 7: Push-up angle extraction
def test_get_pushup_angles():
    landmarks = create_landmarks()

    angles = get_pushup_angles(landmarks)

    assert len(angles) == 8
    assert angles["left_elbow"] == pytest.approx(180.0)
    assert angles["right_elbow"] == pytest.approx(180.0)


# Test 8: Low visibility landmark
def test_low_visibility_landmark():
    landmarks = create_landmarks()

    landmarks[11].visibility = 0.2

    point = get_landmark_point(landmarks, 11)

    assert point is None


# Test 9: Low confidence angle
def test_low_confidence_angle():
    landmarks = create_landmarks()

    landmarks[13].visibility = 0.2

    angles = get_pushup_angles(landmarks)

    assert angles["left_elbow"] is None
    assert angles["right_elbow"] is not None
