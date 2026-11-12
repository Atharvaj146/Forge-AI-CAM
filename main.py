
import cv2
import mediapipe as mp
import time

from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from biomechanics.angles import get_pushup_angles
from biomechanics.smoothing import AngleSmoother

from exercises.pushup.analyzer import PushUpMovementAnalyzer
from exercises.pushup.rep_counter import PushUpRepCounter
from exercises.pushup.form_checks import PushUpFormChecker


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "pose_landmarker_full.task"

CAMERA_INDEX = 0
MIN_CONFIDENCE = 0.5


if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Pose model not found: {MODEL_PATH}")


# Initialize all tracking components
angle_smoother = AngleSmoother(alpha=0.3)
movement_analyzer = PushUpMovementAnalyzer()
rep_counter = PushUpRepCounter()

form_checker = PushUpFormChecker(
    min_confidence=MIN_CONFIDENCE
)


POSE_CONNECTIONS = [
    (11, 12), (11, 13), (13, 15),
    (12, 14), (14, 16),
    (11, 23), (12, 24), (23, 24),
    (23, 25), (25, 27),
    (24, 26), (26, 28)
]


def draw_pose(frame, landmarks):

    height, width, _ = frame.shape

    def is_visible(index):

        landmark = landmarks[index]
        visibility = getattr(landmark, "visibility", None)

        if visibility is None:
            return True

        try:
            return float(visibility) >= MIN_CONFIDENCE
        except (TypeError, ValueError):
            return False

    for start, end in POSE_CONNECTIONS:

        if not is_visible(start) or not is_visible(end):
            continue

        point_a = landmarks[start]
        point_b = landmarks[end]

        x1 = int(point_a.x * width)
        y1 = int(point_a.y * height)

        x2 = int(point_b.x * width)
        y2 = int(point_b.y * height)

        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

    for index, landmark in enumerate(landmarks):

        if not is_visible(index):
            continue

        x = int(landmark.x * width)
        y = int(landmark.y * height)

        cv2.circle(
            frame,
            (x, y),
            5,
            (0, 0, 255),
            -1
        )


def draw_text(frame, text, position, color=(255, 255, 255)):

    cv2.putText(
        frame,
        str(text),
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
        cv2.LINE_AA
    )


def get_feedback_message(issues):

    messages = {
        "sagging_hips": "Raise your hips - avoid sagging",
        "raised_hips": "Lower your hips - maintain body alignment",
        "poor_body_alignment": "Improve your body alignment",
        "incomplete_range_of_motion": "Go lower for full range of motion"
    }

    if not issues:
        return "Good form detected"

    return messages.get(issues[0], "Check your form")


def draw_dashboard(frame, rep_count, phase, elbow_angle, feedback):

    draw_text(
        frame,
        f"Push-ups: {rep_count}",
        (20, 40),
        (0, 255, 0)
    )

    draw_text(
        frame,
        f"Phase: {phase}",
        (20, 80)
    )

    if elbow_angle is not None:

        draw_text(
            frame,
            f"Elbow Angle: {elbow_angle:.1f}",
            (20, 120)
        )

    else:

        draw_text(
            frame,
            "Elbow Angle: unavailable",
            (20, 120),
            (0, 165, 255)
        )

    draw_text(
        frame,
        f"Feedback: {feedback}",
        (20, 165),
        (0, 255, 255)
    )

    draw_text(
        frame,
        "Press Q to quit",
        (20, frame.shape[0] - 20)
    )


def process_frame(frame, landmarker, timestamp_ms):

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    result = landmarker.detect_for_video(
        mp_image,
        timestamp_ms
    )

    # CASE 1: No person detected
    if not result.pose_landmarks:

        # Only reset tracking when pose is actually lost
        phase_result = movement_analyzer.update({
            "left_elbow": None,
            "right_elbow": None
        })

        angle_smoother.reset()

        counter_result = rep_counter.update(
            phase_result["phase"]
        )

        form_checker.update(
            [],
            {},
            phase_result["phase"]
        )

        feedback = "Move into camera view"

        draw_dashboard(
            frame,
            counter_result["rep_count"],
            phase_result["phase"],
            None,
            feedback
        )

        return frame

    # CASE 2: Person detected

    landmarks = result.pose_landmarks[0]

    # Calculate raw joint angles
    raw_angles = get_pushup_angles(
        landmarks,
        min_confidence=MIN_CONFIDENCE
    )

    # Smooth the angles
    smoothed_angles = angle_smoother.update(
        raw_angles
    )

    # IMPORTANT:
    # Update movement analyzer only once per frame.
    # This preserves the previous elbow angle.
    phase_result = movement_analyzer.update(
        smoothed_angles
    )

    current_phase = phase_result["phase"]

    # Count completed repetitions
    counter_result = rep_counter.update(
        current_phase
    )

    # Check exercise form
    form_result = form_checker.update(
        landmarks,
        smoothed_angles,
        current_phase
    )

    feedback = get_feedback_message(
        form_result["issues"]
    )

    # Draw pose and dashboard
    draw_pose(frame, landmarks)

    draw_dashboard(
        frame,
        counter_result["rep_count"],
        current_phase,
        phase_result["elbow_angle"],
        feedback
    )

    return frame


def main():

    print("----------------------------------")
    print("FORGE AI CAM")
    print("Push-up Tracking System")
    print("----------------------------------")

    print("Loading MediaPipe Pose Landmarker...")

    base_options = python.BaseOptions(
        model_asset_path=str(MODEL_PATH)
    )

    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=MIN_CONFIDENCE,
        min_pose_presence_confidence=MIN_CONFIDENCE,
        min_tracking_confidence=MIN_CONFIDENCE
    )

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        raise RuntimeError(
            "Could not open webcam. Check CAMERA_INDEX."
        )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("Starting webcam...")
    print("Press Q to quit.")

    last_timestamp_ms = 0

    try:

        with vision.PoseLandmarker.create_from_options(
            options
        ) as landmarker:

            while True:

                success, frame = camera.read()

                if not success:
                    print("Could not read webcam frame.")
                    break

                timestamp_ms = time.monotonic_ns() // 1_000_000

                timestamp_ms = max(
                    timestamp_ms,
                    last_timestamp_ms + 1
                )

                last_timestamp_ms = timestamp_ms

                processed_frame = process_frame(
                    frame,
                    landmarker,
                    timestamp_ms
                )

                cv2.imshow(
                    "FORGE AI CAM - Push-up Tracking",
                    processed_frame
                )

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break

    finally:

        camera.release()
        cv2.destroyAllWindows()

        print("Webcam closed.")
        print(
            "Final push-up count:",
            rep_counter.rep_count
        )


if __name__ == "__main__":
    main()
