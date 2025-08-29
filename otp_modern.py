import os, sys, json, random, time, sqlite3, smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox, simpledialog

root = tk.Tk()
root.withdraw()

# session + email
if not os.path.exists("session.txt"):
    messagebox.showerror("OTP", "No session. Please login first.")
    sys.exit(1)
email = open("session.txt").read().strip()

# verify user exists
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("SELECT email FROM users WHERE email=?", (email,))
if not c.fetchone():
    messagebox.showerror("OTP", "User not found.")
    sys.exit(1)

# generate OTP
otp = random.randint(100000, 999999)
payload = {"email": email, "otp": otp, "ts": time.time()}
with open("otp_cache.json", "w") as f:
    json.dump(payload, f)

# ---- SEND VIA GMAIL SMTP ----
SENDER_EMAIL = "abhay.s.yemekar@gmail.com"  # <<< set yours
SENDER_PASS = "pygnoinvoarbbqtq"  # <<< Gmail App Password

sent_ok = False
try:
    msg = MIMEText(f"Your OTP code is: {otp}\nIt is valid for 5 minutes.")
    msg["Subject"] = "Your OTP Code"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.sendmail(SENDER_EMAIL, [email], msg.as_string())
    sent_ok = True
    messagebox.showinfo("OTP", f"OTP sent to {email}")
except Exception as e:
    # For local testing, still allow flow by showing OTP
    messagebox.showwarning(
        "OTP",
        f"Could not send email (demo fallback shows OTP):\n\nOTP: {otp}\n\nError: {e}",
    )

# prompt user
entered = simpledialog.askstring(
    "OTP Verification", "Please enter the 6-digit OTP sent to your email:"
)
if not entered:
    messagebox.showerror("OTP", "No OTP entered.")
    sys.exit(2)
if entered.strip() != str(otp):
    messagebox.showerror("OTP", "Incorrect OTP.")
    sys.exit(3)

sys.exit(0)
