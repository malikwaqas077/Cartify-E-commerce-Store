# dashboard.py
from flask import Blueprint, render_template, flash, redirect, url_for
from forms import ProductForm
from flask_mysqldb import MySQL

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@dashboard_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    mysql = MySQL()
    form = ProductForm()
    if form.validate_on_submit():
        # Get data from the form
        name = form.name.data
        description = form.description.data
        price = form.price.data

        # Insert the product into the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)", (name, description, price))
        mysql.connection.commit()
        cursor.close()

        flash('Product added successfully!', 'success')
        return render_template('add_product.html', form=form, success_message='Product added successfully!')

    return render_template('add_product.html', form=form)
