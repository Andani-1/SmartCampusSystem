import sqlite3
from datetime import datetime
DB_NAME = "smart_campus.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialise_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,               -- hashed
            role TEXT NOT NULL,                   -- Lecturer / Admin / Operator
            campus TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            campus TEXT NOT NULL,
            category TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_code TEXT NOT NULL,
            username TEXT NOT NULL,
            campus TEXT NOT NULL,
            booking_date TEXT NOT NULL,           -- YYYY-MM-DD
            start_time TEXT NOT NULL,             -- HH:MM
            duration_minutes INTEGER NOT NULL,
            status TEXT DEFAULT 'Active',         -- Active / Cancelled
            FOREIGN KEY (resource_code) REFERENCES resources(resource_code)
        )
    """)

    cur.execute("SELECT COUNT(*) FROM users WHERE role='Operator'")
    if cur.fetchone()[0] == 0:
        from auth import hash_password
        cur.execute(
            "INSERT INTO users (username, password, role, campus) VALUES (?,?,?,?)",
            ("operator", hash_password("admin123"), "Operator", "ALL")
        )
    conn.commit()
    conn.close()

def add_user(username, hashed_pw, role, campus):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password, role, campus) VALUES (?,?,?,?)",
            (username, hashed_pw, role, campus)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def add_resource(code, name, campus, category):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO resources (resource_code, name, campus, category) VALUES (?,?,?,?)",
            (code, name, campus, category)
        )
        conn.commit()
        return True, "Resource added."
    except sqlite3.IntegrityError:
        return False, "Duplicate resource code — rejected."
    finally:
        conn.close()

def update_resource(code, name, category):
    conn = get_connection()
    conn.execute(
        "UPDATE resources SET name=?, category=? WHERE resource_code=?",
        (name, category, code)
    )
    conn.commit()
    conn.close()

def delete_resource(code):
    conn = get_connection()
    conn.execute("DELETE FROM resources WHERE resource_code=?", (code,))
    conn.commit()
    conn.close()

def get_resources(campus=None):
    conn = get_connection()
    if campus:
        rows = conn.execute("SELECT * FROM resources WHERE campus=?", (campus,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM resources").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_resource(code):
    conn = get_connection()
    row = conn.execute("SELECT * FROM resources WHERE resource_code=?", (code,)).fetchone()
    conn.close()
    return dict(row) if row else None

def add_booking(resource_code, username, campus, date, start, duration):
    conn = get_connection()
    conn.execute(
        """INSERT INTO bookings (resource_code, username, campus, booking_date,
                                 start_time, duration_minutes, status)
           VALUES (?,?,?,?,?,?, 'Active')""",
        (resource_code, username, campus, date, start, duration)
    )
    conn.commit()
    conn.close()

def bookings_for_resource_on_date(resource_code, date):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM bookings WHERE resource_code=? AND booking_date=? AND status='Active'",
        (resource_code, date)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def bookings_for_user(username):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM bookings WHERE username=? ORDER BY booking_date, start_time",
        (username,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def bookings_for_campus(campus):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM bookings WHERE campus=? ORDER BY booking_date, start_time",
        (campus,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def all_bookings():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM bookings ORDER BY campus, booking_date").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def cancel_booking(booking_id):
    conn = get_connection()
    conn.execute("UPDATE bookings SET status='Cancelled' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()