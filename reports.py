import database as db
from collections import Counter

def campus_report(campus: str) -> dict:
    bookings = db.bookings_for_campus(campus)
    active = [b for b in bookings if b["status"] == "Active"]

    total = len(active)
    if total == 0:
        return {"campus": campus, "total_bookings": 0,
                "most_used": "—", "avg_duration": 0}

    counter = Counter(b["resource_code"] for b in active)
    most_used = counter.most_common(1)[0][0] if counter else "—"
    avg = sum(b["duration_minutes"] for b in active) / total

    return {
        "campus": campus,
        "total_bookings": total,
        "most_used": most_used,
        "avg_duration": round(avg, 1),
    }

def cross_campus_report(campuses: list[str]) -> list[dict]:
    return [campus_report(c) for c in campuses]