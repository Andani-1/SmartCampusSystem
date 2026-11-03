import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from booking_rules import get_policy

class AdminWindow:
    def __init__(self, root, admin):
        self.root = root
        self.user = admin
        self.root.title(admin.dashboard_title())
        self.root.geometry("900x600")

        tk.Label(root, text=f"Active Campus: {admin.campus}",
                 font=("Times New Roman", 12, "bold")).pack(anchor="w", padx=10, pady=6)

        frm = tk.LabelFrame(root, text="Resource Management")
        frm.pack(fill="x", padx=10, pady=6)

        tk.Label(frm, text="Code").grid(row=0, column=0)
        self.code = tk.Entry(frm, width=12); self.code.grid(row=0, column=1)
        tk.Label(frm, text="Name").grid(row=0, column=2)
        self.name = tk.Entry(frm, width=22); self.name.grid(row=0, column=3)
        tk.Label(frm, text="Category").grid(row=0, column=4)
        self.cat = tk.Entry(frm, width=15); self.cat.grid(row=0, column=5)

        tk.Button(frm, text="Add", command=self.add_resource).grid(row=0, column=6, padx=4)
        tk.Button(frm, text="Update", command=self.update_resource).grid(row=0, column=7, padx=4)
        tk.Button(frm, text="Delete", command=self.delete_resource).grid(row=0, column=8, padx=4)

        self.res_tree = ttk.Treeview(root, columns=("code", "name", "cat"),
                                      show="headings", height=8)
        for c, h in [("code", "Code"), ("name", "Name"), ("cat", "Category")]:
            self.res_tree.heading(c, text=h); self.res_tree.column(c, width=250)
        self.res_tree.pack(fill="x", padx=10)
        self.res_tree.bind("<<TreeviewSelect>>", self._fill_form)

        tk.Label(root, text="All Bookings at This Campus",
                 font=("Times New Roman", 12, "bold")).pack(anchor="w", padx=10, pady=6)
        self.book_tree = ttk.Treeview(root,
            columns=("id", "code", "user", "date", "start", "dur", "status"),
            show="headings", height=10)
        for c, h in [("id","ID"),("code","Resource"),("user","User"),
                     ("date","Date"),("start","Start"),("dur","Min"),("status","Status")]:
            self.book_tree.heading(c, text=h); self.book_tree.column(c, width=120)
        self.book_tree.pack(fill="x", padx=10)

        self.refresh()

    def refresh(self):
        self.res_tree.delete(*self.res_tree.get_children())
        for r in db.get_resources(self.user.campus):
            self.res_tree.insert("", "end",
                values=(r["resource_code"], r["name"], r["category"]))

        self.book_tree.delete(*self.book_tree.get_children())
        for b in self.user.view_campus_bookings():
            self.book_tree.insert("", "end",
                values=(b["id"], b["resource_code"], b["username"],
                        b["booking_date"], b["start_time"],
                        b["duration_minutes"], b["status"]))

    def _fill_form(self, _):
        sel = self.res_tree.selection()
        if not sel: return
        v = self.res_tree.item(sel[0])["values"]
        self.code.delete(0, "end"); self.code.insert(0, v[0])
        self.name.delete(0, "end"); self.name.insert(0, v[1])
        self.cat.delete(0, "end"); self.cat.insert(0, v[2])

    def add_resource(self):
        code, name, cat = self.code.get().strip(), self.name.get().strip(), self.cat.get().strip()
        if not (code and name):
            messagebox.showerror("Error", "Code and name required."); return
        ok, msg = db.add_resource(code, name, self.user.campus, cat)
        (messagebox.showinfo if ok else messagebox.showerror)("Info", msg)
        self.refresh()

    def update_resource(self):
        code, name, cat = self.code.get().strip(), self.name.get().strip(), self.cat.get().strip()
        if not (code and name):
            messagebox.showerror("Error", "Select a resource or fill fields."); return
        db.update_resource(code, name, cat)
        self.refresh()

    def delete_resource(self):
        code = self.code.get().strip()
        if not code:
            messagebox.showerror("Error", "Select a resource."); return
        db.delete_resource(code)
        self.refresh()