"""Landmark smoothing utilities."""

class AngleSmoother:
    """
    Smooth joint angles using an Exponential Moving Average (EMA).

    Each angle is smoothed independently.
    Missing values return None and do not update the stored value.
    """

    def __init__(self, alpha=0.3):
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be greater than 0 and at most 1")

        self.alpha = alpha
        self.previous_values = {}

    def update(self, angles):
        """
        Accept a dictionary of joint angles and return smoothed angles.

        Example input:
            {
                "left_elbow": 170.0,
                "right_elbow": 175.0
            }
        """

        smoothed_angles = {}

        for name, current_value in angles.items():

            # Do not process missing measurements
            if current_value is None:
                smoothed_angles[name] = None
                continue

            current_value = float(current_value)

            # First measurement: use it directly
            if name not in self.previous_values:
                smoothed_value = current_value

            else:
                previous_value = self.previous_values[name]

                smoothed_value = (
                    self.alpha * current_value
                    + (1 - self.alpha) * previous_value
                )

            self.previous_values[name] = smoothed_value
            smoothed_angles[name] = smoothed_value

        return smoothed_angles

    def reset(self, name=None):
        """
        Reset one angle or all stored angles.

        Useful when tracking is lost or a new exercise starts.
        """

        if name is None:
            self.previous_values.clear()

        else:
            self.previous_values.pop(name, None)
