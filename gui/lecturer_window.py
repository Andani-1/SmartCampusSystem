import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from booking_rules import get_policy, list_campuses
from datetime import datetime

class LecturerWindow:
    def __init__(self, root, lecturer):
        self.root = root
        self.user = lecturer
        self.root.title(lecturer.dashboard_title())
        self.root.geometry("900x600")

        top = tk.Frame(root); top.pack(fill="x", padx=10, pady=6)
        tk.Label(top, text="Active Campus:", font=("Times New Roman", 11, "bold")).pack(side="left")
        self.campus_var = tk.StringVar(value=lecturer.campus or list_campuses()[0])
        cb = ttk.Combobox(top, textvariable=self.campus_var,
                          values=list_campuses(), state="readonly", width=20)
        cb.pack(side="left", padx=6)
        cb.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        self.policy_label = tk.Label(top, text="", fg="blue")
        self.policy_label.pack(side="left", padx=20)

        tk.Label(root, text="Available Resources",
                 font=("Times New Roman", 12, "bold")).pack(anchor="w", padx=10)
        self.res_tree = ttk.Treeview(root, columns=("code", "name", "category"),
                                      show="headings", height=8)
        for c, h in [("code", "Code"), ("name", "Name"), ("category", "Category")]:
            self.res_tree.heading(c, text=h); self.res_tree.column(c, width=200)
        self.res_tree.pack(fill="x", padx=10)

        form = tk.LabelFrame(root, text="Create Booking")
        form.pack(fill="x", padx=10, pady=8)

        tk.Label(form, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=4, pady=4)
        self.date_entry = tk.Entry(form, width=15)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1)

        tk.Label(form, text="Start (HH:MM)").grid(row=0, column=2, padx=4)
        self.start_entry = tk.Entry(form, width=8)
        self.start_entry.insert(0, "09:00")
        self.start_entry.grid(row=0, column=3)

        tk.Label(form, text="Duration (min)").grid(row=0, column=4, padx=4)
        self.dur_entry = tk.Entry(form, width=8)
        self.dur_entry.insert(0, "60")
        self.dur_entry.grid(row=0, column=5)

        tk.Button(form, text="Book Selected Resource",
                  command=self.create_booking).grid(row=0, column=6, padx=10)

        tk.Label(root, text="My Bookings",
                 font=("Times New Roman", 12, "bold")).pack(anchor="w", padx=10)
        self.book_tree = ttk.Treeview(root,
            columns=("id", "code", "date", "start", "dur", "status"),
            show="headings", height=8)
        for c, h in [("id", "ID"), ("code", "Resource"), ("date", "Date"),
                     ("start", "Start"), ("dur", "Min"), ("status", "Status")]:
            self.book_tree.heading(c, text=h); self.book_tree.column(c, width=130)
        self.book_tree.pack(fill="x", padx=10)

        tk.Button(root, text="Cancel Selected Booking",
                  command=self.cancel_booking).pack(pady=6)

        self.refresh()

    def refresh(self):
        campus = self.campus_var.get()
        policy = get_policy(campus)
        self.policy_label.config(
            text=f"Policy in effect — {policy.description}")

        self.res_tree.delete(*self.res_tree.get_children())
        for r in db.get_resources(campus):
            self.res_tree.insert("", "end",
                values=(r["resource_code"], r["name"], r["category"]))

        self.book_tree.delete(*self.book_tree.get_children())
        for b in self.user.view_my_bookings():
            self.book_tree.insert("", "end",
                values=(b["id"], b["resource_code"], b["booking_date"],
                        b["start_time"], b["duration_minutes"], b["status"]))

    def create_booking(self):
        sel = self.res_tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a resource first."); return
        code = self.res_tree.item(sel[0])["values"][0]

        date = self.date_entry.get().strip()
        start = self.start_entry.get().strip()
        try:
            dur = int(self.dur_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number."); return

        campus = self.campus_var.get()
        policy = get_policy(campus)

        for validator, value in [
            (policy.validate_date, date),
            (policy.validate_time, start),
            (policy.validate_duration, dur),
        ]:
            ok, msg = validator(value)
            if not ok:
                messagebox.showerror("Booking rule violation", msg); return

        existing = db.bookings_for_resource_on_date(code, date)
        ok, msg = policy.check_overlap(start, dur, existing)
        if not ok:
            messagebox.showerror("Conflict", msg); return

        db.add_booking(code, self.user.username, campus, date, start, dur)
        messagebox.showinfo("Booked", f"{code} booked on {date} at {start}.")
        self.refresh()

    def cancel_booking(self):
        sel = self.book_tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a booking first."); return
        bid = self.book_tree.item(sel[0])["values"][0]
        values = self.book_tree.item(sel[0])["values"]
        if values[5] == "Cancelled":
            messagebox.showinfo("Info", "Already cancelled."); return
        db.cancel_booking(bid)
        messagebox.showinfo("Cancelled", "Booking cancelled.")
        self.refresh()