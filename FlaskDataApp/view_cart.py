from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_mysqldb import MySQL



view_cart_bp = Blueprint('view_cart_bp', __name__)

mysql = MySQL()

@view_cart_bp.route('/view_cart')
def view_cart():
    user_id = 1  # Assuming user_id is stored in session
    if not user_id:
        # Handle the case where the user is not logged in
        return "Please log in to view your cart", 401

    cursor = mysql.connection.cursor()
    query = """
    SELECT p.*, c.quantity 
    FROM products p 
    JOIN cart c ON p.id = c.product_id 
    WHERE c.user_id = %s
    """ # This query retrieves all products in the cart for the userz
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    print(f"This is view cart items list{cart_items}")

    total_items = 0
    total_amount = 0.0
    cart_items_info = []

    for item in cart_items:
        subtotal = item[2] * item[5]  # Calculate subtotal
        total_items += item[5]
        total_amount += subtotal

        # Create a new structure that includes the subtotal
        cart_item_with_subtotal = item + (subtotal,)
        cart_items_info.append(cart_item_with_subtotal)


    cursor.close()

    return render_template('view_cart.html', cart_items=cart_items, total_items=total_items, total_amount=total_amount)