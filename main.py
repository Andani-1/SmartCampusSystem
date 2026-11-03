import tkinter as tk
import database as db
from gui.login_window import LoginWindow
from gui.lecturer_window import LecturerWindow
from gui.admin_window import AdminWindow
from gui.operator_window import OperatorWindow

def launch_dashboard(user):
    root = tk.Tk()
    if user.role == "Lecturer":
        LecturerWindow(root, user)
    elif user.role == "Admin":
        AdminWindow(root, user)
    else:
        OperatorWindow(root, user)
    root.mainloop()

def main():
    db.initialise_database()

    root = tk.Tk()
    LoginWindow(root, on_login_success=launch_dashboard)
    root.mainloop()

if __name__ == "__main__":
    main()
