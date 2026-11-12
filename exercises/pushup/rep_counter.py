"""Push-up repetition state machine."""

class PushUpRepCounter:
    """
    Counts completed push-up repetitions using a state machine.

    A valid repetition requires:
    TOP -> DESCENDING -> BOTTOM -> ASCENDING -> TOP
    """

    def __init__(self):
        self.rep_count = 0
        self.state = "WAITING_FOR_TOP"

    def update(self, phase):
        """
        Process the movement phase from PushUpMovementAnalyzer.

        Returns:
            {
                "rep_count": total completed repetitions,
                "state": current counter state,
                "rep_completed": whether a rep was counted
            }
        """

        rep_completed = False

        # Tracking loss invalidates the current incomplete repetition.
        if phase == "TRACKING_LOST":
            self.state = "WAITING_FOR_TOP"

            return {
                "rep_count": self.rep_count,
                "state": self.state,
                "rep_completed": False
            }

        # Ignore unknown or invalid phases.
        valid_phases = {
            "TOP",
            "DESCENDING",
            "BOTTOM",
            "ASCENDING"
        }

        if phase not in valid_phases:
            return {
                "rep_count": self.rep_count,
                "state": self.state,
                "rep_completed": False
            }

        # Wait until the user reaches the starting position.
        if self.state == "WAITING_FOR_TOP":

            if phase == "TOP":
                self.state = "READY"

        # A repetition can begin only from TOP.
        elif self.state == "READY":

            if phase == "DESCENDING":
                self.state = "DESCENDING"

        # Wait until the bottom position is reached.
        elif self.state == "DESCENDING":

            if phase == "BOTTOM":
                self.state = "BOTTOM"

            elif phase == "TOP":
                # User returned to the top without reaching bottom.
                self.state = "READY"

        # Wait for upward movement.
        elif self.state == "BOTTOM":

            if phase == "ASCENDING":
                self.state = "ASCENDING"

        # Count only after returning to the top.
        elif self.state == "ASCENDING":

            if phase == "TOP":
                self.rep_count += 1
                rep_completed = True
                self.state = "READY"

            elif phase == "BOTTOM":
                # User moved back down before completing the rep.
                self.state = "BOTTOM"

        return {
            "rep_count": self.rep_count,
            "state": self.state,
            "rep_completed": rep_completed
        }

    def reset(self):
        """Reset the count and state for a new workout session."""

        self.rep_count = 0
        self.state = "WAITING_FOR_TOP"
