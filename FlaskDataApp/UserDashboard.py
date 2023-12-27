import mysql.connector
from flask_mysqldb import MySQL
from flask import Flask, render_template

def view_dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    print(products)  # This retrieves all products from the database
    cursor.close()
    return render_template('user_dashboard.html', products=products)