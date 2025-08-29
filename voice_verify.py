import os, sys, sqlite3, difflib
import tkinter as tk
from tkinter import messagebox, simpledialog

root = tk.Tk()
root.withdraw()

if not os.path.exists("session.txt"):
    messagebox.showerror("Voice", "No session. Please login first.")
    sys.exit(1)
email = open("session.txt").read().strip()

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("SELECT passphrase FROM users WHERE email=?", (email,))
row = c.fetchone()
if not row:
    messagebox.showerror("Voice", "User not found.")
    sys.exit(1)
expected = row[0].strip().lower()

recognized = None
try:
    import speech_recognition as sr

    r = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo(
            "Voice Biometrics",
            f"Please speak your passphrase now:\n\n“{expected}”\n\nRecording for ~4 seconds…",
        )
        r.adjust_for_ambient_noise(source, duration=0.8)
        audio = r.listen(source, timeout=5, phrase_time_limit=4)
    try:
        recognized = r.recognize_google(audio).strip().lower()
    except Exception:
        recognized = None
except Exception:
    recognized = None

if recognized is None:
    typed = simpledialog.askstring(
        "Voice Biometrics",
        f"Microphone/STT unavailable.\nType your passphrase:\n\n{expected}\n",
    )
    if not typed:
        messagebox.showerror("Voice", "No input provided.")
        sys.exit(2)
    recognized = typed.strip().lower()

ratio = difflib.SequenceMatcher(None, expected, recognized).ratio()
if ratio >= 0.85 or expected == recognized:
    sys.exit(0)
else:
    messagebox.showerror("Voice", f"Phrase mismatch.\nHeard: “{recognized}”")
    sys.exit(3)
