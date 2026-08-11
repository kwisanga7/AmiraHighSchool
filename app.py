from flask import Flask, render_template, request
from database import register_student

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Welcome to Amira High School</h1>
    <a href='/register'>Register</a>
    """

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


if __name__ == "__main__":
    app.run(debug=True)