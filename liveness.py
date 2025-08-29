# liveness.py
# Motion-based liveness: measures average frame-to-frame change.
# Returns (ok: bool, score: float). Lower threshold = easier to pass.

import cv2
import time
import numpy as np

# ---- Tunables (safe defaults) ----
MOTION_SCORE_THRESHOLD = 1.0  # <= lower this if it's still too strict
DURATION_SECONDS = 3.0  # capture window; increase for more robust score
BLUR_SIZE = (5, 5)  # denoise before differencing
DIFF_CLIP = 5.0  # clip extreme per-frame diffs (helps stability)


def _frame_motion_score(prev_gray, gray):
    """Compute a simple per-frame motion score (mean abs-diff with light blur)."""
    diff = cv2.absdiff(prev_gray, gray)
    diff = cv2.GaussianBlur(diff, BLUR_SIZE, 0)
    # Normalize to 0..255 mean; this yields small values (0~a few units) for subtle motion
    score = float(diff.mean())
    # clip outliers so a single sudden change doesn't dominate the average
    return min(score, DIFF_CLIP)


def check_motion_liveness(
    camera_index: int = 0,
    duration: float = DURATION_SECONDS,
    threshold: float = MOTION_SCORE_THRESHOLD,
):
    """
    Ask the user to blink/turn head slightly for `duration` seconds.
    Returns (ok, avg_motion_score).
    """
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera")

    try:
        ok, frame = cap.read()
        if not ok or frame is None:
            raise RuntimeError("Could not read from camera")

        prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        total = 0.0
        samples = 0
        end_t = time.time() + duration

        while time.time() < end_t:
            ok, frame = cap.read()
            if not ok or frame is None:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Per-frame score
            score = _frame_motion_score(prev_gray, gray)
            total += score
            samples += 1

            prev_gray = gray

            # small pause to keep CPU reasonable
            cv2.waitKey(15)

        avg = (total / samples) if samples else 0.0
        print(f"[LIVENESS] avg motion={avg:.2f} (threshold={threshold})")
        return (avg >= threshold), float(avg)

    finally:
        try:
            cap.release()
        except Exception:
            pass
