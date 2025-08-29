import os, sys, sqlite3, cv2, numpy as np
from tkinter import messagebox, Tk

_root = Tk()
_root.withdraw()


def info(msg):
    messagebox.showinfo("Face Enrollment", msg)


def error(msg):
    messagebox.showerror("Face Enrollment", msg)


if not os.path.exists("session.txt"):
    error("No session found. Please register or login first.")
    sys.exit(1)
email = open("session.txt", "r").read().strip()
if not email:
    error("Empty session email.")
    sys.exit(1)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

conn = sqlite3.connect("face.db")
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS identities(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE
)"""
)
conn.commit()

c.execute("SELECT id FROM identities WHERE email=?", (email,))
row = c.fetchone()
if row:
    label_id = row[0]
else:
    c.execute("INSERT INTO identities(email) VALUES (?)", (email,))
    conn.commit()
    label_id = c.lastrowid

person_dir = os.path.join(DATA_DIR, email)
os.makedirs(person_dir, exist_ok=True)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    error("Cannot access webcam.")
    sys.exit(2)

cascade_file = os.path.join(
    cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
)
if not os.path.exists(cascade_file):
    error("Haar cascade not found.")
    sys.exit(3)
face_cascade = cv2.CascadeClassifier(cascade_file)

info(
    f"Starting face enrollment for {email}.\nLook at the camera. We'll capture around 60 samples."
)
count, TARGET = 0, 60

while True:
    ok, frame = cap.read()
    if not ok:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces):
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        roi = gray[y : y + h, x : x + w]
        roi = cv2.resize(roi, (200, 200))
        count += 1
        cv2.imwrite(os.path.join(person_dir, f"{count:03d}.png"), roi)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.putText(
        frame,
        f"Samples: {count}/{TARGET}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
    )
    cv2.imshow("Enrollment - Press Q to cancel", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        error("Enrollment cancelled.")
        break
    if count >= TARGET:
        break

cap.release()
cv2.destroyAllWindows()
if count < 15:
    error("Not enough samples captured.")
    sys.exit(4)

try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
except AttributeError:
    error("LBPH not available. Install: pip install opencv-contrib-python")
    sys.exit(5)

images, labels = [], []
for person in os.listdir(DATA_DIR):
    p_dir = os.path.join(DATA_DIR, person)
    if not os.path.isdir(p_dir):
        continue
    c.execute("SELECT id FROM identities WHERE email=?", (person,))
    r = c.fetchone()
    if not r:
        c.execute("INSERT OR IGNORE INTO identities(email) VALUES (?)", (person,))
        conn.commit()
        c.execute("SELECT id FROM identities WHERE email=?", (person,))
        r = c.fetchone()
    pid = r[0]
    for fn in os.listdir(p_dir):
        if fn.lower().endswith((".png", ".jpg", ".jpeg")):
            img = cv2.imread(os.path.join(p_dir, fn), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            images.append(img)
            labels.append(pid)

if len(images) < 10:
    error("Too few training images.")
    sys.exit(6)

recognizer.train(images, np.array(labels))
recognizer.save("trainingdata.yml")
conn.close()

info("✅ Face enrollment completed and model retrained.")
sys.exit(0)
