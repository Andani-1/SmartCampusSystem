from datetime import datetime
class BookingPolicy:
    def __init__(self, campus_name, max_duration_minutes,
                 allowed_hours=(8, 17), description=""):
        self.campus_name = campus_name
        self.max_duration = max_duration_minutes
        self.allowed_hours = allowed_hours   # (open, close) 24h
        self.description = description

    def validate_duration(self, minutes: int) -> tuple[bool, str]:
        if minutes <= 0:
            return False, "Duration must be positive."
        if minutes > self.max_duration:
            return False, (f"{self.campus_name} policy: maximum booking "
                           f"is {self.max_duration} minutes.")
        return True, ""

    def validate_time(self, start_hhmm: str) -> tuple[bool, str]:
        try:
            hour, minute = map(int, start_hhmm.split(":"))
        except ValueError:
            return False, "Time must be HH:MM."

        if not (self.allowed_hours[0] <= hour < self.allowed_hours[1]):
            return False, (f"{self.campus_name} allows bookings only between "
                           f"{self.allowed_hours[0]:02d}:00 and "
                           f"{self.allowed_hours[1]:02d}:00.")
        return True, ""

    def validate_date(self, yyyy_mm_dd: str) -> tuple[bool, str]:
        try:
            d = datetime.strptime(yyyy_mm_dd, "%Y-%m-%d").date()
        except ValueError:
            return False, "Date must be YYYY-MM-DD."
        if d < datetime.today().date():
            return False, "Cannot book in the past."
        return True, ""

    def check_overlap(self, new_start, new_duration, existing_bookings):
        new_start_min = self._to_minutes(new_start)
        new_end = new_start_min + new_duration
        for b in existing_bookings:
            old_start = self._to_minutes(b["start_time"])
            old_end = old_start + b["duration_minutes"]
            if new_start_min < old_end and old_start < new_end:
                return False, (f"Overlaps existing booking "
                               f"{b['start_time']}–{self._fmt(old_end)}.")
        return True, ""

    @staticmethod
    def _to_minutes(hhmm):
        h, m = map(int, hhmm.split(":"))
        return h * 60 + m

    @staticmethod
    def _fmt(total_minutes):
        return f"{total_minutes//60:02d}:{total_minutes%60:02d}"

CAMPUS_POLICIES = {
    "Johannesburg": BookingPolicy(
        "Johannesburg", max_duration_minutes=120,
        allowed_hours=(8, 17),
        description="Max 2 hours per booking, 08:00–17:00."
    ),
    "Cape Town": BookingPolicy(
        "Cape Town", max_duration_minutes=240,
        allowed_hours=(7, 20),
        description="Max 4 hours per booking, 07:00–20:00."
    ),
    "Durban": BookingPolicy(
        "Durban", max_duration_minutes=90,
        allowed_hours=(9, 16),
        description="Max 90 minutes per booking, 09:00–16:00."
    ),
}

def get_policy(campus: str) -> BookingPolicy:
    if campus not in CAMPUS_POLICIES:
        raise ValueError(f"No booking policy defined for campus '{campus}'.")
    return CAMPUS_POLICIES[campus]
def list_campuses():
    return list(CAMPUS_POLICIES.keys())