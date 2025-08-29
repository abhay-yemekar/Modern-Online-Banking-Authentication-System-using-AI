import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import hashlib
import subprocess, sys


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    mobile TEXT NOT NULL,
    passphrase TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT
)"""
)
conn.commit()


def register_user():
    first_name = fname_var.get().strip()
    last_name = lname_var.get().strip()
    email = email_var.get().strip()
    password = pwd_var.get().strip()
    mobile = mobile_var.get().strip()
    passphrase = pass_var.get().strip()

    if not all([first_name, last_name, email, password, mobile, passphrase]):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        c.execute(
            """INSERT INTO users (email, password, mobile, passphrase, first_name, last_name)
                     VALUES (?, ?, ?, ?, ?, ?)""",
            (email, hash_password(password), mobile, passphrase, first_name, last_name),
        )
        conn.commit()

        messagebox.showinfo(
            "Success",
            f"✅ {first_name} {last_name} registered!\nProceed with face capture.",
        )

        with open("session.txt", "w") as f:
            f.write(email)

        root.destroy()
        subprocess.run([sys.executable, "face_capture_enroll.py"], check=True)
        subprocess.run([sys.executable, "GUI_master_modern.py"], check=True)
        sys.exit(0)

    except sqlite3.IntegrityError:
        go_login = messagebox.askyesno(
            "Already Registered",
            "⚠ This email is already registered.\nDo you want to go to Login instead?",
        )
        if go_login:
            root.destroy()
            subprocess.run([sys.executable, "GUI_master_modern.py"], check=True)
            sys.exit(0)


def go_back():
    root.destroy()
    subprocess.run([sys.executable, "main.py"], check=True)


# --- UI ---
root = tk.Tk()
root.title("Modern Online Banking — Registration")
try:
    root.state("zoomed")
except Exception:
    root.attributes("-fullscreen", True)

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
    background="#4CAF50",
    foreground="white",
)
style.map("Primary.TButton", background=[("active", "#43A047")])
style.configure(
    "Secondary.TButton",
    font=("Arial", 14, "bold"),
    padding=10,
    background="#9E9E9E",
    foreground="white",
)

root.configure(bg="#f5f5f5")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

container = ttk.Frame(root, padding=40)
container.grid(row=0, column=0, sticky="nsew")
container.grid_columnconfigure(0, weight=1)

ttk.Label(container, text="New User Registration", style="Title.TLabel").grid(
    row=0, column=0, pady=(10, 30)
)

form = ttk.Frame(container)
form.grid(row=1, column=0)
form.grid_columnconfigure(0, weight=0)
form.grid_columnconfigure(1, weight=1)

fname_var = tk.StringVar(master=root)
lname_var = tk.StringVar(master=root)
email_var = tk.StringVar(master=root)
pwd_var = tk.StringVar(master=root)
mobile_var = tk.StringVar(master=root)
pass_var = tk.StringVar(master=root)


def add_row(r, label, var, show=None):
    ttk.Label(form, text=label, style="Field.TLabel").grid(
        row=r, column=0, padx=(0, 20), pady=8, sticky="e"
    )
    e = ttk.Entry(form, textvariable=var, style="Field.TEntry", show=show, width=40)
    e.grid(row=r, column=1, pady=8, sticky="w")
    return e


row = 0
add_row(row, "First Name:", fname_var)
row += 1
add_row(row, "Last Name:", lname_var)
row += 1
add_row(row, "Email:", email_var)
row += 1
pwd_entry = add_row(row, "Password:", pwd_var, show="*")
row += 1
add_row(row, "Mobile Number:", mobile_var)
row += 1
pass_entry = add_row(row, "Voice Passphrase:", pass_var, show="*")
row += 1

toggles = ttk.Frame(container)
toggles.grid(row=2, column=0, pady=(10, 5))
show_pwd = tk.BooleanVar(master=root, value=False)
show_pass = tk.BooleanVar(master=root, value=False)


def toggle_pwd():
    pwd_entry.config(show="" if show_pwd.get() else "*")


def toggle_pass():
    pass_entry.config(show="" if show_pass.get() else "*")


ttk.Checkbutton(
    toggles, text="Show Password", variable=show_pwd, command=toggle_pwd
).grid(row=0, column=0, padx=10)
ttk.Checkbutton(
    toggles, text="Show Passphrase", variable=show_pass, command=toggle_pass
).grid(row=0, column=1, padx=10)

buttons = ttk.Frame(container)
buttons.grid(row=3, column=0, pady=(25, 10))
ttk.Button(
    buttons, text="Register", style="Primary.TButton", command=register_user
).grid(row=0, column=0, padx=12)
ttk.Button(
    buttons, text="⬅ Back to Menu", style="Secondary.TButton", command=go_back
).grid(row=0, column=1, padx=12)
ttk.Frame(container).grid(row=4, column=0, pady=20)

root.mainloop()
