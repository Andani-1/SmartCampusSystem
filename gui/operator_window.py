import tkinter as tk
from tkinter import ttk
import database as db
from booking_rules import list_campuses
import reports

class OperatorWindow:
    def __init__(self, root, operator):
        self.root = root
        self.user = operator
        self.root.title(operator.dashboard_title())
        self.root.geometry("950x650")

        tk.Label(root, text="All Bookings Across All Campuses",
                 font=("Times New Roman", 12, "bold")).pack(anchor="w", padx=10, pady=6)

        self.tree = ttk.Treeview(root,
            columns=("campus","code","user","date","start","dur","status"),
            show="headings", height=12)
        for c, h in [("campus","Campus"),("code","Resource"),("user","User"),
                     ("date","Date"),("start","Start"),("dur","Min"),("status","Status")]:
            self.tree.heading(c, text=h); self.tree.column(c, width=120)
        self.tree.pack(fill="x", padx=10)

        tk.Button(root, text="Refresh", command=self.refresh).pack(pady=4)

        tk.Label(root, text="Cross-Campus Comparison Report",
                 font=("Times New Roman", 12, "bold")).pack(anchor="w", padx=10, pady=6)

        self.report = tk.Text(root, height=10, font=("Courier New", 10))
        self.report.pack(fill="both", expand=True, padx=10, pady=6)

        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for b in self.user.view_all_bookings():
            self.tree.insert("", "end",
                values=(b["campus"], b["resource_code"], b["username"],
                        b["booking_date"], b["start_time"],
                        b["duration_minutes"], b["status"]))

        rows = reports.cross_campus_report(list_campuses())
        self.report.delete("1.0", "end")
        self.report.insert("end",
            f"{'Campus':<15}{'Bookings':<12}{'Most Used':<15}{'Avg (min)':<12}\n")
        self.report.insert("end", "-" * 60 + "\n")
        for r in rows:
            self.report.insert("end",
                f"{r['campus']:<15}{r['total_bookings']:<12}"
                f"{r['most_used']:<15}{r['avg_duration']:<12}\n")