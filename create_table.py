# =========================
# Insert password hashing for admin password
# =========================

from werkzeug.security import generate_password_hash
import sqlite3


# Connect to database
conn = sqlite3.connect("amirahighschool.db")
cursor = conn.cursor()

# =========================
# REGISTRATION TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS registration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE,
    full_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    sector TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    login_type TEXT NOT NULL DEFAULT 'student'
)
""")

# =========================
# ANNOUNCEMENT TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS announcement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    photo TEXT,
    message TEXT NOT NULL
)
""")

# =========================
# COURSES TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    duration TEXT NOT NULL,
    teacher TEXT NOT NULL,
    fees REAL NOT NULL,
    photo TEXT
)
""")

# =========================
# CREATE DEFAULT ADMIN
# =========================

admin_phone = "0788000000"
hashed_admin_password = generate_password_hash("admin123")

cursor.execute("""
SELECT * FROM registration
WHERE phone = ?
""", (admin_phone,))

admin_exists = cursor.fetchone()

if not admin_exists:
    cursor.execute("""
    INSERT INTO registration
    (
        student_id,
        full_name,
        age,
        sector,
        date_of_birth,
        phone,
        password,
        login_type
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        "ADMIN001",
        "System Administrator",
        30,
        "Kigali",
        "1996-01-01",
        admin_phone,
        hashed_admin_password,
        "admin"
    ))

    print("Default admin created successfully.")
else:
    print("Admin already exists.")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database tables created successfully.")