
from types import SimpleNamespace

from exercises.pushup.form_checks import PushUpFormChecker


def create_landmarks(
    shoulder=(0.1, 0.5),
    hip=(0.5, 0.5),
    ankle=(0.9, 0.5)
):
    """Create simulated landmarks with high confidence."""

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
        x=shoulder[0], y=shoulder[1],
        visibility=1.0, presence=1.0
    )
    landmarks[23] = SimpleNamespace(
        x=hip[0], y=hip[1],
        visibility=1.0, presence=1.0
    )
    landmarks[27] = SimpleNamespace(
        x=ankle[0], y=ankle[1],
        visibility=1.0, presence=1.0
    )

    # Right side
    landmarks[12] = SimpleNamespace(
        x=shoulder[0], y=shoulder[1],
        visibility=1.0, presence=1.0
    )
    landmarks[24] = SimpleNamespace(
        x=hip[0], y=hip[1],
        visibility=1.0, presence=1.0
    )
    landmarks[28] = SimpleNamespace(
        x=ankle[0], y=ankle[1],
        visibility=1.0, presence=1.0
    )

    return landmarks


def create_angles(
    left_elbow=170.0,
    right_elbow=170.0,
    body_alignment=180.0
):
    return {
        "left_elbow": left_elbow,
        "right_elbow": right_elbow,
        "left_body_alignment": body_alignment,
        "right_body_alignment": body_alignment
    }


def test_good_pushup_alignment():
    checker = PushUpFormChecker()

    landmarks = create_landmarks()
    angles = create_angles()

    result = checker.update(landmarks, angles, "TOP")

    assert result["issues"] == []
    assert result["hip_deviation"] == 0.0
    assert result["body_alignment_angle"] == 180.0


def test_sagging_hips():
    checker = PushUpFormChecker()

    landmarks = create_landmarks(
        hip=(0.5, 0.6)
    )

    result = checker.update(
        landmarks,
        create_angles(),
        "TOP"
    )

    assert "sagging_hips" in result["issues"]


def test_raised_hips():
    checker = PushUpFormChecker()

    landmarks = create_landmarks(
        hip=(0.5, 0.4)
    )

    result = checker.update(
        landmarks,
        create_angles(),
        "TOP"
    )

    assert "raised_hips" in result["issues"]


def test_poor_body_alignment():
    checker = PushUpFormChecker()

    result = checker.update(
        create_landmarks(),
        create_angles(body_alignment=150.0),
        "TOP"
    )

    assert "poor_body_alignment" in result["issues"]


def test_unreliable_left_side_uses_right_side():
    checker = PushUpFormChecker()

    landmarks = create_landmarks(
        hip=(0.5, 0.6)
    )

    # Make left-side landmarks unreliable
    landmarks[11].visibility = 0.2
    landmarks[23].visibility = 0.2
    landmarks[27].visibility = 0.2

    result = checker.update(
        landmarks,
        create_angles(),
        "TOP"
    )

    # The right side has the same simulated hip position.
    assert "sagging_hips" in result["issues"]


def test_missing_both_sides():
    checker = PushUpFormChecker()

    landmarks = create_landmarks()

    for index in (11, 23, 27, 12, 24, 28):
        landmarks[index].visibility = 0.2

    result = checker.update(
        landmarks,
        create_angles(),
        "TOP"
    )

    assert result["hip_deviation"] is None
    assert result["body_alignment_angle"] is None


def test_incomplete_range_of_motion():
    checker = PushUpFormChecker()

    landmarks = create_landmarks()

    checker.update(
        landmarks,
        create_angles(left_elbow=120, right_elbow=120),
        "DESCENDING"
    )

    checker.update(
        landmarks,
        create_angles(left_elbow=105, right_elbow=105),
        "BOTTOM"
    )

    checker.update(
        landmarks,
        create_angles(left_elbow=130, right_elbow=130),
        "ASCENDING"
    )

    result = checker.update(
        landmarks,
        create_angles(left_elbow=175, right_elbow=175),
        "TOP"
    )

    assert "incomplete_range_of_motion" in result["issues"]


def test_sufficient_range_of_motion():
    checker = PushUpFormChecker()

    landmarks = create_landmarks()

    checker.update(
        landmarks,
        create_angles(left_elbow=120, right_elbow=120),
        "DESCENDING"
    )

    checker.update(
        landmarks,
        create_angles(left_elbow=75, right_elbow=75),
        "BOTTOM"
    )

    checker.update(
        landmarks,
        create_angles(left_elbow=130, right_elbow=130),
        "ASCENDING"
    )

    result = checker.update(
        landmarks,
        create_angles(left_elbow=175, right_elbow=175),
        "TOP"
    )

    assert "incomplete_range_of_motion" not in result["issues"]


def test_tracking_loss_resets_range_tracking():
    checker = PushUpFormChecker()

    landmarks = create_landmarks()

    checker.update(
        landmarks,
        create_angles(left_elbow=120, right_elbow=120),
        "DESCENDING"
    )

    checker.update(
        landmarks,
        create_angles(left_elbow=80, right_elbow=80),
        "BOTTOM"
    )

    result = checker.update(
        landmarks,
        create_angles(),
        "TRACKING_LOST"
    )

    assert checker.rep_in_progress is False
    assert checker.minimum_angle_during_rep is None
    assert "incomplete_range_of_motion" not in result["issues"]


def test_reset():
    checker = PushUpFormChecker()

    landmarks = create_landmarks()

    checker.update(
        landmarks,
        create_angles(),
        "DESCENDING"
    )

    checker.reset()

    assert checker.rep_in_progress is False
    assert checker.minimum_angle_during_rep is None
