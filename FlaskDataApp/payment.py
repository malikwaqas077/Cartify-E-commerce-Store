# payment.py

from flask import Blueprint, render_template
from flask import request
from flask_mysqldb import MySQL
from flask import flash

# Create a Blueprint for the payment functionality
payment_bp = Blueprint('payment_bp', __name__)
mysql=MySQL()   # MySQL object
@payment_bp.route('/payment')
def payment():
    # Simply render the payment form template
    return render_template('payment_form.html')


@payment_bp.route('/charge', methods=['POST'])
def charge():
    card_name=request.form['name']
    card_number=request.form['cardNumber']
    card_expiry=request.form['expiry']
    card_cvv=request.form['cvv']

    cursor=mysql.connection.cursor()
    cursor.execute("INSERT INTO payment_info (card_name, card_number, card_expiry, card_cvv) VALUES (%s, %s, %s, %s)", (card_name, card_number, card_expiry, card_cvv))
    mysql.connection.commit()
    flash("Payment Successful", "success")
    cursor.close()  # Close the cursor

    return render_template('payment_form.html')

