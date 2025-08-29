import tkinter as tk
import subprocess, sys


def run_script(script):
    subprocess.run([sys.executable, script], check=True)


def start_registration():
    root.destroy()
    run_script("registration_modern.py")


def start_login():
    root.destroy()
    run_script("GUI_master_modern.py")


root = tk.Tk()
root.title("Modern Online Banking — Main Menu")

try:
    root.state("zoomed")
except Exception:
    root.attributes("-fullscreen", True)

root.configure(bg="#f5f5f5")

tk.Label(
    root,
    text="Welcome to Modern Online Banking System",
    font=("Arial", 28, "bold"),
    bg="#f5f5f5",
    fg="#333",
).pack(pady=80)

tk.Button(
    root,
    text="🆕 Register",
    width=25,
    height=2,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 16, "bold"),
    command=start_registration,
).pack(pady=40)

tk.Button(
    root,
    text="🔑 Login",
    width=25,
    height=2,
    bg="#2196F3",
    fg="white",
    font=("Arial", 16, "bold"),
    command=start_login,
).pack(pady=20)

tk.Button(
    root,
    text="❌ Exit",
    width=15,
    height=2,
    bg="#E91E63",
    fg="white",
    font=("Arial", 14, "bold"),
    command=root.quit,
).pack(side="bottom", pady=40)

root.mainloop()
