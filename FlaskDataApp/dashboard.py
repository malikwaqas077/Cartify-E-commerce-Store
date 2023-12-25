# dashboard.py
from flask import Blueprint, render_template, flash, redirect, url_for
from forms import ProductForm
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
def dashboard():
    mysql = MySQL()
    cursor = mysql.connection.cursor()  
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    return render_template('dashboard.html', products=products)

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

@dashboard_bp.route('/view_products')
def view_products():
    mysql = MySQL()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    return render_template('view_products.html', products=products)

@dashboard_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    mysql = MySQL()
    cursor = mysql.connection.cursor(cursorclass=DictCursor)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()  # This should now return a dict
    cursor.close()

    form = ProductForm()
    if form.validate_on_submit():
        # Get data from the form
        name = form.name.data
        description = form.description.data
        price = form.price.data

        # Update the product in the database
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE products SET name=%s, description=%s, price=%s WHERE id=%s", (name, description, price, product_id))
        mysql.connection.commit()
        cursor.close()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('dashboard.view_products'))

    return render_template('edit_product.html', form=form, product=product)

@dashboard_bp.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    mysql = MySQL()
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Product deleted successfully!', 'success')
    return redirect(url_for('dashboard.view_products'))