import mysql.connector
from flask import Blueprint, redirect, render_template, request, url_for

customer = Blueprint("customer", __name__, template_folder="templates")

db_config = {
    "user": "demouser",
    "password": "demopassword",
    "database": "demodb",
    "host": "localhost",
}


@customer.route("/customers", methods=["GET", "POST"])
def customers():

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        created_at = request.form["created_at"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        insert_query = (
            "INSERT INTO Customers"
            + "(customer_name, customer_age, created_at)"
            + "VALUES (%s, %s, %s)"
        )

        cursor.execute(insert_query, (name, age, created_at))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("customer.customers"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()

    return render_template("customers.html", customers=customers)


@customer.route("/delete_customer/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    delete_query = "DELETE FROM Customers " + "WHERE customer_id = %s"

    cursor.execute(delete_query, (customer_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("customer.customers"))


@customer.route("/edit_customer/<int:customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        created_at = request.form["created_at"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        update_query = (
            "UPDATE Customers "
            + "SET customer_name = %s, customer_age = %s , created_at = %s "
            + "WHERE customer_id = %s"
        )

        cursor.execute(update_query, (name, age, created_at, customer_id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("customer.customers"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    select_query = "SELECT * FROM Customers WHERE customer_id = %s"

    cursor.execute(select_query, (customer_id,))

    customer = cursor.fetchone()

    return render_template("edit_customer.html", customer=customer)
