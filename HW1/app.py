""" A simple flask demo """

import mysql.connector
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

db_config = {
    "user": "demouser",
    "password": "demopassword",
    "database": "demodb",
    "host": "localhost",
}


@app.route("/", methods=["GET", "POST"])
def index():
    """default route"""

    if request.method == "POST":
        name = request.form["name"]
        semester = request.form["semester"]
        field = request.form["field"]
        created_at = request.form["created_at"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        insert_query = (
            "INSERT INTO students"
            + "(name, semester, field, created_at)"
            + "VALUES (%s, %s, %s, %s)"
        )

        cursor.execute(insert_query, (name, semester, field, created_at))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("index"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("students.html", students=students)


@app.route("/delete_student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    """deletes a student with the given id"""

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    delete_query = (
        "DELETE FROM students " +
        "WHERE id = %s"
    )

    cursor.execute(delete_query, (student_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("index"))
