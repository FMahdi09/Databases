import mysql.connector
from flask import Blueprint, redirect, render_template, request, url_for

product = Blueprint("product", __name__, template_folder="templates")

db_config = {
    "user": "demouser",
    "password": "demopassword",
    "database": "demodb",
    "host": "localhost",
}


@product.route("/products", methods=["GET", "POST"])
def products():

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        insert_query = (
            "INSERT INTO Products"
            + "(product_name, product_price)"
            + "VALUES (%s, %s)"
        )

        cursor.execute(insert_query, (name, price))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("product.products"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    return render_template("products.html", products=products)


@product.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    delete_query = "DELETE FROM Products " + "WHERE product_id = %s"

    cursor.execute(delete_query, (product_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("product.products"))


@product.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        update_query = (
            "UPDATE Products "
            + "SET product_name = %s, product_price = %s "
            + "WHERE product_id = %s"
        )

        cursor.execute(update_query, (name, price, product_id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("product.products"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    select_query = "SELECT * FROM Products WHERE product_id = %s"

    cursor.execute(select_query, (product_id,))

    product = cursor.fetchone()

    return render_template("edit_product.html", product=product)
