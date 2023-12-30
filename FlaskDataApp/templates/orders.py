from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_mysqldb import MySQL

order_bp = Blueprint('order_bp', __name__)
mysql=MySQL()   # MySQL object
@order_bp.route('/order')
def order():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECt ")


    return render_template('order.html')
