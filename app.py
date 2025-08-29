# app.py — NON-BLOCKING MFA (async subprocess)

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, sys, threading
import sqlite3, os

# ---------- session & DB ----------
session_email = None
if os.path.exists("session.txt"):
    with open("session.txt", "r") as f:
        session_email = f.read().strip() or None

conn = sqlite3.connect("users.db")
c = conn.cursor()
user_data = None
if session_email:
    c.execute(
        "SELECT first_name, last_name, mobile, passphrase FROM users WHERE email=?",
        (session_email,),
    )
    user_data = c.fetchone()
full_name = f"{user_data[0]} {user_data[1]}".strip() if user_data else "User"

# ---------- UI ----------
root = tk.Tk()
root.title("Modern Online Banking — MFA")
try:
    root.state("zoomed")
except Exception:
    root.attributes("-fullscreen", True)
root.configure(bg="#f0ece3")

style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass
style.configure("Title.TLabel", font=("Arial", 26, "bold"))

container = ttk.Frame(root, padding=40)
container.pack(expand=True, fill="both")
ttk.Label(
    container, text=f"Multi-Factor Authentication for {full_name}", style="Title.TLabel"
).pack(pady=20)

center = ttk.Frame(container)
center.pack(pady=10)

status_var = tk.StringVar(value="")
status_lbl = ttk.Label(container, textvariable=status_var)
status_lbl.pack(pady=(10, 0))

# Buttons (we keep references so we can enable/disable)
btn_face = ttk.Button(center, text="😀  Face Recognition", width=25)
btn_otp = ttk.Button(center, text="📧  OTP Verification (Email)", width=25)
btn_voice = ttk.Button(center, text="🎤  Voice Biometrics", width=25)
btn_face.pack(pady=12)
btn_otp.pack(pady=12)
btn_voice.pack(pady=12)

bottom = ttk.Frame(container)
bottom.pack(fill="x", pady=30)
btn_back = ttk.Button(bottom, text="⬅  Back to Login")
btn_exit = ttk.Button(bottom, text="❌  Exit", command=root.quit)
btn_back.pack(side="left", padx=40)
btn_exit.pack(side="right", padx=40)


def back_to_login():
    root.destroy()
    subprocess.Popen([sys.executable, "GUI_master_modern.py"])


btn_back.config(command=back_to_login)


# ---------- helpers ----------
def set_busy(is_busy: bool, msg: str = ""):
    """Disable/enable UI and show a tiny status line."""
    widgets = [btn_face, btn_otp, btn_voice, btn_back, btn_exit]
    for w in widgets:
        try:
            w.state(["disabled"] if is_busy else ["!disabled"])
        except Exception:
            w.config(state=("disabled" if is_busy else "normal"))
    status_var.set(msg)


def run_script_async(script, on_done):
    """Run a Python script in a background thread; call on_done(returncode) on UI thread."""

    def worker():
        rc = 0
        try:
            subprocess.run([sys.executable, script], check=True)
        except subprocess.CalledProcessError as e:
            rc = e.returncode
        except Exception:
            rc = 999
        root.after(0, lambda: on_done(rc))

    threading.Thread(target=worker, daemon=True).start()


# ---------- actions ----------
def do_face():
    if not os.path.exists("trainingdata.yml"):
        messagebox.showwarning(
            "Face Recognition",
            "No trained model found. Please register & enroll face first.",
        )
        return
    if not os.path.exists("face.db"):
        messagebox.showwarning(
            "Face Recognition", "Identity map missing (face.db). Please enroll again."
        )
        return
    set_busy(True, "Verifying face…")
    run_script_async(
        "face_verify.py",
        on_done=lambda rc: (
            set_busy(False, ""),
            (
                messagebox.showinfo("Face Recognition", "✅ Face verified")
                if rc == 0
                else messagebox.showerror(
                    "Face Recognition", "❌ Face verification failed. Try again."
                )
            ),
        ),
    )


def do_otp():
    if not user_data:
        messagebox.showerror("OTP", "No logged-in user found.")
        return
    set_busy(True, "Sending OTP to your email…")
    run_script_async(
        "otp_modern.py",
        on_done=lambda rc: (
            set_busy(False, ""),
            (
                messagebox.showinfo("OTP", "✅ OTP verified")
                if rc == 0
                else (
                    None
                    if rc in (2, 3)
                    else messagebox.showerror("OTP", "❌ OTP flow failed")
                )
            ),
        ),
    )


def do_voice():
    if not user_data:
        messagebox.showerror("Voice Biometrics", "No logged-in user found.")
        return
    set_busy(True, "Listening / verifying passphrase…")

    def done(rc):
        set_busy(False, "")
        if rc == 0:
            messagebox.showinfo(
                "Voice Biometrics", "✅ Voice verified. Access Granted 🎉"
            )
            try:
                os.remove("session.txt")
            except Exception:
                pass
        else:
            messagebox.showerror("Voice Biometrics", "❌ Voice verification failed.")

    run_script_async("voice_verify.py", on_done=done)


btn_face.config(command=do_face)
btn_otp.config(command=do_otp)
btn_voice.config(command=do_voice)

root.mainloop()
