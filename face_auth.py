# face_auth.py
import time
from pathlib import Path
from typing import Optional, Tuple
import cv2

CASCADE_PATH = Path(__file__).with_name("haarcascade_frontalface_default.xml")
LBPH_MODEL_PATH = Path(__file__).with_name("trainingdata.yml")

# Lower is better; 50~70 typical for LBPH when trained well. Tune for your dataset.
LBPH_THRESHOLD = 60.0


def verify_face(
    expected_id: int, timeout_sec: int = 20
) -> Tuple[bool, Optional[float], Optional[int]]:
    """
    Open webcam, detect face, run LBPH prediction.
    Returns (ok, confidence, label). ok=True if label==expected_id and confidence<=threshold.
    """
    if not LBPH_MODEL_PATH.exists():
        raise FileNotFoundError(f"LBPH model not found: {LBPH_MODEL_PATH}")
    if not CASCADE_PATH.exists():
        raise FileNotFoundError(f"Haar cascade not found: {CASCADE_PATH}")

    face_cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(LBPH_MODEL_PATH))

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam (index 0).")

    start = time.time()
    decided = (False, None, None)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for x, y, w, h in faces:
                roi = gray[y : y + h, x : x + w]
                label, confidence = recognizer.predict(roi)
                # Draw UI
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                txt = f"label={label} conf={confidence:.1f} thr={LBPH_THRESHOLD:.1f}"
                cv2.putText(
                    frame,
                    txt,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

                if label == expected_id and confidence <= LBPH_THRESHOLD:
                    decided = (True, confidence, label)
                    cv2.putText(
                        frame,
                        "FACE VERIFIED ✅",
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2,
                    )
                    cv2.imshow("Face Verification", frame)
                    cv2.waitKey(800)
                    return decided

            cv2.putText(
                frame,
                "Look straight; ensure good lighting.",
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )
            cv2.imshow("Face Verification", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break
            if time.time() - start > timeout_sec:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return decided
