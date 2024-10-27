import mysql.connector
from flask import Blueprint, redirect, render_template, request, url_for

order = Blueprint("order", __name__, template_folder="templates")

db_config = {
    "user": "demouser",
    "password": "demopassword",
    "database": "demodb",
    "host": "localhost",
}


@order.route("/orders", methods=["GET", "POST"])
def orders():

    if request.method == "POST":
        order_date = request.form["order_date"]
        customer_id = request.form["Customers"]
        product_id = request.form["Products"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        insert_query = (
            "INSERT INTO Orders"
            + "(customer_id, product_id, order_date)"
            + "VALUES (%s, %s, %s)"
        )

        cursor.execute(insert_query, (customer_id, product_id, order_date))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("order.orders"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT order_id, customer_name, product_name, "
        + "product_price, order_date "
        + "FROM Orders "
        + "JOIN Customers ON Orders.customer_id = Customers.customer_id "
        + "JOIN Products ON Orders.product_id = Products.product_id"
    )

    orders = cursor.fetchall()

    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    return render_template(
        "orders.html", orders=orders, customers=customers, products=products
    )


@order.route("/delete_order/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    delete_query = "DELETE FROM Orders " + "WHERE order_id = %s"

    cursor.execute(delete_query, (order_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("order.orders"))
