
from multiprocessing import connection

from flask import Flask, render_template, request, redirect, flash, session 

import sqlite3


app = Flask(__name__)
app.secret_key = "student_secret_key"  # Required for flashing messages

# ==============================
# CREATE DATABASE
# ==============================

def init_db():

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS students (

            id TEXT PRIMARY KEY,

            name TEXT,

            python INTEGER,

            java INTEGER,

            dbms INTEGER,

            total INTEGER,

            average REAL,

            grade TEXT

        )

    """)

    connection.commit()

    connection.close()

# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        # Simple Login

        if username == "admin" and password == "admin123":

            session["user"] = username

            flash("Login Successful!", "success")

            return redirect("/")

        else:

            flash("Invalid Username or Password", "danger")

    return render_template("login.html")

# ==============================
# LOGOUT
# ==============================

@app.route("/logout")

def logout():

    session.pop("user", None)

    flash("Logged Out Successfully!", "warning")

    return redirect("/login")

# ==============================
# HOME PAGE
# ==============================

@app.route("/")

def index():

    if "user" not in session:

        return redirect("/login")

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    search = request.args.get("search")

    if search:

        cursor.execute("""

            SELECT * FROM students

            WHERE name LIKE ? OR id LIKE ?

        """, (f"%{search}%", f"%{search}%"))

    else:

        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()

    return render_template(

        "index.html",

        students=students
    )
# ==============================
# ADD STUDENT
# ==============================

@app.route("/add", methods=["GET", "POST"])

def add_student():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        student_id = request.form["id"]

        student_name = request.form["name"]

        python_mark = int(request.form["python"])

        java_mark = int(request.form["java"])

        dbms_mark = int(request.form["dbms"])

        total = python_mark + java_mark + dbms_mark

        average = total / 3

        # Grade Logic

        if average >= 90:
            grade = "A+"

        elif average >= 75:
            grade = "A"

        elif average >= 60:
            grade = "B"

        elif average >= 50:
            grade = "C"

        else:
            grade = "Fail"

        # ==============================
        # DATABASE INSERT
        # ==============================

        connection = sqlite3.connect("database.db")

        cursor = connection.cursor()

        cursor.execute("""

            INSERT INTO students

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            student_id,

            student_name,

            python_mark,

            java_mark,

            dbms_mark,

            total,

            average,

            grade

        ))

        connection.commit()

        connection.close()

        flash("Student Added Successfully!", "success")

        return redirect("/")

    return render_template("add_student.html")

# ==============================
# DELETE STUDENT
# ==============================

@app.route("/delete/<student_id>")

def delete_student(student_id):

    if "user" not in session:
        return redirect("/login")

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute(

        "DELETE FROM students WHERE id = ?",

        (student_id,)

    )

    connection.commit()

    connection.close()

    flash("Student Deleted Successfully!", "danger")

    return redirect("/")

# ==============================
# EDIT STUDENT
# ==============================

@app.route("/edit/<student_id>", methods=["GET", "POST"])

def edit_student(student_id):

    if "user" not in session:
        return redirect("/login")

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    # GET STUDENT

    cursor.execute(

        "SELECT * FROM students WHERE id = ?",

        (student_id,)

    )

    student = cursor.fetchone()

    # UPDATE

    if request.method == "POST":

        name = request.form["name"]

        python_mark = int(request.form["python"])

        java_mark = int(request.form["java"])

        dbms_mark = int(request.form["dbms"])

        total = python_mark + java_mark + dbms_mark

        average = total / 3

        # Grade

        if average >= 90:
            grade = "A+"

        elif average >= 75:
            grade = "A"

        elif average >= 60:
            grade = "B"

        elif average >= 50:
            grade = "C"

        else:
            grade = "Fail"

        cursor.execute("""

            UPDATE students

            SET

                name = ?,

                python = ?,

                java = ?,

                dbms = ?,

                total = ?,

                average = ?,

                grade = ?

            WHERE id = ?

        """, (

            name,

            python_mark,

            java_mark,

            dbms_mark,

            total,

            average,

            grade,

            student_id

        ))

        connection.commit()

        connection.close()

        flash("Student Updated Successfully!", "warning")

        return redirect("/")

    connection.close()

    return render_template(

        "edit_student.html",

        student=student
    )


# ==============================
# RUN SERVER
# ==============================

init_db()

if __name__ == "__main__":

    app.run(debug=True)