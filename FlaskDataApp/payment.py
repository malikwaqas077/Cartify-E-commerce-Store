from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_mysqldb import MySQL

# Create a Blueprint for the payment functionality
payment_bp = Blueprint('payment_bp', __name__)
mysql = MySQL()   # MySQL object

@payment_bp.route('/payment')
def payment():
    # Simply render the payment form template
    return render_template('payment_form.html')

@payment_bp.route('/charge', methods=['POST'])
def charge():
    card_name = request.form['name']
    card_number = request.form['cardNumber']
    card_expiry = request.form['expiry']
    card_cvv = request.form['cvv']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO payment_info (card_name, card_number, card_expiry, card_cvv) VALUES (%s, %s, %s, %s)", (card_name, card_number, card_expiry, card_cvv))
    mysql.connection.commit()
    
    cursor.execute("""
    SELECT c.product_id, c.quantity, p.price 
    FROM cart c
    JOIN products p ON c.product_id = p.id
    WHERE c.user_id = %s
    """, (session['id'],))
    cart_items = cursor.fetchall()

    if not cart_items:
        flash("Cart is empty", "error")
        return redirect(url_for('payment_bp.payment'))  # Redirect back to payment form

    total_amount = sum([float(item[1]) * float(item[2]) for item in cart_items])  # Calculate total amount
    cursor.execute("INSERT INTO orders (user_id, total_amount, order_status) VALUES (%s, %s, 'Pending')", (session['id'], total_amount))
    order_id = cursor.lastrowid

    for item in cart_items:
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)", (order_id, item[0], item[1], item[2]))

    cursor.execute("DELETE FROM cart WHERE user_id = %s", (session['id'],))
    mysql.connection.commit()
    cursor.close()

    flash('Order placed successfully', 'success')
    return redirect(url_for('payment_bp.payment'))  # Redirect back to payment form after successful charge
