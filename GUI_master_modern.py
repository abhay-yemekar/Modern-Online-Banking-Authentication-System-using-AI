import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import hashlib
import subprocess, sys


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def run_script(script):
    subprocess.run([sys.executable, script], check=True)


conn = sqlite3.connect("users.db")
c = conn.cursor()


def login_user():
    email = email_var.get().strip()
    password = pwd_var.get().strip()
    if not email or not password:
        messagebox.showwarning("Input Error", "Email and Password required!")
        return

    c.execute(
        "SELECT first_name, last_name FROM users WHERE email=? AND password=?",
        (email, hash_password(password)),
    )
    row = c.fetchone()
    if row:
        with open("session.txt", "w") as f:
            f.write(email)
        full_name = f"{row[0]} {row[1]}".strip()
        messagebox.showinfo(
            "Login", f"✅ Welcome back, {full_name}!\nProceeding to MFA."
        )
        root.destroy()
        run_script("app.py")
    else:
        messagebox.showerror("Error", "❌ Invalid credentials.")


def go_back():
    root.destroy()
    run_script("main.py")


root = tk.Tk()
root.title("Modern Online Banking — Login")
try:
    root.state("zoomed")
except Exception:
    root.attributes("-fullscreen", True)
root.configure(bg="#f5f5f5")

style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass
style.configure("Title.TLabel", font=("Arial", 28, "bold"))
style.configure("Field.TLabel", font=("Arial", 14))
style.configure("Field.TEntry", font=("Arial", 14))
style.configure(
    "Primary.TButton",
    font=("Arial", 14, "bold"),
    padding=10,
    background="#2196F3",
    foreground="white",
)
style.configure(
    "Secondary.TButton",
    font=("Arial", 14, "bold"),
    padding=10,
    background="#9E9E9E",
    foreground="white",
)

container = ttk.Frame(root, padding=40)
container.pack(expand=True)
ttk.Label(container, text="User Login", style="Title.TLabel").pack(pady=40)

form = ttk.Frame(container)
form.pack(pady=10)

email_var = tk.StringVar(master=root)
pwd_var = tk.StringVar(master=root)

ttk.Label(form, text="Email:", style="Field.TLabel").grid(
    row=0, column=0, padx=(0, 20), pady=8, sticky="e"
)
email_entry = ttk.Entry(form, textvariable=email_var, style="Field.TEntry", width=40)
email_entry.grid(row=0, column=1, pady=8, sticky="w")

ttk.Label(form, text="Password:", style="Field.TLabel").grid(
    row=1, column=0, padx=(0, 20), pady=8, sticky="e"
)
pwd_entry = ttk.Entry(
    form, textvariable=pwd_var, style="Field.TEntry", show="*", width=40
)
pwd_entry.grid(row=1, column=1, pady=8, sticky="w")

show_pwd = tk.BooleanVar(master=root, value=False)


def toggle_pwd():
    pwd_entry.config(show="" if show_pwd.get() else "*")


ttk.Checkbutton(
    container, text="Show Password", variable=show_pwd, command=toggle_pwd
).pack(pady=5)

btns = ttk.Frame(container)
btns.pack(pady=20)
ttk.Button(btns, text="Login", style="Primary.TButton", command=login_user).grid(
    row=0, column=0, padx=10
)
ttk.Button(
    btns, text="⬅ Back to Menu", style="Secondary.TButton", command=go_back
).grid(row=0, column=1, padx=10)

root.mainloop()
