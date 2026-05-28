from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


# ==============================
# LOAD STUDENTS
# ==============================

def load_students():

    try:

        with open("students.json", "r") as file:

            return json.load(file)

    except:

        return []


# ==============================
# SAVE STUDENTS
# ==============================

def save_students(students):

    with open("students.json", "w") as file:

        json.dump(students, file, indent=4)


# ==============================
# HOME PAGE
# ==============================

@app.route("/")

def index():

    students = load_students()

    return render_template("index.html", students=students)


# ==============================
# ADD STUDENT
# ==============================

@app.route("/add", methods=["GET", "POST"])

def add_student():

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

        # Student Data

        student = {

            "id": student_id,

            "name": student_name,

            "python": python_mark,

            "java": java_mark,

            "dbms": dbms_mark,

            "total": total,

            "average": average,

            "grade": grade
        }

        students = load_students()

        students.append(student)

        save_students(students)

        return redirect("/")

    return render_template("add_student.html")


# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":

    app.run(debug=True)