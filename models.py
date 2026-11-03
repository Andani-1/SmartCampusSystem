from abc import ABC, abstractmethod
import database as db

class User(ABC):
    def __init__(self, username: str, role: str, campus: str = ""):
        self._username = username
        self._role = role
        self._campus = campus

    @property
    def username(self): return self._username

    @property
    def role(self): return self._role

    @property
    def campus(self): return self._campus

    @abstractmethod
    def dashboard_title(self) -> str:
        pass

    def __str__(self):
        return f"{self._role}: {self._username} ({self._campus})"

class Lecturer(User):
    def __init__(self, username, campus):
        super().__init__(username, "Lecturer", campus)

    def dashboard_title(self):
        return f"Lecturer Dashboard — {self.username}"

    def view_my_bookings(self):
        return db.bookings_for_user(self.username)

class CampusAdmin(User):
    def __init__(self, username, campus):
        super().__init__(username, "Admin", campus)

    def dashboard_title(self):
        return f"Campus Administrator — {self.campus}"

    def view_campus_bookings(self):
        return db.bookings_for_campus(self.campus)

class SystemOperator(User):
    def __init__(self, username):
        super().__init__(username, "Operator", "ALL")

    def dashboard_title(self):
        return "System Operator — Institutional View"

    def view_all_bookings(self):
        return db.all_bookings()

class Resource:
    def __init__(self, code, name, campus, category):
        self.code = code
        self.name = name
        self.campus = campus
        self.category = category

    def __repr__(self):
        return f"<Resource {self.code} — {self.name} @ {self.campus}>"

class Booking:
    def __init__(self, resource_code, username, campus,
                 date, start, duration, status="Active", bid=None):
        self.id = bid
        self.resource_code = resource_code
        self.username = username
        self.campus = campus
        self.date = date
        self.start = start
        self.duration = duration
        self.status = status

    def __repr__(self):
        return f"<Booking {self.resource_code} {self.date} {self.start} ({self.duration}min)>"