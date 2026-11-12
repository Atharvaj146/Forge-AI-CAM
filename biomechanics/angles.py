
import math


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate angle ABC in degrees.
    B is the vertex.
    Returns an angle between 0 and 180 degrees.
    Returns None for invalid coordinates.
    """

    try:
        ax, ay = float(point_a[0]), float(point_a[1])
        bx, by = float(point_b[0]), float(point_b[1])
        cx, cy = float(point_c[0]), float(point_c[1])

        coordinates = (ax, ay, bx, by, cx, cy)

        if not all(math.isfinite(value) for value in coordinates):
            return None

        vector_ba = (ax - bx, ay - by)
        vector_bc = (cx - bx, cy - by)

        dot_product = (
            vector_ba[0] * vector_bc[0]
            + vector_ba[1] * vector_bc[1]
        )

        magnitude_ba = math.hypot(*vector_ba)
        magnitude_bc = math.hypot(*vector_bc)

        if magnitude_ba == 0 or magnitude_bc == 0:
            return None

        cosine = dot_product / (magnitude_ba * magnitude_bc)
        cosine = max(-1.0, min(1.0, cosine))

        return math.degrees(math.acos(cosine))

    except (TypeError, ValueError, IndexError, OverflowError):
        return None


def get_landmark_point(landmarks, landmark_index, min_confidence=0.5):
    """
    Extract x and y coordinates only when landmark confidence
    is sufficient.

    Returns:
        (x, y) if reliable
        None if unreliable or invalid
    """

    try:
        landmark = landmarks[landmark_index]

        visibility = getattr(landmark, "visibility", None)
        presence = getattr(landmark, "presence", None)

        confidence_values = [
            value
            for value in (visibility, presence)
            if value is not None
        ]

        # Reject if confidence information is unavailable
        if not confidence_values:
            return None

        # Validate available confidence values
        for confidence in confidence_values:
            confidence = float(confidence)

            if not math.isfinite(confidence):
                return None

            if confidence < min_confidence:
                return None

        x = float(landmark.x)
        y = float(landmark.y)

        if not math.isfinite(x) or not math.isfinite(y):
            return None

        return (x, y)

    except (TypeError, ValueError, IndexError, AttributeError):
        return None


def get_pushup_angles(landmarks, min_confidence=0.5):
    """
    Calculate important joint angles for push-up analysis.

    MediaPipe landmark indices:
    11, 12 = Shoulders
    13, 14 = Elbows
    15, 16 = Wrists
    23, 24 = Hips
    25, 26 = Knees
    27, 28 = Ankles
    """

    def point(index):
        return get_landmark_point(
            landmarks,
            index,
            min_confidence
        )

    # Extract reliable landmarks
    left_shoulder = point(11)
    right_shoulder = point(12)

    left_elbow = point(13)
    right_elbow = point(14)

    left_wrist = point(15)
    right_wrist = point(16)

    left_hip = point(23)
    right_hip = point(24)

    left_knee = point(25)
    right_knee = point(26)

    left_ankle = point(27)
    right_ankle = point(28)

    # Calculate joint angles
    angles = {
        "left_elbow": calculate_angle(
            left_shoulder, left_elbow, left_wrist
        ),

        "right_elbow": calculate_angle(
            right_shoulder, right_elbow, right_wrist
        ),

        "left_shoulder": calculate_angle(
            left_elbow, left_shoulder, left_hip
        ),

        "right_shoulder": calculate_angle(
            right_elbow, right_shoulder, right_hip
        ),

        "left_hip": calculate_angle(
            left_shoulder, left_hip, left_knee
        ),

        "right_hip": calculate_angle(
            right_shoulder, right_hip, right_knee
        ),

        "left_body_alignment": calculate_angle(
            left_shoulder, left_hip, left_ankle
        ),

        "right_body_alignment": calculate_angle(
            right_shoulder, right_hip, right_ankle
        )
    }

    return angles
