# =============================
# Password Hashing 
#=============================

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
hashed_password = generate_password_hash("admin123")

# =============================
# Database Connection
# =============================

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


from werkzeug.security import generate_password_hash

def register_student(
    full_name,
    age,
    sector,
    date_of_birth,
    phone,
    password
):

    student_id = generate_student_id()

    hashed_password = generate_password_hash(password)

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
        hashed_password,
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

    user = conn.execute("""
    SELECT *
    FROM registration
    WHERE phone = ?
    """, (phone,)).fetchone()

    conn.close()

    if user and check_password_hash(
            user["password"],
            password):

        return user

    return None

# ==============================
# Get all announcements
# ==============================

def get_all_announcements():

    conn = get_connection()

    announcements = conn.execute("""
    SELECT *
    FROM announcement
    ORDER BY id ASC
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

# ==============================
# Add Announcement
# ==============================

def add_announcement(title, photo, message):

    conn = get_connection()

    conn.execute("""
    INSERT INTO announcement
    (title, photo, message)
    VALUES (?, ?, ?)
    """, (title, photo, message))

    conn.commit()
    conn.close()

# ==============================
# Get All Announcements
# ==============================

def get_all_announcements():

    conn = get_connection()

    announcements = conn.execute("""
    SELECT *
    FROM announcement
    ORDER BY id ASC
    """).fetchall()

    conn.close()

    return announcements

# ==============================
# Get One Announcement
# ==============================

def get_announcement(id):

    conn = get_connection()

    announcement = conn.execute("""
    SELECT *
    FROM announcement
    WHERE id = ?
    """, (id,)).fetchone()

    conn.close()

    return announcement

# ==============================
# Delete Announcement
# ==============================

def delete_announcement(id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM announcement
    WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

# ==============================
# Update Announcement
# ==============================

def update_announcement(id, title, message):

    conn = get_connection()

    conn.execute("""
    UPDATE announcement
    SET title = ?, message = ?
    WHERE id = ?
    """, (title, message, id))

    conn.commit()
    conn.close()

# ==============================
# Add Course
# ==============================

def add_course(
        course_name,
        duration,
        teacher,
        fees,
        photo):

    conn = get_connection()

    conn.execute("""
    INSERT INTO courses
    (
        course_name,
        duration,
        teacher,
        fees,
        photo
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        course_name,
        duration,
        teacher,
        fees,
        photo
    ))

    conn.commit()
    conn.close()

# ==============================
# Get All Courses
# ==============================

def get_all_courses():

    conn = get_connection()

    courses = conn.execute("""
    SELECT *
    FROM courses
    ORDER BY course_id ASC
    """).fetchall()

    conn.close()

    return courses
# ==============================
# Get One Course
# ==============================

def get_course(course_id):

    conn = get_connection()

    course = conn.execute("""
    SELECT *
    FROM courses
    WHERE course_id = ?
    """, (course_id,)).fetchone()

    conn.close()

    return course

# ==============================
# Update Course
# ==============================

def update_course(
        course_id,
        course_name,
        duration,
        teacher,
        fees):

    conn = get_connection()

    conn.execute("""
    UPDATE courses
    SET
        course_name = ?,
        duration = ?,
        teacher = ?,
        fees = ?
    WHERE course_id = ?
    """,
    (
        course_name,
        duration,
        teacher,
        fees,
        course_id
    ))

    conn.commit()
    conn.close()

# ==============================
# Delete Course
# ==============================

def delete_course(course_id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM courses
    WHERE course_id = ?
    """, (course_id,))

    conn.commit()
    conn.close()

# ==============================
# Get All Students
# ==============================

def get_all_students():

    conn = get_connection()

    students = conn.execute("""
    SELECT *
    FROM registration
    WHERE login_type = 'student'
    ORDER BY id ASC
    """).fetchall()

    conn.close()

    return students

# ==============================
# Get One Student
# ==============================

def get_student(id):

    conn = get_connection()

    student = conn.execute("""
    SELECT *
    FROM registration
    WHERE id = ?
    """, (id,)).fetchone()

    conn.close()

    return student

# ==============================
# Update Student
# ==============================

def update_student(
        id,
        full_name,
        age,
        sector,
        date_of_birth,
        phone):

    conn = get_connection()

    conn.execute("""
    UPDATE registration
    SET
        full_name = ?,
        age = ?,
        sector = ?,
        date_of_birth = ?,
        phone = ?
    WHERE id = ?
    """,
    (
        full_name,
        age,
        sector,
        date_of_birth,
        phone,
        id
    ))

    conn.commit()
    conn.close()

# ==============================
# Delete Student
# ==============================

def delete_student(id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM registration
    WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()