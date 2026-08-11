import sqlite3

DATABASE = "amirahighschool.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ==============================
# Generate Student ID
# ==============================

def generate_student_id():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM registration
    WHERE login_type = 'student'
    """)

    count = cursor.fetchone()[0]

    next_number = count + 1

    student_id = f"AHM2026{next_number:03d}"

    conn.close()

    return student_id

# ==============================
# Register Student
# ==============================

def register_student(
        full_name,
        age,
        sector,
        date_of_birth,
        phone,
        password):

    student_id = generate_student_id()

    conn = get_connection()
    cursor = conn.cursor()

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
        student_id,
        full_name,
        age,
        sector,
        date_of_birth,
        phone,
        password,
        "student"
    ))

    conn.commit()
    conn.close()

    return student_id

# ==============================
# Login function
# ==============================

def login_user(phone, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM registration
    WHERE phone = ?
    AND password = ?
    """, (phone, password))

    user = cursor.fetchone()

    conn.close()

    return user

# ==============================
# Get all announcements
# ==============================

def get_announcements():

    conn = get_connection()

    announcements = conn.execute("""
    SELECT *
    FROM announcement
    ORDER BY id DESC
    """).fetchall()

    conn.close()

    return announcements

# ==============================
# Get all courses
# ==============================

def get_courses():

    conn = get_connection()

    courses = conn.execute("""
    SELECT *
    FROM courses
    ORDER BY course_id DESC
    """).fetchall()

    conn.close()

    return courses

# ==============================
# Dashboard Statistics
# ==============================

def total_students():

    conn = get_connection()

    total = conn.execute("""
    SELECT COUNT(*)
    FROM registration
    WHERE login_type='student'
    """).fetchone()[0]

    conn.close()

    return total


def total_announcements():

    conn = get_connection()

    total = conn.execute("""
    SELECT COUNT(*)
    FROM announcement
    """).fetchone()[0]

    conn.close()

    return total


def total_courses():

    conn = get_connection()

    total = conn.execute("""
    SELECT COUNT(*)
    FROM courses
    """).fetchone()[0]

    conn.close()

    return total