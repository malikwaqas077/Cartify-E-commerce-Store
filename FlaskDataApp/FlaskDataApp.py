from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import mysql.connector
from flask_mysqldb import MySQL
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import ValidationError
from flask import Flask
from models import db
from forms import ProductForm
from dashboard import dashboard_bp
from view_cart import view_cart_bp    
# from payment_proceed import payment_proceed_bp
from payment import payment_bp  # Import the payment blueprint
from user_login import bp_user_login  # Import the user_login blueprint
from flask import session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Malik786'
app.config['MYSQL_DB'] = 'crud_app_db'
mysql = MySQL(app)


app.register_blueprint(dashboard_bp)  # Register the blueprint
app.register_blueprint(view_cart_bp)  # Register the blueprint
# app.payment_proceed_bp(payment_proceed_bp)  # Register the blueprint
app.register_blueprint(payment_bp)  # Register the blueprint
app.register_blueprint(bp_user_login)  # Register the blueprint

# User registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_confirm(self, field):
        if self.password.data != field.data:
            raise ValidationError('Passwords must match')

# User login form
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Sign In')

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (form.username.data, form.password.data))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (form.username.data, form.password.data))
        user = cursor.fetchone()
        cursor.close()
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard'))  # Redirect to the dashboard

        else:
            flash('Login failed. Check your username and password.', 'danger')
            flash('Or register if you have not done so already.', 'danger')
    return render_template('login.html', form=form)

@app.route('/user_dashboard')
def view_dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    print(products)
      # This retrieves all products from the database
    cursor.close()
    return render_template('user_dashboard.html', products=products)

@app.route('/add_to_cart', methods=['POST'])

def add_to_cart():
    print("add to cart")
    # Check if the user is logged in
    if 'loggedin' in session and session['loggedin']:
        # User is logged in, process the add to cart action
        product_id = request.form['product_id']
        print(f"this is product id {product_id}")
        user_id = session['id']  # Assuming user_id is stored in session
        print(f"this is user id {user_id}")
        # Add the product to the cart in the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, 1)", (user_id, product_id))
        mysql.connection.commit()
        cursor.close()

        
        return redirect(url_for('view_dashboard'))  # Redirect to a relevant page
    else:
        print("user not logged in")
        #User is not logged in, redirect to the login page
        flash('Please log in to add items to your cart', 'error')
        return redirect(url_for('bp_user_login.user_login'))  # Redirect to the login page


@app.route('/check_cart')
def check_cart():
    user_id = session.get('id')
    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM cart WHERE user_id = %s", (user_id,))
        cart_count = cursor.fetchone()[0]
        print(f"This is a cart_count{cart_count}")
        cursor.close()
        return {'cart_empty': cart_count == 0}
    else:
        # Handle the case where the user is not logged in
        return {'cart_empty': True}


# @app.route('/view_cart')
# def view_cart():
#     user_id = 1
#     return render_template('view_cart.html', user_id=user_id)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('view_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)



