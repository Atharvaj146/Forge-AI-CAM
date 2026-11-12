"""Push-up movement and form analysis."""

import math


class PushUpMovementAnalyzer:
    """
    Identifies the current phase of a push-up using elbow angles.

    Phases:
        UNKNOWN
        TOP
        DESCENDING
        BOTTOM
        ASCENDING
        TRACKING_LOST
    """

    def __init__(
        self,
        top_threshold=160.0,
        bottom_threshold=90.0,
        movement_threshold=2.0
    ):
        if not 0 <= bottom_threshold < top_threshold <= 180:
            raise ValueError("Invalid elbow angle thresholds")

        if movement_threshold < 0:
            raise ValueError("movement_threshold cannot be negative")

        self.top_threshold = top_threshold
        self.bottom_threshold = bottom_threshold
        self.movement_threshold = movement_threshold

        self.previous_angle = None
        self.current_phase = "UNKNOWN"

    def select_elbow_angle(self, angles):
        """
        Select a usable elbow angle.

        If both sides are available, use their average.
        If only one side is available, use that side.
        """

        left = angles.get("left_elbow")
        right = angles.get("right_elbow")

        valid_angles = []

        for value in (left, right):
            if value is None:
                continue

            try:
                value = float(value)

                if math.isfinite(value) and 0 <= value <= 180:
                    valid_angles.append(value)

            except (TypeError, ValueError):
                continue

        if not valid_angles:
            return None

        return sum(valid_angles) / len(valid_angles)

    def update(self, angles):
        """
        Process one frame of joint angles.

        Returns:
            {
                "phase": current movement phase,
                "elbow_angle": selected elbow angle
            }
        """

        elbow_angle = self.select_elbow_angle(angles)

        # No reliable elbow measurement
        if elbow_angle is None:
            self.previous_angle = None
            self.current_phase = "TRACKING_LOST"

            return {
                "phase": self.current_phase,
                "elbow_angle": None
            }

        # First valid measurement after initialization or tracking loss
        if self.previous_angle is None:

            if elbow_angle >= self.top_threshold:
                self.current_phase = "TOP"

            elif elbow_angle <= self.bottom_threshold:
                self.current_phase = "BOTTOM"

            else:
                self.current_phase = "UNKNOWN"

        # Determine movement direction
        else:
            difference = elbow_angle - self.previous_angle

            if elbow_angle >= self.top_threshold:
                self.current_phase = "TOP"

            elif elbow_angle <= self.bottom_threshold:
                self.current_phase = "BOTTOM"

            elif difference < -self.movement_threshold:
                self.current_phase = "DESCENDING"

            elif difference > self.movement_threshold:
                self.current_phase = "ASCENDING"

            # Otherwise retain the previous phase.
            # This prevents tiny angle fluctuations from changing the phase.

        self.previous_angle = elbow_angle

        return {
            "phase": self.current_phase,
            "elbow_angle": elbow_angle
        }

    def reset(self):
        """Reset movement analysis before a new exercise session."""

        self.previous_angle = None
        self.current_phase = "UNKNOWN"
