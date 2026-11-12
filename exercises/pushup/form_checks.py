"""Push-up form checks and feedback generation."""

from biomechanics.angles import get_landmark_point


class PushUpFormChecker:
    """
    Checks common push-up form issues using MediaPipe landmarks
    and elbow angles.

    This initial version is designed for a side-facing camera.
    """

    def __init__(
        self,
        min_confidence=0.5,
        hip_deviation_threshold=0.04,
        alignment_angle_threshold=165.0,
        minimum_elbow_angle=95.0
    ):
        self.min_confidence = min_confidence
        self.hip_deviation_threshold = hip_deviation_threshold
        self.alignment_angle_threshold = alignment_angle_threshold
        self.minimum_elbow_angle = minimum_elbow_angle

        self.rep_in_progress = False
        self.minimum_angle_during_rep = None

    def get_reliable_side(self, landmarks):
        """
        Select a side where shoulder, hip and ankle are reliable.

        Prefer the left side. Fall back to the right side.
        """

        left = {
            "shoulder": get_landmark_point(
                landmarks, 11, self.min_confidence
            ),
            "hip": get_landmark_point(
                landmarks, 23, self.min_confidence
            ),
            "ankle": get_landmark_point(
                landmarks, 27, self.min_confidence
            )
        }

        right = {
            "shoulder": get_landmark_point(
                landmarks, 12, self.min_confidence
            ),
            "hip": get_landmark_point(
                landmarks, 24, self.min_confidence
            ),
            "ankle": get_landmark_point(
                landmarks, 28, self.min_confidence
            )
        }

        if all(value is not None for value in left.values()):
            return left

        if all(value is not None for value in right.values()):
            return right

        return None

    def calculate_hip_deviation(self, side):
        """
        Calculate vertical hip deviation from the line joining
        shoulder and ankle.

        Positive deviation = hip is lower in the image (sagging).
        Negative deviation = hip is higher in the image (raised).

        Returns normalized image-coordinate deviation, or None.
        """

        shoulder = side["shoulder"]
        hip = side["hip"]
        ankle = side["ankle"]

        shoulder_x, shoulder_y = shoulder
        hip_x, hip_y = hip
        ankle_x, ankle_y = ankle

        horizontal_distance = ankle_x - shoulder_x

        if abs(horizontal_distance) < 0.05:
            return None

        position = (hip_x - shoulder_x) / horizontal_distance

        expected_hip_y = (
            shoulder_y
            + position * (ankle_y - shoulder_y)
        )

        return hip_y - expected_hip_y

    def get_elbow_angle(self, angles):
        """Use the average of reliable elbow angles, if available."""

        valid_angles = []

        for key in ("left_elbow", "right_elbow"):
            value = angles.get(key)

            if value is None:
                continue

            try:
                value = float(value)

                if 0 <= value <= 180:
                    valid_angles.append(value)

            except (TypeError, ValueError):
                continue

        if not valid_angles:
            return None

        return sum(valid_angles) / len(valid_angles)

    def update_range_of_motion(self, elbow_angle, phase):
        """
        Track the minimum elbow angle during one repetition.

        A completed repetition is flagged as shallow if its
        minimum elbow angle stays above the configured threshold.
        """

        shallow_rep = False

        if phase == "TRACKING_LOST":
            self.rep_in_progress = False
            self.minimum_angle_during_rep = None
            return False

        if phase == "DESCENDING":
            if not self.rep_in_progress:
                self.rep_in_progress = True
                self.minimum_angle_during_rep = None

        if self.rep_in_progress and elbow_angle is not None:
            if self.minimum_angle_during_rep is None:
                self.minimum_angle_during_rep = elbow_angle

            else:
                self.minimum_angle_during_rep = min(
                    self.minimum_angle_during_rep,
                    elbow_angle
                )

        if phase == "TOP" and self.rep_in_progress:
            if self.minimum_angle_during_rep is not None:
                shallow_rep = (
                    self.minimum_angle_during_rep
                    > self.minimum_elbow_angle
                )

            self.rep_in_progress = False
            self.minimum_angle_during_rep = None

        return shallow_rep

    def update(self, landmarks, angles, phase):
        """
        Run all form checks for the current frame.

        Returns a dictionary containing detected issues and
        useful measurements.
        """

        issues = []

        elbow_angle = self.get_elbow_angle(angles)

        shallow_rep = self.update_range_of_motion(
            elbow_angle,
            phase
        )

        if shallow_rep:
            issues.append("incomplete_range_of_motion")

        side = self.get_reliable_side(landmarks)

        if side is None:
            return {
                "issues": issues,
                "hip_deviation": None,
                "body_alignment_angle": None,
                "minimum_elbow_angle": None
            }

        hip_deviation = self.calculate_hip_deviation(side)

        if hip_deviation is not None:
            if hip_deviation > self.hip_deviation_threshold:
                issues.append("sagging_hips")

            elif hip_deviation < -self.hip_deviation_threshold:
                issues.append("raised_hips")

        body_alignment_angle = angles.get(
            "left_body_alignment"
        )

        if body_alignment_angle is None:
            body_alignment_angle = angles.get(
                "right_body_alignment"
            )

        if body_alignment_angle is not None:
            try:
                body_alignment_angle = float(
                    body_alignment_angle
                )

                if not 0 <= body_alignment_angle <= 180:
                    body_alignment_angle = None

            except (TypeError, ValueError):
                body_alignment_angle = None

        if (
            body_alignment_angle is not None
            and body_alignment_angle < self.alignment_angle_threshold
        ):
            issues.append("poor_body_alignment")

        return {
            "issues": issues,
            "hip_deviation": hip_deviation,
            "body_alignment_angle": body_alignment_angle,
            "minimum_elbow_angle": self.minimum_angle_during_rep
        }

    def reset(self):
        """Reset form analysis for a new exercise session."""

        self.rep_in_progress = False
        self.minimum_angle_during_rep = None
