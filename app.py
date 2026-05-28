from flask import Flask, render_template, request, redirect, flask
import json

app = Flask(__name__)
app.secret_key = "student_secret_key"  # Required for flashing messages

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

    search = request.args.get("search")

    if search:

        filtered_students = []

        for student in students:

            if (

                search.lower() in student["name"].lower()

                or search in student["id"]

            ):

                filtered_students.append(student)

        students = filtered_students

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

        flash("Student Added Successfully!", "success")
        
        return redirect("/")

    return render_template("add_student.html")

# ==============================
# DELETE STUDENT
# ==============================

@app.route("/delete/<student_id>")

def delete_student(student_id):

    students = load_students()

    updated_students = []

    for student in students:

        if student["id"] != student_id:

            updated_students.append(student)

    save_students(updated_students)

    flash("Student Deleted Successfully!", "success")

    return redirect("/")

# ==============================
# EDIT STUDENT
# ==============================

@app.route("/edit/<student_id>", methods=["GET", "POST"])

def edit_student(student_id):

    students = load_students()

    student_data = None

    for student in students:

        if student["id"] == student_id:

            student_data = student

            break

    # UPDATE LOGIC

    if request.method == "POST":

        student_data["name"] = request.form["name"]

        student_data["python"] = int(request.form["python"])

        student_data["java"] = int(request.form["java"])

        student_data["dbms"] = int(request.form["dbms"])

        # Recalculate

        total = (

            student_data["python"]

            + student_data["java"]

            + student_data["dbms"]

        )

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

        student_data["total"] = total

        student_data["average"] = average

        student_data["grade"] = grade

        save_students(students)

        flash("Student Updated Successfully!", "warning")

        return redirect("/")

    return render_template(

        "edit_student.html",

        student=student_data
    )


# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":

    app.run(debug=True)