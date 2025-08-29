import os, sys, sqlite3, cv2, numpy as np
from tkinter import messagebox, Tk

_root = Tk()
_root.withdraw()


def info(msg):
    messagebox.showinfo("Face Verification", msg)


def error(msg):
    messagebox.showerror("Face Verification", msg)


if not os.path.exists("session.txt"):
    error("No session. Please login first.")
    sys.exit(1)
if not os.path.exists("trainingdata.yml"):
    error("No trained model. Enroll first.")
    sys.exit(1)
if not os.path.exists("face.db"):
    error("face.db missing. Enroll first.")
    sys.exit(1)

email = open("session.txt", "r").read().strip()

conn = sqlite3.connect("face.db")
c = conn.cursor()
c.execute("SELECT id FROM identities WHERE email=?", (email,))
row = c.fetchone()
if not row:
    error("Your face not enrolled.")
    sys.exit(1)
label_expected = row[0]

try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
except AttributeError:
    error("LBPH not available. Install: pip install opencv-contrib-python")
    sys.exit(1)
recognizer.read("trainingdata.yml")

cascade_file = os.path.join(
    cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
)
if not os.path.exists(cascade_file):
    error("Haar cascade not found.")
    sys.exit(1)
face_cascade = cv2.CascadeClassifier(cascade_file)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    error("Cannot access webcam.")
    sys.exit(1)

info("Look at the camera. We will verify your face now.\nPress Q to cancel.")
votes_match = 0
votes_total = 0
MAX_FRAMES = 50
CONF_THRESHOLD = 70.0

while votes_total < MAX_FRAMES:
    ok, frame = cap.read()
    if not ok:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces):
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        roi = gray[y : y + h, x : x + w]
        roi = cv2.resize(roi, (200, 200))
        label, conf = recognizer.predict(roi)
        votes_total += 1
        if label == label_expected and conf <= CONF_THRESHOLD:
            votes_match += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"id={label} conf={conf:.1f}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    cv2.putText(
        frame,
        f"Match votes: {votes_match}/{votes_total}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
    )
    cv2.imshow("Face Verify - Press Q to cancel", frame)
    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

if votes_total == 0 or votes_match < max(5, int(0.6 * votes_total)):
    error("Face not verified. Try again with better lighting.")
    sys.exit(2)
sys.exit(0)
