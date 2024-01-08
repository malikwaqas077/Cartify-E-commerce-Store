from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_mysqldb import MySQL
from flask import session

view_cart_bp = Blueprint('view_cart_bp', __name__)
mysql = MySQL()

@view_cart_bp.route('/view_cart', methods=['GET', 'POST'])
def view_cart_main():
    try:
        if request.method == 'POST':
            return update_cart()
        else:
            return view_cart()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_cart():
    if 'loggedin' in session and session['loggedin']:
        data = request.json
        user_id = session['id']
        product_id = data['product_id']
        action = data['action']

        cursor = mysql.connection.cursor()
        if action == 'increase':
            cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        elif action == 'decrease':
            cursor.execute("UPDATE cart SET quantity = quantity - 1 WHERE user_id = %s AND product_id = %s AND quantity > 1", (user_id, product_id))
        elif action == 'delete':
            cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))

        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Cart updated successfully"})
    else:
        return jsonify({"error": "User not logged in"}), 401

def view_cart():
    if 'loggedin' in session and session['loggedin']:
        user_id = session['id']  # Assuming user_id is stored in session
        cursor = mysql.connection.cursor()
        query = """
        SELECT p.*, c.quantity 
        FROM products p 
        JOIN cart c ON p.id = c.product_id 
        WHERE c.user_id = %s
        """ 
        cursor.execute(query, (user_id,))
        cart_items = cursor.fetchall()
        print(f"cart_items:{cart_items}")

        total_items = 0
        total_amount = 0.0
        cart_items_info = []

        for item in cart_items:
            print(item)
            price_without_comma = float(item[2].replace(',', ''))
            quantity = int(item[5])
            subtotal = price_without_comma * quantity
            total_items += quantity
            total_amount += subtotal

            cart_item_with_subtotal = item + (subtotal,)
            cart_items_info.append(cart_item_with_subtotal)

        cursor.close()
        return render_template('view_cart.html', cart_items=cart_items_info, total_items=total_items, total_amount=total_amount)
    else:
        flash('Please log in to view your cart', 'danger')
        return redirect(url_for('bp_user_login.user_login'))

# Make sure to register the Blueprint in your main app.
