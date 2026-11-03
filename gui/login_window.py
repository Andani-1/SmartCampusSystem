import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from auth import hash_password, verify_password
from booking_rules import list_campuses
from models import Lecturer, CampusAdmin, SystemOperator

def build_user_object(row):
    if row["role"] == "Lecturer":
        return Lecturer(row["username"], row["campus"])
    if row["role"] == "Admin":
        return CampusAdmin(row["username"], row["campus"])
    return SystemOperator(row["username"])

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_success = on_login_success
        self.root.title("Smart Campus Booking")
        self.root.geometry("380x360")

        tk.Label(root, text="Smart Campus Booking",
                 font=("Times New Roman", 16, "bold")).pack(pady=10)

        tk.Label(root, text="Username").pack()
        self.user_entry = tk.Entry(root, width=28)
        self.user_entry.pack(pady=2)

        tk.Label(root, text="Password").pack()
        self.pw_entry = tk.Entry(root, width=28, show="*")
        self.pw_entry.pack(pady=2)

        tk.Button(root, text="Log In", width=20,
                  command=self.login).pack(pady=10)

        tk.Label(root, text="— OR register as Lecturer —").pack()
        tk.Label(root, text="Campus").pack()
        self.campus_var = tk.StringVar(value=list_campuses()[0])
        ttk.Combobox(root, textvariable=self.campus_var,
                     values=list_campuses(), state="readonly",
                     width=25).pack(pady=2)

        tk.Button(root, text="Register (Lecturer)", width=20,
                  command=self.register).pack(pady=8)

    def login(self):
        u = self.user_entry.get().strip()
        p = self.pw_entry.get().strip()
        if not u or not p:
            messagebox.showerror("Error", "Enter username and password.")
            return
        row = db.get_user(u)
        if not row or not verify_password(p, row["password"]):
            messagebox.showerror("Error", "Invalid credentials.")
            return
        user = build_user_object(row)
        self.root.destroy()
        self.on_success(user)

    def register(self):
        u = self.user_entry.get().strip()
        p = self.pw_entry.get().strip()
        campus = self.campus_var.get()
        if not u or len(p) < 4:
            messagebox.showerror("Error",
                "Username required and password must be ≥4 characters.")
            return
        ok = db.add_user(u, hash_password(p), "Lecturer", campus)
        if ok:
            messagebox.showinfo("Success", "Account created — now log in.")
        else:
            messagebox.showerror("Error", "Username already exists.")