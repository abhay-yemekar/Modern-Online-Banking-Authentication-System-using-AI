# livelines_net.py  — responsive liveness window + safe TF imports
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Tuple, cast
import cv2
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent
CASCADE = PROJECT_DIR / "haarcascade_frontalface_default.xml"
JSON = PROJECT_DIR / "antispoofing_model.json"
H5_A = PROJECT_DIR / "antispoofing_model.h5"
H5_B = PROJECT_DIR / "antispoofing_model.hdf5"

# ---- Optional TensorFlow import (no static errors) ----
try:
    import tensorflow as tf  # type: ignore
except Exception:
    tf = None  # type: ignore

def load_model() -> Tuple[Optional[Any], Optional[Any]]:
    """
    Returns (model, tf) if a model can be loaded, else (None, None).
    No direct keras sub-imports to keep Pylance happy.
    """
    if tf is None:
        print("[liveness] TensorFlow not installed; running camera only.")
        return None, None

    # Access keras via getattr/cast to avoid type-stub issues
    try:
        keras_models = cast(Any, tf.keras.models)  # type: ignore[attr-defined]
    except Exception:
        print("[liveness] tf.keras not available.")
        return None, None

    # JSON + weights
    if JSON.exists() and (H5_A.exists() or H5_B.exists()):
        try:
            model_from_json = getattr(keras_models, "model_from_json", None)
            if callable(model_from_json):
                model = model_from_json(JSON.read_text())
                model.load_weights(str(H5_A if H5_A.exists() else H5_B))
                print("[liveness] Loaded model from JSON + weights.")
                return model, tf
        except Exception as e:
            print("[liveness] JSON+weights load failed:", e)

    # Single .h5
    if H5_A.exists():
        try:
            load_model_fn = getattr(keras_models, "load_model", None)
            if callable(load_model_fn):
                model = load_model_fn(str(H5_A))
                print("[liveness] Loaded model from H5.")
                return model, tf
        except Exception as e:
            print("[liveness] H5 load failed:", e)

    print("[liveness] No model found; running camera only.")
    return None, None

def main() -> None:
    if not CASCADE.exists():
        print(f"[liveness] Missing cascade: {CASCADE}")
        return

    detector = cv2.CascadeClassifier(str(CASCADE))
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW is stable on Windows
    if not cap.isOpened():
        print("[liveness] Could not open webcam.")
        return

    model, tf_mod = load_model()

    # Determine input size for the model if we have one
    input_w: int = 80
    input_h: int = 80
    input_c: int = 3
    if model is not None:
        try:
            ishape = getattr(model, "input_shape", None)
            if isinstance(ishape, (list, tuple)) and len(ishape) and isinstance(ishape[0], (list, tuple)):
                ishape = ishape[0]
            if isinstance(ishape, (list, tuple)) and len(ishape) == 4:
                _, h, w, c = ishape
                input_h = int(h or 80)
                input_w = int(w or 80)
                input_c = int(c or 3)
        except Exception:
            pass

    cv2.namedWindow("Liveness (press Q/Esc to exit)", cv2.WINDOW_NORMAL)

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            label = "NO FACE"
            color = (0, 0, 255)

            if len(faces) > 0:
                x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
                roi_color = frame[y:y+h, x:x+w]

                if model is not None:
                    resized = cv2.resize(roi_color, (int(input_w), int(input_h)))
                    if input_c == 1:
                        resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                        resized = resized[..., None]
                    sample = resized.astype("float32") / 255.0
                    sample = np.expand_dims(sample, axis=0)
                    try:
                        pred = cast(Any, model).predict(sample, verbose=0)
                        score = float(np.ravel(pred)[0])
                        is_live = score >= 0.5  # adjust if your model is inverted
                        label = f"{'LIVE' if is_live else 'SPOOF'} {score:.2f}"
                        color = (0, 200, 0) if is_live else (0, 0, 255)
                    except Exception as e:
                        label = "MODEL ERR"
                        print("[liveness] inference error:", e)
                else:
                    label = "CAMERA OK (no model)"
                    color = (200, 200, 0)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            cv2.imshow("Liveness (press Q/Esc to exit)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q"), 27):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
