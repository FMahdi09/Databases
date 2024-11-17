from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["database"]
collection = db["students"] 


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        name = request.form["name"]
        semester = request.form["semester"]
        field = request.form["field"]
        created_at = request.form["created_at"]

        record = {
                "name": name,
                "semester": semester,
                "field": field,
                "created_at": created_at
        }

        collection.insert_one(record)

        return redirect(url_for("index"))

    students = list(collection.find({}))

    return render_template("index.html", students=students)
