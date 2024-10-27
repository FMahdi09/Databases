""" A simple flask demo """

from flask import Flask, render_template

from customer import customer
from order import order
from product import product

app = Flask(__name__)
app.register_blueprint(customer)
app.register_blueprint(product)
app.register_blueprint(order)

db_config = {
    "user": "demouser",
    "password": "demopassword",
    "database": "demodb",
    "host": "localhost",
}


@app.route("/", methods=["GET"])
def index():
    """default route"""
    return render_template("index.html")
