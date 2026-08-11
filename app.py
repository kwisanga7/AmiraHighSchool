from database import (
    register_student,
    login_user,
    total_students,
    total_announcements,
    total_courses,
    add_announcement,
    get_all_announcements,
    get_announcement,
    delete_announcement,
    update_announcement
)

from database import (
    add_course,
    get_all_courses,
    get_course,
    update_course,
    delete_course,
    get_all_students,
    get_student,
    update_student,
    delete_student
)

import os
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, session
from database import register_student, login_user

app = Flask(__name__)
app.secret_key = "amira_high_school_secret_key"

UPLOAD_FOLDER = "static/uploads/announcements"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

COURSE_UPLOAD_FOLDER = "static/uploads/courses"
app.config["COURSE_UPLOAD_FOLDER"] = COURSE_UPLOAD_FOLDER

# ===========================
# Home Route
# ===========================

@app.route("/")
def home():

    return """
    <h1>Welcome to Amira High School</h1>

    <a href='/register'>Register</a><br><br>

    <a href='/login'>Login</a>
    """


# ===========================
# Register Route
# ===========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        age = request.form["age"]
        sector = request.form["sector"]
        date_of_birth = request.form["date_of_birth"]
        phone = request.form["phone"]
        password = request.form["password"]

        student_id = register_student(
            full_name,
            age,
            sector,
            date_of_birth,
            phone,
            password
        )

        return f"""
        Registration Successful!<br><br>
        Your Student ID is: <b>{student_id}</b><br><br>
        <a href='/register'>Register Another Student</a>
        """

    return render_template("register.html")


# ===========================
# Login Route
# ===========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        phone = request.form["phone"]
        password = request.form["password"]

        user = login_user(phone, password)

        if user:

            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["login_type"] = user["login_type"]

            if user["login_type"] == "admin":
                return redirect("/admin/dashboard")

            return redirect("/student/dashboard")

        return "Invalid phone number or password"

    return render_template("login.html")


# ===========================
# Student Dashboard Route
# ===========================

@app.route("/student/dashboard")
def student_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "student":
        return "Access Denied"

    return render_template("student_dashboard.html")


# ===========================
# Admin Dashboard Route
# ===========================

@app.route("/admin/dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    students = total_students()
    announcements = total_announcements()
    courses = total_courses()

    return render_template(
        "admin_dashboard.html",
        students=students,
        announcements=announcements,
        courses=courses
    )


# ===========================
# Logout Route
# ===========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# ===========================
# Add Announcement Route
# ===========================

@app.route("/admin/announcements/add", methods=["GET", "POST"])
def add_announcement_page():

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    if request.method == "POST":

        title = request.form["title"]
        message = request.form["message"]

        image = request.files["photo"]

        filename = ""

        if image and image.filename:

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        add_announcement(
            title,
            filename,
            message
        )

        return redirect("/admin/announcements")

    return render_template("add_announcement.html")


# ==========================
# View Announcements Route
# ==========================

@app.route("/admin/announcements")
def announcements():

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    announcements = get_all_announcements()

    return render_template(
        "announcements.html",
        announcements=announcements
    )

# ==========================
# Edite Announcement Route
# ==========================

@app.route("/admin/announcements/edit/<int:id>",
           methods=["GET", "POST"])
def edit_announcement(id):

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    announcement = get_announcement(id)

    if request.method == "POST":

        title = request.form["title"]
        message = request.form["message"]

        update_announcement(
            id,
            title,
            message
        )

        return redirect("/admin/announcements")

    return render_template(
        "edit_announcement.html",
        announcement=announcement
    )

# ==========================
# Delete Announcement Route
# ==========================

@app.route("/admin/announcements/delete/<int:id>")
def delete_announcement_page(id):

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    delete_announcement(id)

    return redirect("/admin/announcements")

# ==========================
# Student View Announcements Route
# ==========================

@app.route("/student/announcements")
def student_announcements():

    if "user_id" not in session:
        return redirect("/login")

    announcements = get_all_announcements()

    return render_template(
        "student_announcements.html",
        announcements=announcements
    )

# ==========================
# Add Course Route
# ==========================

@app.route("/admin/courses/add",
           methods=["GET", "POST"])
def add_course_page():

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    if request.method == "POST":

        course_name = request.form["course_name"]
        duration = request.form["duration"]
        teacher = request.form["teacher"]
        fees = request.form["fees"]

        image = request.files["photo"]

        filename = ""

        if image and image.filename:

            filename = secure_filename(
                image.filename
            )

            image.save(
                os.path.join(
                    COURSE_UPLOAD_FOLDER,
                    filename
                )
            )

        add_course(
            course_name,
            duration,
            teacher,
            fees,
            filename
        )

        return redirect("/admin/courses")

    return render_template("add_course.html")

# =========================
# View Courses Route
# =========================

@app.route("/admin/courses")
def courses():

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    courses = get_all_courses()

    return render_template(
        "courses.html",
        courses=courses
    )

# =========================
# Edit Course Route
# =========================

@app.route("/admin/courses/edit/<int:course_id>",
           methods=["GET", "POST"])
def edit_course_page(course_id):

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    course = get_course(course_id)

    if request.method == "POST":

        update_course(
            course_id,
            request.form["course_name"],
            request.form["duration"],
            request.form["teacher"],
            request.form["fees"]
        )

        return redirect("/admin/courses")

    return render_template(
        "edit_course.html",
        course=course
    )

# =========================
# Delete Course Route
# =========================

@app.route("/admin/courses/delete/<int:course_id>")
def delete_course_page(course_id):

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    delete_course(course_id)

    return redirect("/admin/courses")

# =========================
# Student View Courses Route
# =========================

@app.route("/student/courses")
def student_courses():

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "student":
        return "Access Denied"

    courses = get_all_courses()

    return render_template(
        "student_courses.html",
        courses=courses
    )

# =========================
# Student list Route
# =========================

@app.route("/admin/students")
def students():

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    students = get_all_students()

    return render_template(
        "students.html",
        students=students
    )

# =========================
# Edit Student Route
# =========================

@app.route("/admin/students/edit/<int:id>",
           methods=["GET", "POST"])
def edit_student_page(id):

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    student = get_student(id)

    if request.method == "POST":

        update_student(
            id,
            request.form["full_name"],
            request.form["age"],
            request.form["sector"],
            request.form["date_of_birth"],
            request.form["phone"]
        )

        return redirect("/admin/students")

    return render_template(
        "edit_student.html",
        student=student
    )

# =========================
# Delete Student Route
# =========================

@app.route("/admin/students/delete/<int:id>")
def delete_student_page(id):

    if "user_id" not in session:
        return redirect("/login")

    if session["login_type"] != "admin":
        return "Access Denied"

    delete_student(id)

    return redirect("/admin/students")

if __name__ == "__main__":
    app.run(debug=True)
